import os
import shutil
from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, Request, File, UploadFile
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from core.enumerations import VectorDatabaseEnum

from schemas.qa_schema import QASchema, QASchemaResponse

from drivers.faiss_driver import faiss_qa
from drivers.pinecone_driver import pinecone_qa


router = APIRouter()

required_user_attribuites = []


@router.post('/faiss', response_model=QASchemaResponse, status_code=status.HTTP_200_OK, summary='QA against Faiss index')
async def post_obj(
                    request: Request, 
                    payload: QASchema, 
                    db: AsyncSession = Depends(get_session), 
                ):

    try:

        answer = await faiss_qa(index_name=payload.index_name, question=payload.question)
           
        return QASchemaResponse(
            answer=answer
        )

    except Exception as e:
        raise HTTPException(detail=str(
            e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.post('/pinecone', response_model=QASchemaResponse, status_code=status.HTTP_200_OK, summary='QA against Pinecone index')
async def post_obj(
                    request: Request, 
                    payload: QASchema, 
                    db: AsyncSession = Depends(get_session), 
                ):

    try:

        answer = await pinecone_qa(index_name=payload.index_name, question=payload.question)

        res = QASchemaResponse(
            answer=answer['result'],
            # source_documents=answer['source_documents']
        )

        return res 

    except Exception as e:
        raise HTTPException(detail=str(
            e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)