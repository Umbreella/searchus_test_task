from datetime import datetime

from elasticsearch import NotFoundError
from sqlalchemy import JSON, Column, DateTime, Integer, Text, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from schemas.DocSchema import DocSchemaIn
from services.async_database import BASE
from services.async_elastic import async_elasticsearch


class DocModel(BASE):
    __tablename__ = 'docs'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    rubrics = Column(JSON, nullable=True)

    @classmethod
    async def create(cls, data: DocSchemaIn, db: AsyncSession) -> None:
        query = insert(cls).values(
            data.dict()
        ).on_conflict_do_nothing().returning(cls)

        rows = await db.execute(query)
        result = rows.scalars().first()

        if result:
            await async_elasticsearch.index(**{
                'index': settings.ELASTICSEARCH_DOCS_INDEX,
                'id': result.id,
                'document': {
                    'text': result.text,
                },
            })

        return result

    @classmethod
    async def delete(cls, doc_id: int, db: AsyncSession) -> bool:
        query = delete(cls).where(
            cls.id == doc_id
        ).returning(cls)

        rows = await db.execute(query)
        result = rows.scalars().first()

        if result:
            await async_elasticsearch.delete(**{
                'id': result.id,
                'index': settings.ELASTICSEARCH_DOCS_INDEX,
            })

        return bool(result)

    @classmethod
    async def elastic_search(cls, search: str, db: AsyncSession):
        try:
            response = await async_elasticsearch.search(**{
                'index': settings.ELASTICSEARCH_DOCS_INDEX,
                'q': search,
                'size': 20,
            })
        except NotFoundError:
            return []

        search_ids = [
            int(item.get('_id')) for item in response.body['hits']['hits']
        ]

        query = select(cls).where(
            cls.id.in_(search_ids)
        ).order_by(cls.created_date.desc())

        rows = await db.execute(query)

        return rows.scalars().all()
