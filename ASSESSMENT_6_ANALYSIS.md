# Assessment 6 — Supporting Analysis

**Course:** BCSE302P – Database Systems Lab
**Repository:** Blue-Ledger (Android / Kotlin / Jetpack Compose)
**Deliverable this analysis supports:** `Assessment_6_Project_Proposal.pdf`

This file is the working analysis behind the submitted PDF. It exists so the reasoning — what was
found in the actual codebase, what gap that creates, and what change closes it — is auditable
without having to re-derive it from the PDF's prose. **No source file under `app/` was modified as
part of this task.** Everything below is a proposal.

---

## 1. What the repository actually is today

BlueLedger is a working, single-module Android app (`applicationId
com.example.blueledger`, Kotlin 2.0, Jetpack Compose, min SDK 24 / target SDK 36). It has no
backend and no real database, despite `Room` being declared as a Gradle dependency.

**Implemented and working:**
- Splash → onboarding → login/signup → 4-tab home (Dashboard, Upload, Wallet, Profile) Compose UI
  (`ui/screens/**`, `ui/theme/**`).
- Jetpack Navigation graph (`navigation/AppNavGraph.kt`, `NavRoutes.kt`).
- GPS capture via `FusedLocationProviderClient` (`util/LocationHelper.kt`).
- Image picker for plot photo evidence (`ui/screens/home/tabs.kt`, `UploadTab`).
- A deterministic carbon-credit formula: species base rate × hectares × area bonus multiplier
  (`data/repo/Repositories.kt`, `mockMintCreditsForSpecies()`).
- Local persistence via Android Preferences DataStore, with the *entire* user object and the
  *entire* uploads list each serialized to one JSON string via Gson
  (`data/local/DataStoreManager.kt`, `data/repo/Repositories.kt`).

**Explicitly not implemented (per the project's own README "Known Limitations & TODOs"):**
- Real backend/auth (login accepts any non-empty credentials).
- A database (Room is declared in `app/build.gradle.kts` — `androidx.room.runtime`,
  `androidx.room.ktx` — but zero `@Entity`/`@Dao`/`@Database` classes exist anywhere in the
  source tree).
- Credit redemption ("Sell Credits" button in `WalletTab` is a no-op TODO).
- Any verification/approval step before credits are minted.

## 2. Identified DBMS gaps (why this repo needs Part 2 of this task)

| # | Gap | Evidence | Consequence |
|---|-----|----------|-------------|
| 1 | No relational structure | `DataStoreManager.kt:29-34` — two string preference keys (`user_json`, `uploads_json`) hold whole serialized objects | Cannot query, filter, or index; every read means full deserialization |
| 2 | Non-atomic read-then-write | `Repositories.kt:83-97`, `ProjectsRepository.addUpload()` reads the full list, appends in memory, writes the full list back with no lock/transaction | Concurrent uploads can race and silently drop each other's data |
| 3 | Business rule hardcoded in logic, not data | `Repositories.kt:100-111`, `mockMintCreditsForSpecies()` — species→rate mapping is a `when` block | Adding/correcting a rate needs a new APK build; no historical record of the rate in effect at mint time |
| 4 | No audit trail | `data/model/Models.kt` — `UploadProject.mintedCredits` is a single field baked in at upload time | No ledger; "Sell Credits" cannot be built safely without double-spend risk |
| 5 | No real user table / auth | `Repositories.kt:31-36`, `AuthRepository.login()` — mock accepts any non-empty credentials, one user blob per device | No credential verification, no multi-account support, no attribution of a plot to a verified person |
| 6 | Dashboard stat with no backing data | `ui/screens/home/tabs.kt:48`, `DashboardTab(totalCommunities: Int, ...)` | "Total communities enrolled" is passed in from outside with nothing populating it — there is no Community concept anywhere in the data layer |

## 3. Recommended database technology

**SQLite via the Android Room Persistence Library** (embedded relational database).

Justification (full detail in PDF §7): the app is offline-first by design (README says so
explicitly), the data is a shallow one-to-many relational shape (User→Project→CreditTransaction,
Species→Project), Room is *already* a declared but unused dependency (least-restructuring path),
and Room's Flow-returning DAOs are a drop-in match for the app's existing
`StateFlow`/`stateIn(...)` architecture in `ui/viewmodel/ViewModels.kt`. A cloud document store was
considered and rejected for now (adds a network dependency the offline-first product doesn't have)
but flagged as a reasonable Phase-2 addition once multi-device sync is actually needed.

## 4. Proposed entities and relationships

Five tables, all one-to-many relationships, surrogate integer primary keys:

```
COMMUNITY (1) ──enrolls──< (M) USER
USER      (1) ──uploads──< (M) PROJECT
SPECIES   (1) ──classified as──< (M) PROJECT
PROJECT   (1) ──generates──< (M) CREDIT_TRANSACTION
USER      (1) ──owns──< (M) CREDIT_TRANSACTION
```

- **COMMUNITY** — new entity; backs the currently-unsupported "total communities enrolled" stat.
- **USER** — evolves `data/model/Models.kt:User`; adds `password_hash`, `community_id` FK.
- **SPECIES** — new reference table; externalizes the hardcoded rate table.
- **PROJECT** — evolves `data/model/Models.kt:UploadProject`; `species` free-text becomes a
  validated FK; adds a `status` column (PENDING/VERIFIED/REJECTED).
- **CREDIT_TRANSACTION** — new append-only ledger; replaces the single `mintedCredits` field with
  auditable MINT/REDEEM rows.

Full attribute lists, data types, constraints, SQL DDL, and the ER diagram are in
`Assessment_6_Project_Proposal.pdf`, §8.

## 5. Files/modules that would need to change to actually implement this

| File / module | Change required | Priority |
|---|---|---|
| `app/build.gradle.kts` | Confirm/add the Room annotation processor (KSP or kapt) — the runtime/ktx artifacts are already present | **High** |
| `data/model/Models.kt` | Replace `User`, `UploadProject`, `WalletSummary` with Room `@Entity` classes for User, Community, Species, Project, CreditTransaction | **High** |
| *(new)* `data/local/entities/*.kt` or same file | Define the five `@Entity` classes with the PK/FK/CHECK constraints from PDF §8.D | **High** |
| *(new)* `data/local/dao/*Dao.kt` | `UserDao`, `ProjectDao`, `SpeciesDao`, `CommunityDao`, `CreditTransactionDao` — Flow-returning queries mirroring today's repository methods | **High** |
| *(new)* `data/local/BlueLedgerDatabase.kt` | Room `@Database` class wiring the five entities + DAOs; seed `Species` rows (Rhizophora/Avicennia/Bruguiera) on creation | **High** |
| `data/repo/Repositories.kt` | Rewrite `AuthRepository`/`ProjectsRepository` internals to call DAOs instead of Gson/DataStore JSON, **keeping existing public method signatures** so downstream code doesn't change | **High** |
| `data/local/DataStoreManager.kt` | Trim to only what DataStore is still good at (e.g. `remember_me`, `language` preference); remove `user_json`/`uploads_json` keys once migrated | **Medium** |
| `ui/screens/home/tabs.kt` (`UploadTab`) | Replace the hardcoded `speciesList` with a live query against the Species table | **Medium** |
| `ui/viewmodel/ViewModels.kt` | No signature changes expected; verify Flow types still line up after the repository rewrite | **Low** (verification only) |
| App-level: verifier/admin UI | Net-new screen to transition `Project.status`; not required for Assessment 6 | **Low / Future** |
| Credit redemption ("Sell Credits") | Wire the existing TODO button to insert REDEEM rows | **Low / Future** |

## 6. Implementation roadmap (priority-ordered)

1. **High** — Add Room annotation processor; define the five entities and DAOs; stand up
   `BlueLedgerDatabase` with seeded `Species` data.
2. **High** — Migrate `AuthRepository` and `ProjectsRepository` to Room, preserving their existing
   method signatures and Flow-based API so the ViewModel/UI layers need no changes.
3. **Medium** — Point `UploadTab`'s species dropdown at the live `Species` table instead of the
   hardcoded list; remove the now-redundant `mockMintCreditsForSpecies()` rate table (keep only the
   area-bonus multiplier logic, since the per-hectare rate now comes from the DB).
4. **Medium** — Retire the `user_json`/`uploads_json` DataStore keys once Room is verified working;
   keep DataStore only for lightweight preferences (remember-me, language).
5. **Low / Future** — Verifier role + review screen for `Project.status`; credit-redemption flow
   using `CreditTransaction(txn_type='REDEEM')`; cloud sync layer if multi-device access is ever
   required.

## 7. Deliverables produced by this task

- `Assessment_6_Project_Proposal.pdf` — the fully designed, submission-ready PDF (cover, TOC, all
  9 required sections, plus the additional-value appendices). Written for a faculty reader: no
  file paths, line numbers, or internal code identifiers appear in the body text.
- `Assessment_6_Project_Proposal.docx` — an **editable** Word version of the same document (same
  content, same two figures), so the student can review, annotate, and adjust wording before
  submission. Its Table of Contents is a live Word field — right-click it and choose "Update
  Field" (or press F9) after opening.
- `docs/assessment6/generate_pdf.py` — the script that generates the PDF, including the vector ER
  diagram (crow's-foot notation) and system-architecture diagram (editable source — re-run with
  `python docs/assessment6/generate_pdf.py` after any edits).
- `docs/assessment6/generate_docx.py` — the script that generates the Word version; imports the
  diagram-drawing functions from `generate_pdf.py` and re-exports them as PNGs
  (`docs/assessment6/assets/`) for embedding. Re-run both generator scripts together if the
  diagrams or entities change, so the PDF and Word versions stay in sync.
- `docs/assessment6/assets/` — the exported `er_diagram.png` and `architecture_diagram.png` used
  by the Word version.
- `ASSESSMENT_6_ANALYSIS.md` — this file (internal engineering analysis; not for submission).
