# Medical History Diary

A simple personal healthcare record management web application. Users store
each medical visit — date, diagnosis, prescription, and the doctor's
comments — as a single record, browse their history chronologically in a
sidebar, and search across it by keyword.

Built with Flask, following the same package layout as our music web app
project (blueprints per feature area, a domain model, and a repository
adapter behind the services layer).

## Project layout

```
medical_diary/
├── medical_diary/
│   ├── adapters/           # repository interface + in-memory implementation
│   ├── authentication/     # login / register / logout
│   ├── domainmodel/        # User, MedicalRecord
│   ├── home/                # landing page
│   ├── records/             # add / view / search medical records
│   ├── profile/              # personal + healthcare provider + GP info
│   ├── static/                # css/style.css, js/records.js
│   └── templates/
├── tests/
├── requirements.txt
└── wsgi.py
```

## Running it

```bash
python -m venv .venv
source .venv/bin/activate        # .venv\Scripts\activate on Windows
pip install -r requirements.txt
python wsgi.py
```

Then open http://127.0.0.1:5000 and log in with the seeded demo account:

- **username:** `demo`
- **password:** `demo1234`

The demo account already has five sample records so the sidebar, search, and
record view all have something to show immediately.

## Notes on data storage

The original brief allowed medical records to live in browser LocalStorage
for the hackathon MVP, since a full backend wasn't required. Here they're
kept in an in-memory repository on the Flask server instead (mirroring the
music web app's `MemoryRepository` pattern), so the same `AbstractRepository`
interface can later be swapped for a real database without touching the
`records`, `authentication`, or `profile` blueprints. Data resets whenever
the server restarts — that's expected for a demo.

## Running tests

```bash
pytest tests/
```

## What's implemented (MVP)

- [x] View medical records, ordered newest to oldest
- [x] Create and save new medical records (date, diagnosis, prescription, comments)
- [x] Live keyword search across date / diagnosis / prescription / comments
- [x] User profile: personal info, healthcare provider, GP details
- [x] Log in / register / log out
- [x] Black-and-white, minimalist, ledger-style UI matching the wireframe
