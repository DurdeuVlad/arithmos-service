# arithmos-service

A simple, production-ready microservice in FastAPI providing mathematical operations (power, Fibonacci, factorial) with request logging, caching, monitoring, and optional authentication and messaging.

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
│   │   ├── db.py             # Database connection (SQLite via SQLAlchemy & databases)
│   │   └── request_log.py    # ORM model for persisting requests
│   ├── schemas/
│   │   └── math.py           # Pydantic models for request/response
│   └── utils/
│       ├── cache.py          # fastapi-cache2 configuration
│       ├── monitoring.py     # Prometheus metrics setup
│       ├── auth.py           # JWT-based authentication
│       └── logging.py        # Async message publishing (RabbitMQ/Kafka)
├── docker/
│   ├── Dockerfile            # Container definition
│   └── docker-compose.yml    # API + Redis/RabbitMQ/Kafka stack
├── requirements.txt          # Python dependencies
├── .flake8                   # Linting rules
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

* **Docker** (>= 20.x)
* **Docker Compose** (>= 1.29) or **Docker Compose v2**
* **Windows PowerShell** (version 5+)

### 1. Clone & Activate

```bash
git clone https://github.com/your-org/arithmos-service.git
cd arithmos-service
python3 -m venv .venv
```

```powershell
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure

Copy `.env.example` to `.env` and adjust variables as needed. By default, the local setup uses SQLite and Docker containers for Redis, RabbitMQ, and Kafka.

### 4. Start the Stack

```bash
# Rebuild and start all services in detached mode
docker-compose up --build -d
```

* **API**: `http://localhost:8000`
* **Metrics**: `http://localhost:8001/metrics`

### 5. Health Check

```powershell
Invoke-RestMethod \
  -Uri http://localhost:8000/health \
  -Method Get
```

Expected response:

```json
{
  "status": "ok"
}
```

## 📝 API Endpoints

| Method | Path        | Description                      |
| ------ | ----------- | -------------------------------- |
| POST   | `/pow`      | Compute `base ** exp`            |
| GET    | `/fib/{n}`  | Return the n-th Fibonacci number |
| GET    | `/fact/{n}` | Return the factorial of n        |
| GET    | `/logs`     | Retrieve recent request logs     |

Explore Swagger UI and OpenAPI schema at:

```bash
http://localhost:8000/docs
```

## 🔧 Test Requests via PowerShell

1. **Power (POST /pow)**

```powershell
Invoke-RestMethod \
  -Uri http://localhost:8000/api/pow \
  -Method Post \
  -ContentType "application/json" \
  -Body '{ "base": 2, "exp": 8 }'
```

**Response:**

```json
{ "result": 256.0 }
```

2. **Fibonacci (GET /fib/{n})**

```powershell
Invoke-RestMethod \
  -Uri http://localhost:8000/api/fib/10 \
  -Method Get
```

**Response:**

```json
{ "result": 55 }
```

3. **Factorial (GET /fact/{n})**

```powershell
Invoke-RestMethod \
  -Uri http://localhost:8000/api/fact/5 \
  -Method Get
```

**Response:**

```json
{ "result": 120 }
```

4. **View Logs (GET /logs)**

```powershell
Invoke-RestMethod \
  -Uri http://localhost:8000/api/logs?limit=5 \
  -Method Get
```

**Sample Response:**

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

## 🐳 Docker

```bash
# Build & Run Full Stack
docker-compose up --build
```

```bash
# Stop & Clean Up (preserves the SQLite volume)
docker-compose down
```

```bash
# Remove Database
rm -rf data/arithmos.db
```
