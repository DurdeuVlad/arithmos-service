from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.math_ops import router as math_router
from app.utils.monitoring import start_metrics_server
from app.utils.cache import init_cache
from app.models.db import database

from sqlalchemy import create_engine
from app.models.db import DATABASE_URL, metadata

# Creează tabelele definite de metadata (dacă nu există deja)
sync_db_url = DATABASE_URL.replace("+aiosqlite", "")
engine = create_engine(
    sync_db_url,
    connect_args={"check_same_thread": False},
)
metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_metrics_server()
    init_cache()
    # ↑ tabelele sunt deja create aici
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="Arithmos Service",
    description="Microservice providing power, Fibonacci, and factorial operations",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes under /api
app.include_router(math_router, prefix="/api")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True
    )
