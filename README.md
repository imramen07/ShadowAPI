# ShadowAPI

A modern FastAPI boilerplate designed for building scalable and production-ready REST APIs with minimal setup.

---

## Features

* FastAPI-powered backend
* Modular project structure
* Structured logging
* Response caching support
* Middleware integration
* Environment-based configuration
* Clean architecture for easy maintenance
* Auto-generated API documentation
* Ready for deployment and future scaling

---

## Project Structure

```text
shadowapi/
├── app/
│   ├── core/
│   │    └── logger.py
│   ├── dash/
│   │    └── dash_router.py
│   ├── proxy/
│   │    ├── forwarder.py
│   │    ├── router.py
│   │    └── shadow.py
│   ├── storage/
│   │    ├── crud.py
│   │    ├── database.py
│   │    └── models.py
│   └── main.py
├── run.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/shadowapi.git
cd shadowapi
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates documentation:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## Logging

ShadowAPI includes structured logging to help monitor requests, errors, and application events during development and production.

---

## Caching

Caching support is included to improve response times and reduce unnecessary processing for frequently accessed endpoints.

---

## Why ShadowAPI?

ShadowAPI provides a solid foundation for backend development without forcing unnecessary complexity. It is ideal for learning FastAPI, building personal projects, hackathon applications, and production services.

---

## Author - Ramen
## GitHub - imramen07
