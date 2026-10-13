"""
BlueLedger demo backend.

A tiny FastAPI service backed by SQLite, standing in for the "real" database the
BlueLedger Android app doesn't have yet. Run this on your laptop; point the phone
app's Server IP setting at this machine's LAN address (see README.md in this folder).

Not production-grade (password hashing is a plain SHA-256 digest, there's no auth
token/session, CORS is wide open) -- this exists to demonstrate the relational
schema and let a phone on the same wifi write rows a laptop can see land live.
"""
import hashlib
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "blueledger.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

SEED_SPECIES = [
    ("Rhizophora", 14.0),
    ("Avicennia", 12.0),
    ("Bruguiera", 10.0),
]
SEED_COMMUNITY = "Mangrove Bay Community"


def area_bonus_multiplier(hectares: float) -> float:
    if hectares >= 10.0:
        return 1.2
    if hectares >= 5.0:
        return 1.1
    return 1.0


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        cur = conn.execute("SELECT COUNT(*) FROM species")
        if cur.fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO species (name, credits_per_hectare) VALUES (?, ?)",
                SEED_SPECIES,
            )
        cur = conn.execute("SELECT COUNT(*) FROM community")
        if cur.fetchone()[0] == 0:
            conn.execute("INSERT INTO community (name) VALUES (?)", (SEED_COMMUNITY,))
        conn.commit()
    finally:
        conn.close()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="BlueLedger Demo API", lifespan=lifespan)

# Demo-only: the phone's IP on a classroom/home wifi isn't known ahead of time,
# so we allow any origin rather than hardcoding one.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SignupRequest(BaseModel):
    email: str
    phone: str = ""
    username: str = ""
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    phone: Optional[str] = ""
    username: Optional[str] = ""


class SpeciesOut(BaseModel):
    id: int
    name: str
    credits_per_hectare: float


class CommunityOut(BaseModel):
    id: int
    name: str


class ProjectRequest(BaseModel):
    user_id: int
    plot_id: str
    species: str
    hectares: float
    gps_lat: float
    gps_lng: float
    image_uri: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    plot_id: str
    species: str
    hectares: float
    gps_lat: float
    gps_lng: float
    image_uri: Optional[str] = None
    minted_credits: int
    status: str
    created_at: str


class WalletOut(BaseModel):
    total_credits: int
    total_hectares: float


def _user_row_to_out(row: sqlite3.Row) -> UserOut:
    return UserOut(id=row["user_id"], email=row["email"], phone=row["phone"] or "", username=row["username"] or "")


@app.post("/api/signup", response_model=UserOut)
def signup(req: SignupRequest, db: sqlite3.Connection = Depends(get_db)):
    existing = db.execute("SELECT 1 FROM user WHERE email = ?", (req.email,)).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    community = db.execute("SELECT community_id FROM community ORDER BY community_id LIMIT 1").fetchone()
    cur = db.execute(
        "INSERT INTO user (email, password_hash, phone, username, community_id) VALUES (?, ?, ?, ?, ?)",
        (req.email, hash_password(req.password), req.phone, req.username, community["community_id"] if community else None),
    )
    db.commit()
    row = db.execute("SELECT * FROM user WHERE user_id = ?", (cur.lastrowid,)).fetchone()
    return _user_row_to_out(row)


@app.post("/api/login", response_model=UserOut)
def login(req: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM user WHERE email = ?", (req.email,)).fetchone()
    if row is None or row["password_hash"] != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return _user_row_to_out(row)


@app.get("/api/species", response_model=list[SpeciesOut])
def list_species(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("SELECT * FROM species ORDER BY species_id").fetchall()
    return [SpeciesOut(id=r["species_id"], name=r["name"], credits_per_hectare=r["credits_per_hectare"]) for r in rows]


@app.get("/api/communities", response_model=list[CommunityOut])
def list_communities(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute("SELECT * FROM community ORDER BY community_id").fetchall()
    return [CommunityOut(id=r["community_id"], name=r["name"]) for r in rows]


def _project_row_to_out(row: sqlite3.Row, species_name: str, minted_credits: int) -> ProjectOut:
    return ProjectOut(
        id=row["project_id"],
        plot_id=row["plot_id"],
        species=species_name,
        hectares=row["hectares"],
        gps_lat=row["gps_lat"],
        gps_lng=row["gps_lng"],
        image_uri=row["image_uri"],
        minted_credits=minted_credits,
        status=row["status"],
        created_at=row["created_at"],
    )


@app.post("/api/projects", response_model=ProjectOut)
def create_project(req: ProjectRequest, db: sqlite3.Connection = Depends(get_db)):
    user = db.execute("SELECT 1 FROM user WHERE user_id = ?", (req.user_id,)).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Unknown user_id")
    species = db.execute("SELECT * FROM species WHERE name = ?", (req.species,)).fetchone()
    if not species:
        raise HTTPException(status_code=400, detail=f"Unknown species '{req.species}'")
    if req.hectares <= 0:
        raise HTTPException(status_code=400, detail="hectares must be > 0")

    minted = int(req.hectares * species["credits_per_hectare"] * area_bonus_multiplier(req.hectares))
    minted = max(minted, 1)

    cur = db.execute(
        """INSERT INTO project (plot_id, user_id, species_id, hectares, gps_lat, gps_lng, image_uri)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (req.plot_id, req.user_id, species["species_id"], req.hectares, req.gps_lat, req.gps_lng, req.image_uri),
    )
    project_id = cur.lastrowid
    db.execute(
        "INSERT INTO credit_transaction (user_id, project_id, txn_type, credits) VALUES (?, ?, 'MINT', ?)",
        (req.user_id, project_id, minted),
    )
    db.commit()

    row = db.execute("SELECT * FROM project WHERE project_id = ?", (project_id,)).fetchone()
    return _project_row_to_out(row, species["name"], minted)


@app.get("/api/projects", response_model=list[ProjectOut])
def list_projects(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute(
        """SELECT p.*, s.name AS species_name,
                  COALESCE((SELECT SUM(credits) FROM credit_transaction WHERE project_id = p.project_id), 0) AS minted
           FROM project p JOIN species s ON s.species_id = p.species_id
           WHERE p.user_id = ?
           ORDER BY p.project_id DESC""",
        (user_id,),
    ).fetchall()
    return [_project_row_to_out(r, r["species_name"], int(r["minted"])) for r in rows]


@app.get("/api/wallet/{user_id}", response_model=WalletOut)
def get_wallet(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    credits_row = db.execute(
        "SELECT COALESCE(SUM(CASE WHEN txn_type = 'MINT' THEN credits ELSE -credits END), 0) AS total "
        "FROM credit_transaction WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    hectares_row = db.execute(
        "SELECT COALESCE(SUM(hectares), 0) AS total FROM project WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return WalletOut(total_credits=int(credits_row["total"]), total_hectares=hectares_row["total"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
