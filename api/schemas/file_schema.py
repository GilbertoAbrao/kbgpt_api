from typing import Optional
from datetime import datetime
from pydantic import BaseModel as SchemaBaseModel, Field
        

class FileSchemaRead(SchemaBaseModel):
    id: Optional[int]
    date_include: Optional[datetime]
    date_update: Optional[datetime]
    name: Optional[str]
    path: Optional[str]

    class Config:
        orm_mode = True


class FileSchemaInsert(SchemaBaseModel):
    name: str = Field(..., max_length=100)

    class Config:
        orm_mode = True


class FileSchemaUpdate(SchemaBaseModel):
    name: Optional[str] = Field(None, max_length=100)

    class Config:
        orm_mode = True
        