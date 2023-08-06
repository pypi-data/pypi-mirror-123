from collections import (
    Mapping,
)
from typing import (
    NewType,
    Optional,
    Union,
)

import asyncpg
from django.db import (
    DEFAULT_DB_ALIAS,
    connections as django_connections,
)
from django.db.models import (
    Model,
)


ConnectionAlias = NewType('ConnectionAlias', str)
ConnectionInterface = Union[asyncpg.Pool, asyncpg.Connection]


connections: Mapping[ConnectionAlias, asyncpg.Pool] = {}


async def _make_connection(alias: ConnectionAlias) -> asyncpg.Pool:
    dj_connection = django_connections[alias]
    params = dj_connection.get_connection_params()
    return await asyncpg.create_pool(**params)


async def get_pool(alias: Optional[ConnectionAlias] = None) -> asyncpg.Pool:
    if alias is None:
        alias = DEFAULT_DB_ALIAS

    if alias not in connections:
        connections[alias] = await _make_connection(alias)

    connection = connections[alias]

    return connection


async def get_connection(alias: Optional[ConnectionAlias] = None) -> asyncpg.Connection:
    pool = await get_pool(alias)
    return pool.acquire()


async def truncate_table(conn: ConnectionInterface, model: Model):
    db_table = model._meta.db_table
    query = f'TRUNCATE TABLE {db_table} RESTART IDENTITY CASCADE'
    await conn.execute(query)


async def set_insert_index_enabled(conn: ConnectionInterface, model: Model, enabled: bool):
    db_table = model._meta.db_table
    query = f'''
        UPDATE pg_index
        SET indisready=$1
        WHERE indrelid = (
            SELECT oid
            FROM pg_class
            WHERE relname=$2
        ) AND NOT indisprimary;
    '''
    await conn.execute(query, enabled, db_table)

    if enabled:
        query = f'REINDEX TABLE {db_table}'
        await conn.execute(query)
