from typing import Generic, TypeVar, Type

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select, SQLModel

ModelType = TypeVar("ModelType", bound=any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.Model = model
        self.session = session

    def get(self, id: any) -> ModelType | None:
        return self.session.exec(select(self.Model).where(self.Model.id == id)).first()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = {key: value for key, value in obj_in if value is not None}
        db_obj = self.Model(**obj_in_data)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, any]) -> ModelType:
        obj_data = jsonable_encoder(obj_in)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])  # can't set db_obj.field = field
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def remove(self, obj: ModelType) -> ModelType:
        self.session.delete(obj)
        self.session.commit()
        return obj
