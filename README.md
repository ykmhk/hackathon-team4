# Starter Flask App Skeleton

This project is a neutral starter application scaffold. It keeps the Flask structure, blueprints, template layout, and repository pattern, but removes the music-specific naming so it is ready to be repurposed for any app idea.

## Features

- Flask app factory pattern
- Blueprint-based layout
- Basic auth flow with registration and login
- Simple in-memory repository pattern
- Neutral landing page and starter UI

## Project Structure

- `main/` contains the application package
- `config.py` holds environment configuration
- `wsgi.py` boots the app
- `requirements.txt` lists the Python dependencies

## Requirements

- Python 3
- The packages listed in `requirements.txt`

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Running the Application

```bash
flask run
```

Then open:

```text
http://127.0.0.1:5000
```

## Configuration

Set any environment variables you need in a local `.env` file, for example:

```dotenv
SECRET_KEY=replace-with-a-local-secret
WTF_CSRF_SECRET_KEY=replace-with-a-second-local-secret
```

## Customising This Skeleton

Replace the placeholder content in the templates, rename the domain model objects to fit your use case, and adapt the in-memory repository and routes as needed.
