import datetime
import json
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import noload
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel as SchemaBaseModel

from core.exceptions import ValidationException, RegisterNotFound
from core.configs import settings
from core.enumerations import CrudActionEnum
from core.database import Base

from util.merge import merge_object_models


class BasicCrudUseCase():

    model_name: Base = None

    def __init__(self, db: AsyncSession, user = None, auto_commit: bool = True, **kwargs):
        self.db = db
        self.user = user
        if self.model_name:
            self.obj_model: self.model_name = self.model_name()
        self.action = None
        self.auto_commit = auto_commit
        self.count_rows = 0


    async def before_validate(self, **kwargs):
        ...


    async def validate(self, **kwargs) -> str:
        ...

    async def prepair_data(self, **kwargs):
        ...

    async def delete_validate(self, **kwargs) -> str:
        ...

    async def before_create(self, **kwargs):
        ...

    async def after_create(self, **kwargs):
        ...

    async def before_update(self, **kwargs):
        ...

    async def after_update(self, **kwargs):
        ...

    async def before_delete(self, **kwargs):
        ...
    
    async def before_list(self, **kwargs):
        ...

    async def after_delete(self, **kwargs):
        ...

    async def after_search(self, **kwargs):
        ...

    async def after_list(self, **kwargs):
        ...


    async def get_one(self, **kwargs) -> Base | None:

        try:
            async with self.db as session:

                query = select(self.model_name)

                # apply filters that came as kwargs
                if not 'filters' in kwargs:
                    raise Exception('No filters provided')
                else:
                    for k in kwargs['filters']:
                        if k in self.model_name.__table__.columns.keys():
                            query = query.filter(getattr(self.model_name, k) == kwargs[k])
                

                # apply noload that came in kwargs
                if 'noload' in kwargs:
                    query = query.options(noload(kwargs['noload']))

                result = await session.execute(query)
                obj_result: self.model_name = result.scalars().first()
                self.obj_model: self.model_name = obj_result

                if not self.obj_model:
                    raise RegisterNotFound(f'Register not found in table {self.model_name.__tablename__}. Params: {kwargs}')
                
                await self.after_search(**kwargs)

                return self.obj_model
            
        except Exception as e:
            await self.exception_handling(e)
            

    async def save(self):
        """Save object in database"""

        async with self.db as session:
            session.add(self.obj_model)
            await session.commit()



    async def create(self, object: Base, **kwargs):
        
        try:
            self.action = CrudActionEnum.create

            # make sure that the object is the same type of the model
            if not isinstance(object, self.model_name):
                raise Exception(f'Object is not instance of {self.model_name.__name__}')

            # actions before validate
            await self.before_validate(object=object, **kwargs)

            # validate
            await self.validate(object=object, **kwargs)

            # prepair data before insert
            await self.prepair_data(object=object, **kwargs)

            # actions before create
            await self.before_create(object=object, **kwargs)

            self.obj_model = object

            # insert
            if self.auto_commit: 
                await self.save()
                
            # actions after create
            await self.after_create(**kwargs)

            return self.obj_model

        except Exception as e:
            await self.exception_handling(e)


    async def update(self,  object: Base, **kwargs):
        
        try:

            self.action = CrudActionEnum.update

            # make sure that the object is the same type of the model
            if not isinstance(object, self.model_name):
                raise Exception(f'Object is not instance of {self.model_name.__name__}')

            # check if object hasn't id
            if not object.id:
                raise Exception('Object has no id')
            
            # get object from database
            self.obj_model: self.model_name = await self.get_one(id=object.id)

            # if not found
            if not self.obj_model:
                raise RegisterNotFound(f'Register not found in table {self.model_name.__tablename__} with id {object.id}')

            # merge given object to object from database
            merge_object_models(object, self.obj_model)

            # actions before validate
            await self.before_validate(**kwargs)

            # validate
            await self.validate(**kwargs)

            # actions before update
            await self.before_update(object, **kwargs)


            # update
            if self.auto_commit:
                await self.save()


            # actions after update
            await self.after_update(object, **kwargs)

            return self.obj_model

        except Exception as e:
            await self.exception_handling(e)



    async def list(self, page_size: int = None, page_index: int = None, qry = None, *args, **kwargs):
        
        try:

            self.action = CrudActionEnum.List

            try:

                async with self.db as session:

                    # se foi passado uma query, usa ela
                    if not qry is None:

                        query = qry

                    # senao, monta uma query baseada no model e nos parametros enviados via kwargs
                    else:

                        query = select(self.model_name)
                        
                        # aplica filtros que vieram como kwargs
                        for k in kwargs:
                            if k in self.model_name.__table__.columns.keys() and kwargs[k] != None:
                                query = query.filter(getattr(self.model_name, k) == kwargs[k])
                    

                        # aplica noload que vier no kwargs
                        if 'noload' in kwargs:
                            query = query.options(noload(kwargs['noload']))

                        # ordena
                        query = query.order_by(self.model_name.Id)
                    
                    # aplica paginação
                    if page_index and page_size:

                        # calcula qtd total de registros
                        query_count = select(func.count()).select_from(query.subquery())
                        QtdeRegistros = await session.execute(query_count)
                        self.count_rows = QtdeRegistros.scalar()

                        query = query.offset((page_index - 1) * page_size)
                        query= query.limit(page_size) 


                        # QtdeRegistros = await session.execute(func.count(self.nome_model.Id))
                        # self.total_registros = QtdeRegistros.scalar()

                    result = await session.execute(query)

                    self.obj_model: List[self.model_name] = result.scalars().all()
                    
                    await self.after_list(**kwargs)

                    return self.obj_model
                
            
            except Exception as e:
                print(settings.DB_URL)
                print(str(e))

        except Exception as e:
            await self.exception_handling(e)




    async def delete(self, **kwargs):

        try: 

            self.action = CrudActionEnum.delete

            async with self.db as session:

                # se não existir um registro já carregado
                if self.obj_model is None or self.obj_model.id is None:
                    # tenta carregar a partir dos kwargs
                    self.obj_model: self.model_name = await self.get_one(**kwargs)
                
                    # se ainda assim não existir um registro carregado, levanta exceção
                    if self.obj_model is None or self.obj_model.id is None:
                        raise RegisterNotFound('Any record was provided')

                # valida exclusao
                erro_validacao = await self.delete_validate()
                if erro_validacao:
                    raise ValidationException(erro_validacao)

                # se não encontrou
                if not self.obj_model:
                    raise RegisterNotFound('Record not found')
                
                # açoes antes excluir
                await self.before_delete(self.obj_model)

                # exclui objetos que estiverem na lista de objetos relacionados a excluir
                for obj_relacionado_excluir in self.objetos_relacionados_excluir:
                    await session.delete(obj_relacionado_excluir)

                # exclui
                await session.delete(self.obj_model)
                await session.commit()

                # açoes após excluir
                await self.after_delete(self.obj_model)

        except Exception as e:
                    await self.exception_handling(e)



    async def exception_handling(self, e: Exception):
        raise e