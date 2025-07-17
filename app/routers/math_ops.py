from fastapi import APIRouter, HTTPException
from typing import Any
from datetime import datetime

from app.schemas.math import PowRequest, PowResponse, FibResponse, FactResponse
from app.services.calculator import power, fibonacci, factorial
from app.models.db import database
from app.models.request_log import request_logs
from app.utils.cache import cache

router = APIRouter(
    tags=["Math Operations"],
    responses={404: {"description": "Not found"}}
)

async def log_request(endpoint: str, params: dict, result: Any) -> None:
    """
    Persist the API call details into the database.
    """
    query = request_logs.insert().values(
        endpoint=endpoint,
        params=params,
        result=result,
        created_at=datetime.utcnow(),
    )
    await database.execute(query)

@router.post("/pow", response_model=PowResponse)
async def compute_pow(payload: PowRequest):
    result = power(payload.base, payload.exp)
    await log_request("pow", payload.dict(), result)
    return {"result": result}

@router.get("/fib/{n}", response_model=FibResponse)
@cache(expire=60)
async def compute_fib(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be non-negative")
    result = fibonacci(n)
    await log_request("fib", {"n": n}, result)
    return {"result": result}

@router.get("/fact/{n}", response_model=FactResponse)
@cache(expire=60)
async def compute_fact(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be non-negative")
    result = factorial(n)
    await log_request("fact", {"n": n}, result)
    return {"result": result}

@router.get("/logs")
async def get_logs(limit: int = 20):
    query = request_logs\
        .select()\
        .order_by(request_logs.c.created_at.desc())\
        .limit(limit)
    rows = await database.fetch_all(query)
    return [dict(r) for r in rows]
