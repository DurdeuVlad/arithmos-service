# 📦 Alembic Migrations Setup

Pentru a adăuga suport de migraţii a schemei de bazei de date, vom folosi **Alembic**. Iată paşii şi fişierele necesare:

---

## 1. Structura directoare

```
arithmos-service/
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 0001_initial_request_logs.py
```

---

## 2. Fișierul `alembic.ini` (în rădăcina proiectului)

```ini
[alembic]
script_location = alembic
sqlalchemy.url = sqlite+aiosqlite:///./app.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s] %(message)s
```

---

## 3. Fișierul `alembic/env.py`

```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# adăugăm path-ul proiectului
import os, sys
sys.path.append(os.getcwd())

from app.models.db import metadata  # metadata definit în models/db.py

def run_migrations_online():
    config = context.config
    fileConfig(config.config_file_name)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise NotImplementedError("Offline mode not supported")
else:
    run_migrations_online()
```

---

## 4. Prima migrație: `alembic/versions/0001_initial_request_logs.py`

```python
"""create initial request_logs table

Revision ID: 0001_initial_request_logs
Revises:
Create Date: 2025-07-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'request_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('endpoint', sa.String, nullable=False),
        sa.Column('params', sa.JSON, nullable=False),
        sa.Column('result', sa.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('request_logs')
```

---

## 5. Cum rulezi migrațiile

În proiect:

```bash
# generează folder alembic și inițializează (o singură dată)
alembic init alembic

# aplică migrațiile la baza de date locală
alembic upgrade head
```

După acestea, tabela `request_logs` va exista în `app.db`, iar viitoarele modificări de schemă pot fi gestionate cu Alembic.
