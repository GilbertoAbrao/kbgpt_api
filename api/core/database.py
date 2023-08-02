from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.configs import settings
from sqlalchemy.ext.asyncio import AsyncEngine

Base = declarative_base()


# class AsyncDatabaseSession:
#     def __init__(self):
#         self._session = None
#         self._engine = None
# 
#     def __getattr__(self, name):
#             return getattr(self._session, name)
# 
#     def init(self):
#             self._engine = create_async_engine(
#                 settings.DB_URL,                
#                 future=True,
#                 echo=True,
#             )
#             self._session = sessionmaker(
#                 self._engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession
#             )()
#     async def create_all(self):
#             async with self._engine.begin() as conn:
#                 await conn.run_sync(Base.metadata.create_all)
# 
# db=AsyncDatabaseSession()


engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)