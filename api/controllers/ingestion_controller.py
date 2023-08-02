import os
import shutil
from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, Request, File, UploadFile
from fastapi import BackgroundTasks
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from core.enumerations import VectorDatabaseEnum, FilePlaceEnum

from schemas.embedding_schema import EmbeddingFromS3Schema

from drivers.pinecone_driver import pinecone_pdf_ingestor

from use_cases.ingestion_uc import ingestion_uc


router = APIRouter()

required_user_attribuites = []
    


@router.post('/pinecone', status_code=status.HTTP_200_OK, summary='Ingestion files into a Pinecone vectore store')
async def post_obj(
                    payload: List[EmbeddingFromS3Schema], 
                    background_tasks: BackgroundTasks,
                    db: AsyncSession = Depends(get_session), 
                ):

    try:
        
        for f in payload:
            # await ingestion_uc(file_path=p.file_path, file_place=FilePlaceEnum.s3, index_name=p.index_name, vector_store=VectorDatabaseEnum.pinecone)
            background_tasks.add_task(ingestion_uc, file_path=f.file_path, file_place=FilePlaceEnum.s3, index_name=f.index_name, vector_store=VectorDatabaseEnum.pinecone, callback_url=f.callback_url)

    except Exception as e:
        raise HTTPException(detail=str(
            e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)