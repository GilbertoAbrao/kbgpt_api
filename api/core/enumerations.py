from enum import Enum


class StatusAsyncEnum(str, Enum):

    def __str__(self):
        return str(self.value)

    processing = 'processing'
    done = 'done'
    error = 'error'
    canceled = 'cancelled'


class CrudActionEnum(str, Enum):

    def __str__(self):
        return str(self.value)
    
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'



class VectorDatabaseEnum(str, Enum):

    def __str__(self):
        return str(self.value)
    
    faiss = 'faiss'
    pinecone = 'pinecone'


class FilePlaceEnum(str, Enum):

    def __str__(self):
        return str(self.value)
    
    local = 'local'
    s3 = 's3'