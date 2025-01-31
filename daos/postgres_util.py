import os
import asyncpg
from dotenv import load_dotenv
from typing import Any, List, Optional
from contextlib import asynccontextmanager


class PostgresClient:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        if not self.pool:
            load_dotenv()
            url = os.getenv("POSTGRES_URL")
            if not url:
                raise ValueError("POSTGRES_URL environment variable is not set.")
            pool_size = 2
            self.pool = await asyncpg.create_pool(
                url, statement_cache_size=0, min_size=1, max_size=pool_size
            )

    @asynccontextmanager
    async def get_connection(self):
        await self.init_pool()
        async with self.pool.acquire() as conn:
            yield conn

    async def fetch(self, query: str, *args) -> List[asyncpg.Record]:
        async with self.get_connection() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        async with self.get_connection() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args) -> Any:
        async with self.get_connection() as conn:
            return await conn.fetchval(query, *args)

    async def fetchall(self, query: str, *args) -> List[asyncpg.Record]:
        # Note: fetchall is an alias for fetch in asyncpg
        return await self.fetch(query, *args)

    async def execute(self, query: str, *args) -> str:
        async with self.get_connection() as conn:
            return await conn.execute(query, *args)

    async def close(self):
        if self.pool:
            await self.pool.close()