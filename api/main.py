from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import client_controller, file_controller, qa_controller, ingestion_controller


app = FastAPI(title="Knowledge GPT API",
    description="API of knowledge data base powered by GPT technologie",
    version="1.0.0",
    )


origins = [    
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8081",
    "https://kbgpt.ai"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(client_controller.router, prefix='/client', tags=['Clients'])
app.include_router(file_controller.router, prefix='/file', tags=['File'])
app.include_router(ingestion_controller.router, prefix='/ingestion', tags=['Ingestion'])
app.include_router(qa_controller.router, prefix='/qa', tags=['Quenstion Answering'])
