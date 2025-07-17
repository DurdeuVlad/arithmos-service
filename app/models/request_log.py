from sqlalchemy import Table, Column, Integer, String, JSON, DateTime
from app.models.db import metadata

request_logs = Table(
    "request_logs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("endpoint", String, nullable=False),
    Column("params", JSON, nullable=False),
    Column("result", JSON, nullable=False),
    Column("created_at", DateTime, nullable=False),
)
