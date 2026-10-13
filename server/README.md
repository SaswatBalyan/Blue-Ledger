# BlueLedger demo backend

A small FastAPI + SQLite server that stands in for a real backend database, so the
BlueLedger Android app can demonstrate writing to a relational database over the network
instead of a local on-device blob. **This is a classroom demo, not production code** —
password hashing is a plain SHA-256 digest, there's no auth token/session, and CORS/HTTP
are wide open.

## 1. One-time setup (on your laptop)

```bash
cd server
python -m venv venv
venv\Scripts\activate        # PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Find your laptop's LAN IP

Your phone needs this to reach the server. With the laptop connected to the same wifi
as your phone:

```powershell
ipconfig
```

Look for the "Wireless LAN adapter Wi-Fi" section → **IPv4 Address**, e.g. `192.168.1.42`.
(If Windows Firewall prompts when you start the server below, allow access on **private
networks** — that's the home/classroom wifi.)

## 3. Run the server

```bash
venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

`--host 0.0.0.0` is what makes it reachable from other devices on the wifi, not just the
laptop itself. Leave this running during the demo. The database file `blueledger.db`
(created next to this README on first run) is a plain SQLite file — open it anytime in
[DB Browser for SQLite](https://sqlitebrowser.org/) to show the tables filling up live.

## 4. Point the phone app at it

In the BlueLedger app's first screen (Onboarding, where you pick Login/Sign up), there's
a small "Server:" field at the top. Type `<your-laptop-ip>:8000`, e.g. `192.168.1.42:8000`
— then sign up / log in. If it can't reach the server you'll see an error on the
Login/Signup screen telling you to check the IP.

## 5. Demo flow

1. Start the server (step 3), confirm it printed `Uvicorn running on http://0.0.0.0:8000`.
2. On the phone: enter the server IP on the Onboarding screen, sign up a new account.
3. Go to the Upload tab, fill in a plot, pick a species, enter hectares, submit.
4. A snackbar on the phone confirms "Project submitted — N credits minted".
5. On the laptop: open `server/blueledger.db` in DB Browser for SQLite (or run the
   `sqlite3` CLI query below) and show the new row in `project` and `credit_transaction`,
   or just refresh `http://<laptop-ip>:8000/api/projects?user_id=1` in a browser.

Quick CLI check instead of a GUI tool:

```bash
sqlite3 blueledger.db "select * from project; select * from credit_transaction;"
```

## API reference

| Method | Path                      | Purpose                                  |
|--------|---------------------------|-------------------------------------------|
| POST   | `/api/signup`              | Create a user                            |
| POST   | `/api/login`               | Verify credentials                       |
| GET    | `/api/species`             | List species + credit rate per hectare   |
| GET    | `/api/communities`         | List communities                         |
| POST   | `/api/projects`            | Submit a project; mints a credit ledger row |
| GET    | `/api/projects?user_id=`   | List a user's projects                   |
| GET    | `/api/wallet/{user_id}`    | Aggregate credits + hectares for a user  |

Interactive docs (Swagger UI) are available at `http://<laptop-ip>:8000/docs` while the
server is running — handy for poking at the API directly during the demo if you want to
show the schema off without the phone.

## Schema

See `schema.sql` — five tables (`community`, `user`, `species`, `project`,
`credit_transaction`) matching the ER design in `Assessment_6_Project_Proposal.pdf`.
`credit_transaction` is an append-only ledger (`MINT`/`REDEEM`), so credits minted for a
project are never overwritten, only added to.
