from datetime import datetime, timedelta

import pytest

from app.settings import settings
from models.DocModel import DocModel
from schemas.DocSchema import DocSchemaIn
from services.async_database import async_database
from services.async_elastic import async_elasticsearch


@pytest.fixture
async def clear_elasticsearch():
    await async_elasticsearch.options(**{
        'ignore_status': [400, 404, ],
    }).indices.delete(**{
        'index': settings.ELASTICSEARCH_DOCS_INDEX,
    })


@pytest.fixture
async def filling_docs(clear_elasticsearch):
    async with async_database.session() as db, db.begin():
        await DocModel.create(**{
            'data': DocSchemaIn(**{
                'text': 'text',
                'created_date': datetime.utcnow() - timedelta(days=2),
                'rubrics': [
                    'rubric',
                    'rubric',
                ],
            }),
            'db': db,
        })
        await DocModel.create(**{
            'data': DocSchemaIn(**{
                'text': 'text',
                'created_date': datetime.utcnow() - timedelta(days=1),
                'rubrics': [
                    'test_rubric',
                    'test_rubric',
                ],
            }),
            'db': db,
        })


@pytest.fixture
async def filling_many_docs(clear_elasticsearch):
    async with async_database.session() as db, db.begin():
        for _ in range(21):
            await DocModel.create(**{
                'data': DocSchemaIn(**{
                    'text': 'text',
                    'created_date': datetime.utcnow() - timedelta(days=2),
                    'rubrics': [
                        'rubric', 'rubric',
                    ],
                }),
                'db': db,
            })
