from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from .models import Base

T = TypeVar("T", bound=Base)

class Repository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get(self, id: Any) -> Optional[T]:
        return self.db.get(self.model, id)

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, obj_in: T) -> T:
        self.db.add(obj_in)
        self.db.commit()
        self.db.refresh(obj_in)
        return obj_in

    def update(self, db_obj: T, obj_in: dict) -> T:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: Any) -> Optional[T]:
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
