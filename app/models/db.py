import os
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/arithmos.db")

database = Database(DATABASE_URL)

metadata = MetaData()
Base = declarative_base(metadata=metadata)
