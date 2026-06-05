# 🧮 Arithmos Service

A production-grade FastAPI microservice delivering essential mathematical operations (**power**, **Fibonacci**, **factorial**) with built-in request logging, Redis-based caching, Prometheus monitoring (optional), and support for JWT authentication and asynchronous messaging (RabbitMQ/Kafka).

---

## 📂 Project Structure

```
arithmos-service/
├── app/
│   ├── main.py               # FastAPI app and router inclusion
│   ├── routers/
│   │   └── math_ops.py       # API endpoints
│   ├── services/
│   │   └── calculator.py     # Core logic: pow, fib, fact
│   ├── models/
│   │   ├── db.py             # Database connection (SQLite + SQLAlchemy/databases)
│   │   └── request_log.py    # ORM model for logging API calls
│   ├── schemas/
│   │   └── math.py           # Pydantic models
│   └── utils/
│       ├── cache.py          # fastapi-cache2 config
│       ├── monitoring.py     # Prometheus metrics setup (if enabled)
│       ├── auth.py           # JWT-based auth (optional)
│       └── logging.py        # Async message publishing (RabbitMQ/Kafka)
├── docker/
│   ├── Dockerfile            # Build definition
│   └── docker-compose.yml    # Service stack: API, Redis, RabbitMQ/Kafka
├── requirements.txt          # Dependencies
├── .flake8                   # Linting rules
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

* Docker (>= 20.x)
* Docker Compose v1.29+ or v2
* Windows PowerShell 5+ or Bash (macOS/Linux)

> 💡 **Windows users:** Docker must be running with **administrator privileges** to avoid engine connection errors.

### 1. Clone & Setup

```bash
git clone https://github.com/DurdeuVlad/arithmos-service.git
cd arithmos-service
python3 -m venv .venv
# Activate environment:
# PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update variables as needed. Default setup uses SQLite, Redis, and optionally RabbitMQ/Kafka via Docker.

### 4. Launch Services

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

* API: [http://localhost:8000](http://localhost:8000)
* Docs (Swagger/OpenAPI): [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Health Check

```powershell
Invoke-RestMethod -Uri http://localhost:8000/health -Method Get
```

Expected response:

```json
{ "status": "ok" }
```

---

## 📋 API Endpoints

| Method | Path           | Description                      |
| ------ | -------------- | -------------------------------- |
| POST   | /api/pow       | Compute base \*\* exp            |
| GET    | /api/fib/{n}   | Return the n-th Fibonacci number |
| GET    | /api/fact/{n}  | Return the factorial of n        |
| GET    | /api/logs      | Retrieve recent request logs     |

---

## ⚙️ Example Requests (PowerShell)

### Power (POST /pow)

```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/pow -Method Post -ContentType "application/json" -Body '{ "base": 2, "exp": 8 }'
```

Response:

```json
{ "result": 256.0 }
```

### Fibonacci (GET /fib/{n})

```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/fib/10 -Method Get
```

Response:

```json
{ "result": 55 }
```

### Factorial (GET /fact/{n})

```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/fact/5 -Method Get
```

Response:

```json
{ "result": 120 }
```

### View Logs (GET /logs)

```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/logs?limit=5 -Method Get
```

Sample Response:

```json
[
  {
    "id": 3,
    "endpoint": "fact",
    "params": { "n": 5 },
    "result": 120,
    "created_at": "2025-07-17T10:13:39.683296"
  },
  {
    "id": 2,
    "endpoint": "fib",
    "params": { "n": 10 },
    "result": 55,
    "created_at": "2025-07-17T10:13:35.416599"
  }
]
```

---

## 🔐 Authentication (JWT - Optional)

To enable JWT authentication:

1. Configure `.env`:

```env
JWT_SECRET=supersecretkey
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
```

2. Use `Depends(get_current_user)` to secure routes.
3. Issue tokens via a login route (to be implemented separately).

Useful for securing logs or extending service with user access control.

---

## 🐳 Docker Commands

```bash
# Build & launch full stack
docker compose -f docker/docker-compose.yml up -d --build

# Stop & clean up (preserves database volume)
docker compose -f docker/docker-compose.yml down

# Remove SQLite database
rm -rf data/arithmos.db
```

---
