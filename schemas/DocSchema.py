from datetime import datetime
from typing import List

from pydantic import BaseModel


class DocSchemaIn(BaseModel):
    text: str
    created_date: datetime | datetime = datetime.utcnow()
    rubrics: List[str]


class DocSchemaOut(BaseModel):
    id: int
    text: str
    created_date: datetime
    rubrics: List[str]

    class Config:
        orm_mode = True
