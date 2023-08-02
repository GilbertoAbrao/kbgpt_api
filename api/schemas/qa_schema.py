from typing import Optional
from datetime import datetime
from pydantic import BaseModel as SchemaBaseModel, Field

from core.enumerations import VectorDatabaseEnum
        

class QASchema(SchemaBaseModel):
    index_name: str
    question: str = Field(..., max_length=1000)

    
    class Config:
        orm_mode = False



class QASchemaResponse(SchemaBaseModel):
    answer: str
    source_documents: Optional[list[str] | None]

    
    class Config:
        orm_mode = False
