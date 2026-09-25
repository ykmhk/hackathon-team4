# 

A Flask web application for browsing and discovering music tracks. The application loads the supplied CSV data into an in-memory repository and provides browsing, search, authentication, reviews, ratings, and personal favourites.

## Features

## Project Structure

## Requirements

- Python 3
- The packages listed in `requirements.txt`

## Installation

Clone or download the repository, open a terminal in the project root, and create a virtual environment.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Open the new `.env` file and replace both placeholder secrets with private random values:

```dotenv
SECRET_KEY=replace-with-a-local-secret
WTF_CSRF_SECRET_KEY=replace-with-a-second-local-secret
```

Do not commit `.env`. The supplied `.env.example` documents the required variables without containing real secrets.

## Running the Application

With the virtual environment activated and from the project root, run:

```bash
flask run
```

Then open the address displayed by Flask, normally:

```text
http://127.0.0.1:5000
```

The application loads the supplied album and track CSV files into the in-memory repository during startup.

## Configuration

The root-level `.env` file supplies the application configuration:

| Variable | Purpose |
| --- | --- |
| `FLASK_APP` | Flask entry point; keep this as `wsgi.py`. |
| `FLASK_DEBUG` | Enables Flask debug mode for local development. |
| `SECRET_KEY` | Signs session cookies and protects session data. |
| `TESTING` | Set to `False` when running the application normally. |
| `WTF_CSRF_SECRET_KEY` | Protects Flask-WTF forms with CSRF tokens. |

## Data Sources

