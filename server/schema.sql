-- BlueLedger relational schema (SQLite)
-- Mirrors the ER design in Assessment_6_Project_Proposal (COMMUNITY -< USER, USER -< PROJECT,
-- SPECIES -< PROJECT, PROJECT -< CREDIT_TRANSACTION, USER -< CREDIT_TRANSACTION).

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS community (
    community_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS user (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    phone         TEXT,
    username      TEXT,
    community_id  INTEGER REFERENCES community(community_id)
);

CREATE TABLE IF NOT EXISTS species (
    species_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name                 TEXT NOT NULL UNIQUE,
    credits_per_hectare  REAL NOT NULL CHECK (credits_per_hectare > 0)
);

CREATE TABLE IF NOT EXISTS project (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plot_id    TEXT NOT NULL,
    user_id    INTEGER NOT NULL REFERENCES user(user_id),
    species_id INTEGER NOT NULL REFERENCES species(species_id),
    hectares   REAL NOT NULL CHECK (hectares > 0),
    gps_lat    REAL NOT NULL,
    gps_lng    REAL NOT NULL,
    image_uri  TEXT,
    status     TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'VERIFIED', 'REJECTED')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS credit_transaction (
    txn_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES user(user_id),
    project_id INTEGER REFERENCES project(project_id),
    txn_type   TEXT NOT NULL CHECK (txn_type IN ('MINT', 'REDEEM')),
    credits    REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_project_user ON project(user_id);
CREATE INDEX IF NOT EXISTS idx_txn_user ON credit_transaction(user_id);
CREATE INDEX IF NOT EXISTS idx_txn_project ON credit_transaction(project_id);
