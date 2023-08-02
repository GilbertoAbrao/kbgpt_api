from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


async def get_session() -> Generator:
    
    session: AsyncSession = Session()

    session.autoflush = False

    try:
        yield session
    finally:
        await session.close()
