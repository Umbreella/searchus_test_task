from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.DocModel import DocModel
from schemas.DocSchema import DocSchemaOut
from services.async_database import get_db

router = APIRouter()


@router.get('/')
async def search_docs(
        search: str = '',
        db: AsyncSession = Depends(get_db),
) -> List[DocSchemaOut]:
    return await DocModel.elastic_search(search, db)
