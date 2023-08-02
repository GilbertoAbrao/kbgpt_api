from sqlalchemy import BigInteger, Column, DateTime, String, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base


class ClientModel(Base):
    __tablename__ = 'client'

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    date_include: datetime = Column(DateTime, default=datetime.now)
    date_update: datetime = Column(DateTime, onupdate=datetime.now, default=datetime.now)
    name: str = Column(String(200), index=True)
    email: str = Column(String(200), index=True)
