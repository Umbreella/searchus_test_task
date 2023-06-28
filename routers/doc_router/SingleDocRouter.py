from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.DocModel import DocModel
from services.async_database import get_db

router = APIRouter()


@router.delete('/{doc_id}/')
async def delete_doc(
        response: Response,
        doc_id: int,
        db: AsyncSession = Depends(get_db),
) -> Response:
    is_deleted = await DocModel.delete(doc_id, db)

    if not is_deleted:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        response.status_code = status.HTTP_204_NO_CONTENT

    return response
