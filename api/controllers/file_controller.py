import os
import shutil
from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, Request, File, UploadFile
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from core.enumerations import VectorDatabaseEnum, FilePlaceEnum

from schemas.file_schema import FileSchemaRead, FileSchemaInsert, FileSchemaUpdate

from use_cases.ingestion_uc import ingestion_uc

from drivers.faiss_driver import faiss_pdf_ingestor
from drivers.pinecone_driver import pinecone_pdf_ingestor


router = APIRouter()

required_user_attribuites = []


@router.post("/faiss")
async def create_upload_file(file: UploadFile):
    
    upload_dir = os.path.join(os.getcwd(), "uploads")

    # create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)
    print(dest)

    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    r = await faiss_pdf_ingestor(dest)

    return r




@router.post("/pinecone")
async def create_upload_file(file: UploadFile, index_name: str = Query(..., min_length=1, max_length=50)):
    
    upload_dir = os.path.join(os.getcwd(), "uploads")

    # create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)

    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await ingestion_uc(file_path=dest, file_place=FilePlaceEnum.local, index_name=index_name, vector_store=VectorDatabaseEnum.pinecone)
