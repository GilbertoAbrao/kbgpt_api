from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, Request
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session

from schemas.client_schema import ClientSchemaRead, ClientSchemaInsert, ClientSchemaUpdate

from models.client_model import ClientModel

from use_cases.client_uc import ClientUseCase


router = APIRouter()

required_user_attribuites = []


# INSERT
@router.post('', response_model=ClientSchemaRead, status_code=status.HTTP_200_OK, summary='Create new Client')
async def post_obj(
                    request: Request, 
                    payload: ClientSchemaInsert, 
                    db: AsyncSession = Depends(get_session), 
                ):

    try:

        obj_model: ClientModel = ClientModel(**payload.dict())

        uc = ClientUseCase(db=db, user="")

        await uc.create(object=obj_model)



    except Exception as e:
        raise HTTPException(detail=str(
            e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
