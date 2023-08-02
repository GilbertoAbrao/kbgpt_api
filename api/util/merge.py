from pydantic import BaseModel as SchemaBaseModel
from core.database import Base



def merge_object_schema_to_object_model(obj_schema: SchemaBaseModel, obj_model: Base):
    """
    Merge attributes from schema pydantic to model sqlalchemy
    """

    for key, value in obj_schema.dict(exclude_unset=True).items():
        if value is not None:
            # trim if string
            if isinstance(value, str):
                setattr(obj_model, key, value.strip())
            else:
                setattr(obj_model, key, value)


def merge_object_models(model_from, model_to, ignore_none=True):

    for key, value in model_from.__dict__.items():
        if key[:1] != '_':
            if ignore_none:
                if value is not None:
                    setattr(model_to, key, value)
            else:
                setattr(model_to, key, value)