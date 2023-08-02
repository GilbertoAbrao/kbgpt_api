from sqlalchemy import BigInteger, Column, DateTime, String, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base


class FileModel(Base):
    __tablename__ = 'flient'

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    date_include: datetime = Column(DateTime, default=datetime.now)
    date_update: datetime = Column(DateTime, onupdate=datetime.now, default=datetime.now)
    name: str = Column(String(100), index=True)
    path: str = Column(String(200), index=True)
    size: int = Column(Integer)
