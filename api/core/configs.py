from pydantic import BaseSettings
import os

enviroment = os.getenv("APP_ENVIRONMENT", "")


class Settings(BaseSettings):

    URL = ""
    DB_URL = ""

    OPENAI_API_KEY = ""

    PINECONE_API_KEY = ""
    PINECONE_ENVIRONMENT = ""

    AWS_ACCESS_KEY_ID=""
    AWS_SECRET_ACCESS_KEY=""
    AWS_S3_BUCKET_NAME=""
    AWS_S3_SIGNATURE_VERSION=""
    AWS_S3_REGION_NAME=""

    LOCAL_TEMP_FOLDER = ""


    class Config:
        env_file = [f"{enviroment}.env"]
        case_sensitive = True


settings: Settings = Settings()
