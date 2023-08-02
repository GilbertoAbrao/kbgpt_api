import datetime
import json
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import noload
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel as SchemaBaseModel

from core.configs import settings
from core.database import Base
from core.exceptions import RegisterNotFound, ValidationException
from core.enumerations import CrudActionEnum

from models.client_model import ClientModel

from use_cases.__crudbase_uc import BasicCrudUseCase


class ClientUseCase(BasicCrudUseCase):

    model_name = ClientModel


    async def before_validation(self, object: SchemaBaseModel, **kwargs):
        
        if self.action == CrudActionEnum.create:
            ...
           

    async def validate(self, object: SchemaBaseModel, **kwargs) -> str:

        if self.action == CrudActionEnum.create:
            ...
    

 


