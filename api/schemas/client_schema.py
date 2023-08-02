from typing import Optional
from datetime import datetime
from pydantic import BaseModel as SchemaBaseModel, Field
        

class ClientSchemaRead(SchemaBaseModel):
    id: Optional[int]
    date_include: Optional[datetime]
    date_update: Optional[datetime]
    name: Optional[str]
    email: Optional[str]

    class Config:
        orm_mode = True


class ClientSchemaInsert(SchemaBaseModel):
    name: str = Field(..., max_length=200)
    email: str = Field(..., max_length=200)

    class Config:
        orm_mode = True


class ClientSchemaUpdate(SchemaBaseModel):
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=200)

    class Config:
        orm_mode = True
        