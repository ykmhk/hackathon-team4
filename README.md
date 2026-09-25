# CS235 Music Library

A Flask web application for browsing and discovering music tracks. The application loads the supplied CSV data into an in-memory repository and provides browsing, search, authentication, reviews, ratings, and personal favourites.

## Team Members

| Name | GitHub username |
| --- | --- |
| Steven Wang | Whi3e |
| Meti Liu | meti-liu |
| Nuo Chen | NuoChen144 |
| Yufan | ykmhk |


## Features

- Browse all available tracks in alphabetical title order.
- Move through the track catalogue with pagination.
- Search by title, artist, album, or genre.
- View track information, including artist, album, genres, duration, and release year where available.
- Register, log in, and log out securely.
- Post ratings and reviews while logged in.
- View reviews and the average rating on a track's detail page.
- Add tracks to, view, and remove tracks from a personal favourites list.
- Switch between the available display themes.

## Project Structure

The application uses Flask blueprints and separates HTTP routes from service-layer business logic. Services access data through the abstract repository interface, which is implemented by the in-memory repository.

```text
music/
|-- adapters/          Repository interface, in-memory repository, and CSV loading
|-- authentication/    Registration, login, and logout
|-- domainmodel/       Music Library domain classes
|-- favourites/        Favourite-track routes and services
|-- home/              Home page
|-- reviews/           Review and rating routes and services
|-- static/            CSS and JavaScript
|-- templates/         Jinja templates
`-- tracks/            Browse, pagination, search, and track detail

tests/
|-- unit/
|-- integration/
`-- e2e/
```

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

## Running the Tests

With the virtual environment activated and from the project root, run the complete test suite:

```bash
python -m pytest -v tests
```

The test suite includes domain model, repository, service, route/integration, and end-to-end tests.

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

The supplied data files are modified excerpts from the Library of Congress collection and the Free Music Archive dataset:

- [Library of Congress collection](https://www.loc.gov/item/2018655052)
- [Free Music Archive on GitHub](https://github.com/mdeff/fma)

We acknowledge the following publications introducing the Free Music Archive dataset:

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A dataset for music analysis. In *Proceedings of the 18th International Society for Music Retrieval Conference*.

Defferrard, M., Mohanty, S., Carroll, X., & Salathe, M. (2018). Learning to recognize musical genre from audio. In *The Web Conference 2018 Companion*. ACM Press.
