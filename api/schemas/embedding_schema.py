from typing import Optional
from datetime import datetime
from pydantic import BaseModel as SchemaBaseModel, Field
        

class EmbeddingFromS3Schema(SchemaBaseModel):
    file_path: Optional[str]
    index_name: Optional[str]
    callback_url: Optional[str]

    class Config:
        orm_mode = True

