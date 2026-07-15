from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import Base

ModelT = TypeVar("ModelT", bound=Base)


class Repository(Generic[ModelT]):
    def __init__(self, db: Session, model: type[ModelT]):
        self.db = db
        self.model = model

    def list(self, limit: int = 50, offset: int = 0) -> list[ModelT]:
        return list(self.db.scalars(select(self.model).limit(limit).offset(offset)))

    def add(self, instance: ModelT) -> ModelT:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
