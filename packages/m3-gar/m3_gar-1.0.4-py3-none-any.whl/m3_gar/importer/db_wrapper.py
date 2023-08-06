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
    """
    Создаёт пул подключений asyncpg.Pool с теми же параметрами, что
    используются для создания подключения alias в django.
    Для внутреннего использования, используйте публичные интерфейсы
    get_pool и get_connection

    Args:
        alias: псевдоним БД в django

    Returns:
        пул подключений asyncpg.Pool

    """
    dj_connection = django_connections[alias]
    params = dj_connection.get_connection_params()
    return await asyncpg.create_pool(**params)


async def get_pool(alias: Optional[ConnectionAlias] = None) -> asyncpg.Pool:
    """
    Получение пула подключений asyncpg.Pool, аналогичного подключению
    alias в django

    Args:
        alias: псевдоним БД в django,
            если не передан - используется БД по-умолчанию

    Returns:
        пул подключений asyncpg.Pool

    """
    if alias is None:
        alias = DEFAULT_DB_ALIAS

    if alias not in connections:
        connections[alias] = await _make_connection(alias)

    connection = connections[alias]

    return connection


async def get_connection(alias: Optional[ConnectionAlias] = None) -> asyncpg.Connection:
    """
    Получение подключения asyncpg.Connection, аналогичного подключению
    alias в django

    Args:
        alias: псевдоним БД в django,
            если не передан - используется БД по-умолчанию

    Returns:
        подключение asyncpg.Connection

    """
    pool = await get_pool(alias)
    return pool.acquire()


async def truncate_table(conn: ConnectionInterface, model: Model):
    """
    Сброс данных из таблицы модели model

    Args:
        conn: asyncpg подключение к БД (asyncpg.Connection, либо asyncpg.Pool)
        model: django-модель

    """
    db_table = model._meta.db_table
    query = f'TRUNCATE TABLE {db_table} RESTART IDENTITY CASCADE'
    await conn.execute(query)
