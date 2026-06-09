# ShadowAPI

ShadowAPI is a lightweight API proxy that automatically records responses from upstream APIs and serves cached responses when the upstream service becomes unavailable.

Built as a learning project focused on backend systems, caching, resilience, and API infrastructure.

---

## Features

### Reverse Proxy

Forward requests to an upstream API with zero changes required in the client application.

### Response Recording

Automatically stores successful API responses in a local SQLite database.

### Shadow Mode

When the upstream API becomes unavailable, ShadowAPI switches to Shadow Mode and serves previously cached responses.

### Route Discovery

Tracks and stores requested API routes for inspection and debugging.

### Dashboard Endpoints

Monitor cached routes and ShadowAPI status through built-in dashboard endpoints.

---

## Architecture

```text
Client
   │
   ▼
ShadowAPI
   │
   ├── Live Mode
   │      │
   │      ▼
   │  Upstream API
   │      │
   │      ▼
   │  Save Response
   │
   └── Shadow Mode
          │
          ▼
     SQLite Cache
          │
          ▼
     Cached Response
```

---

## Tech Stack

* FastAPI
* SQLAlchemy
* SQLite
* HTTPX
* Uvicorn

---

## Project Structure

```text
ShadowAPI/
│
├── app/
│   ├── core/
│   │   └── logger.py
│   │
│   ├── dashboard/
│   │   └── router.py
│   │
│   ├── proxy/
│   │   ├── router.py
│   │   ├── forwarder.py
│   │   └── shadow.py
│   │
│   ├── storage/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── crud.py
│   │
│   └── main.py
│
└── shadow.db
```

---

## Dashboard Endpoints

### Service Status

```http
GET /shadow/status
```

Example Response:

```json
{
  "service": "ShadowAPI",
  "status": "running"
}
```

### Cached Routes

```http
GET /shadow/routes
```

Returns all recorded routes stored in the cache.

### Statistics

```http
GET /shadow/stats
```

Returns ShadowAPI statistics and cache information.

---

## How It Works

### Live Mode

1. Request arrives.
2. ShadowAPI forwards request to upstream API.
3. Response is returned to client.
4. Response is stored in SQLite.

### Shadow Mode

1. Upstream API becomes unavailable.
2. ShadowAPI detects the failure.
3. Cached response is retrieved from SQLite.
4. Response is served to the client.

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/imramen07/ShadowAPI.git
cd ShadowAPI
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn app.main:app --reload
```

Server will start at:

```text
http://localhost:8000
```

---

## Roadmap

### v0.1

* Reverse Proxy
* SQLite Cache
* Shadow Fallback
* Dashboard Endpoints

### v0.2

* Metrics System
* Cache Hit/Miss Tracking
* TTL Expiration

### v0.3

* POST/PUT Support
* Stateful Mock Responses

### v1.0

* Intelligent API Shadowing
* Route Parameterization
* Automatic Schema Learning
* Advanced Failure Simulation

---

## Motivation

Modern applications depend heavily on third-party APIs and microservices. Development often comes to a halt when these services become unavailable.

ShadowAPI aims to reduce this dependency by learning API responses during normal operation and providing cached fallbacks when services fail.

---

## Author

**Ramen**

GitHub: https://github.com/imramen07
