# Cocktail API

A read-only REST API for browsing and searching a cocktail recipe dataset.

The application is built with FastAPI, uses PostgreSQL for storage, and returns validated JSON responses through Pydantic schemas.

The database is populated by a separate ETL pipeline that scrapes, normalizes, validates, and imports cocktail recipes.

## Features

- Paginated cocktail listing
- Cocktail search by cocktail name and ingredient text
- Detailed cocktail recipes with ordered ingredients
- Ingredient search with cocktail usage counts
- Dataset and parsing statistics
- Application and database health checks
- Validated request parameters and response schemas
- Sanitized `503 Service Unavailable` responses
- Automated API and service tests
- Dockerized application environment

## Dataset

The current PostgreSQL dataset contains:

- **6,614 cocktails**
- **30,761 ingredient rows**
- **5,619 fully parsed recipes**
- **995 partially parsed recipes**
- **0 failed recipes**
- **11 unresolved ingredient rows**
- **6,360 cocktails with images**
- **254 cocktails without images**

Dataset statistics are calculated directly from PostgreSQL and are available through:

```http
GET /stats
```

## Technology Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- psycopg 3
- Pydantic
- Uvicorn
- pytest
- HTTPX
- Docker

## Requirements

The API requires access to a populated PostgreSQL database containing the `cocktails` and `ingredients` tables.

The repository does not include database migrations or seed data. Database extraction, normalization, validation, and import are handled by a separate ETL project.

### Local development

- Python 3.12+
- Access to PostgreSQL

### Docker

- Docker Engine
- Access to PostgreSQL from the container

## Local Setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd cocktail_api
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the application and test dependencies:

```bash
python -m pip install -e ".[test]"
```

The project dependencies are defined in `pyproject.toml`.

Production dependencies can be installed without the test extras:

```bash
python -m pip install .
```

## Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure the PostgreSQL connection:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cocktails
DB_USER=postgres
DB_PASSWORD=your_password
```

The `.env` file is ignored by both Git and Docker build context. It must not be committed or copied into the Docker image.

The database may be:

- running locally;
- available through an SSH tunnel;
- running on a remote server;
- running on the same VPS as the deployed API.

## Running Locally

Start the FastAPI development server:

```bash
fastapi dev
```

The FastAPI CLI entrypoint is configured in `pyproject.toml`:

```toml
[tool.fastapi]
entrypoint = "app.main:app"
```

The application can also be started directly through Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

## Running with Docker

### Build the image

Build a versioned Docker image from the project root:

```bash
docker build -t cocktail-api:0.1.0 .
```

The Docker image contains:

- Python 3.12
- application source code
- production dependencies from `pyproject.toml`
- Uvicorn startup command

The image does not contain:

- `.env`
- database credentials
- local virtual environments
- Git history
- pytest cache
- test files

### Run with a directly accessible database

When `DB_HOST` contains a reachable database hostname or IP address:

```bash
docker run -d \
  --name cocktail-api \
  --env-file .env \
  -p 8000:8000 \
  cocktail-api:0.1.0
```

Port mapping:

```text
localhost:8000
        ↓
container:8000
        ↓
Uvicorn
        ↓
FastAPI
```

The API will be available at:

```text
http://localhost:8000
```

### Run with a local SSH tunnel on Linux

A common development setup is:

```text
FastAPI
    ↓
localhost:5432
    ↓
SSH tunnel
    ↓
PostgreSQL on VPS
```

Inside a regular Docker container, `localhost` refers to the container itself, not to the host machine.

When `.env` contains:

```dotenv
DB_HOST=localhost
DB_PORT=5432
```

and PostgreSQL is reached through an SSH tunnel opened on the Linux host, run the container with host networking:

```bash
docker run -d \
  --name cocktail-api \
  --network host \
  --env-file .env \
  cocktail-api:0.1.0
```

Port publishing with `-p` is not required when `--network host` is used.

The API remains available at:

```text
http://localhost:8000
```

### Verify the container

Check running containers:

```bash
docker ps
```

View application logs:

```bash
docker logs cocktail-api
```

Follow logs in real time:

```bash
docker logs -f cocktail-api
```

Check application health:

```bash
curl "http://localhost:8000/health"
```

Check database connectivity:

```bash
curl "http://localhost:8000/health/db"
```

Expected database health response:

```json
{
  "status": "ok",
  "database": "ok"
}
```

### Container lifecycle

Stop the container:

```bash
docker stop cocktail-api
```

Start the existing container again:

```bash
docker start cocktail-api
```

Remove the stopped container:

```bash
docker rm cocktail-api
```

Removing a container does not remove its image.

List local images:

```bash
docker image ls
```

After changing the application code, rebuild the image and recreate the container:

```bash
docker build -t cocktail-api:0.1.1 .

docker stop cocktail-api
docker rm cocktail-api

docker run -d \
  --name cocktail-api \
  --network host \
  --env-file .env \
  cocktail-api:0.1.1
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Check whether the application is running |
| `GET` | `/health/db` | Check the PostgreSQL connection |
| `GET` | `/cocktails` | List cocktails with pagination |
| `GET` | `/cocktails/search?q=gin` | Search cocktails by cocktail or ingredient text |
| `GET` | `/cocktails/{cocktail_id}` | Get a cocktail with its ingredients |
| `GET` | `/ingredients/search?q=gin` | Search normalized ingredient names and usage counts |
| `GET` | `/stats` | Get current dataset statistics |

## Pagination

The following endpoints support pagination:

```text
GET /cocktails
GET /cocktails/search
GET /ingredients/search
```

Available query parameters:

| Parameter | Description | Default | Limits |
| --- | --- | --- | --- |
| `page` | Page number | `1` | Minimum: `1` |
| `page_size` | Number of results per page | `20` | From `1` to `100` |

Example:

```bash
curl "http://127.0.0.1:8000/cocktails?page=2&page_size=5"
```

Paginated endpoints return a consistent response:

```json
{
  "items": [],
  "page": 2,
  "page_size": 5,
  "total": 6614,
  "total_pages": 1323
}
```

A page outside the available range is not treated as an error. It returns `200 OK` with an empty `items` array while preserving pagination metadata.

## Cocktail Search

Search cocktail names and ingredient text:

```bash
curl "http://127.0.0.1:8000/cocktails/search?q=gin&page=1&page_size=5"
```

Search is case-insensitive and uses partial matching against:

- `cocktails.name`
- `ingredients.name`
- `ingredients.raw`

Cocktail search requires at least three characters.

A whitespace-only query returns an empty paginated response without opening a database connection.

Example empty result:

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 0,
  "total_pages": 0
}
```

## Cocktail Detail

Retrieve one cocktail and its ordered ingredients:

```bash
curl "http://127.0.0.1:8000/cocktails/36843"
```

Example response:

```json
{
  "id": 36843,
  "name": "Gin Tonic",
  "description": "A simple highball cocktail.",
  "image_url": "https://example.com/gin-tonic.jpg",
  "glass": "Highball glass",
  "garnish": "Lime wedge",
  "method": "Build over ice",
  "parse_status": "ok",
  "source_url": "https://example.com/cocktails/36843",
  "ingredients": [
    {
      "id": 1,
      "position": 1,
      "raw": "50 ml gin",
      "amount": "50",
      "unit": "ml",
      "name": "Gin",
      "comment": null,
      "unresolved": false
    }
  ]
}
```

A missing cocktail returns:

```http
404 Not Found
```

```json
{
  "detail": "Cocktail not found"
}
```

## Ingredient Search

Search normalized ingredient names and return the number of cocktails that use each ingredient:

```bash
curl "http://127.0.0.1:8000/ingredients/search?q=gin&page=1&page_size=20"
```

Example response:

```json
{
  "items": [
    {
      "name": "Gin",
      "cocktail_count": 1160
    },
    {
      "name": "Old Tom gin",
      "cocktail_count": 85
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 32,
  "total_pages": 2
}
```

Ingredient search requires at least two characters.

Results are ordered by:

1. Cocktail usage count in descending order
2. Ingredient name in ascending order

The search currently uses partial matching. For example, `gin` may also match names such as `Ginger ale` or `Ginseng bitters`.

## Dataset Statistics

Retrieve current dataset statistics:

```bash
curl "http://127.0.0.1:8000/stats"
```

Example response:

```json
{
  "cocktails_total": 6614,
  "ingredients_total": 30761,
  "parse_status": {
    "ok": 5619,
    "partial": 995,
    "failed": 0
  },
  "unresolved_ingredients": 11,
  "images": {
    "with_image": 6360,
    "without_image": 254
  }
}
```

The values are calculated from the current PostgreSQL contents and are not hardcoded.

## Health Checks

Application health:

```bash
curl "http://127.0.0.1:8000/health"
```

Expected response:

```json
{
  "status": "ok"
}
```

Database health:

```bash
curl "http://127.0.0.1:8000/health/db"
```

Expected response:

```json
{
  "status": "ok",
  "database": "ok"
}
```

The application health endpoint does not depend on PostgreSQL. It remains available even when the database is offline.

## Error Handling

Invalid query and path parameters return:

```http
422 Unprocessable Entity
```

Missing cocktail detail resources return:

```http
404 Not Found
```

Empty list and search results return:

```http
200 OK
```

with an empty `items` array.

If PostgreSQL is unavailable, database-backed endpoints return:

```http
503 Service Unavailable
```

```json
{
  "detail": "Database unavailable"
}
```

Internal psycopg errors, connection parameters, and database credentials are not exposed in HTTP responses.

Full diagnostic information is written to the application logs.

## Architecture

Requests pass through separate application layers:

```text
HTTP request
    ↓
FastAPI router
    ↓
Service
    ↓
Repository
    ↓
PostgreSQL
    ↓
Pydantic response
    ↓
JSON
```

Responsibilities are separated as follows:

- **Routers** handle HTTP paths, query validation, response types, and status codes.
- **Services** handle pagination, input normalization, model construction, and application logic.
- **Repositories** contain SQL queries and return database rows.
- **Schemas** define validated API response contracts.
- **Database infrastructure** manages connections and translates availability failures into application exceptions.

## Project Structure

```text
cocktail_api/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application and exception handlers
│   ├── config.py                # Environment-based database configuration
│   ├── exceptions.py            # Application-specific exceptions
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py        # PostgreSQL connection management
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── cocktail_repository.py
│   │   ├── ingredient_repository.py
│   │   └── stats_repository.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── cocktails.py
│   │   ├── ingredients.py
│   │   └── stats.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── cocktail.py
│   │   ├── ingredient.py
│   │   └── stats.py
│   └── services/
│       ├── __init__.py
│       ├── cocktail_service.py
│       ├── ingredient_service.py
│       └── stats_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared pytest fixtures
│   ├── services/                # Service unit tests
│   └── test_*.py                # HTTP contract and error-handling tests
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Tests

Run the complete test suite:

```bash
pytest -q
```

The project currently includes **56 automated tests** covering:

- Application health
- Query and path validation
- Pagination contracts
- Cocktail listing and search
- Cocktail detail responses
- Ingredient search
- Dataset statistics
- Empty search results
- Whitespace normalization
- Missing resources
- Database availability failures
- Sanitized error responses
- Service-layer logic

The current test suite does not require a live PostgreSQL instance.

Database-dependent behavior is isolated with pytest fixtures and monkeypatching, so tests do not read from or modify the production database.

Repository integration tests against a dedicated test PostgreSQL instance are planned for a later stage.

## Docker Status

The API has been successfully:

- packaged through `pyproject.toml`;
- built as a Docker image;
- started as a Docker container;
- configured through an external `.env` file;
- connected to PostgreSQL through an SSH tunnel;
- verified through `/health`, `/health/db`, `/cocktails`, and `/stats`.

## Current Limitations

- Read-only API
- No database migrations
- No seed data
- No authentication or authorization
- No write endpoints
- No repository integration tests
- No CI workflow
- No public production deployment yet

## Roadmap

- Deploy the Dockerized API to a VPS
- Configure production container restart policy
- Add reverse proxy and HTTPS
- Add repository integration tests
- Add GitHub Actions CI
- Move the Telegram bot from direct PostgreSQL access to HTTP API calls
- Add semantic search with pgvector
- Add a retrieval-augmented `/ask` endpoint