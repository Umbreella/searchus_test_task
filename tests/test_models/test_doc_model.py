import asyncio
from datetime import datetime
from typing import List

from pydantic import parse_obj_as

from app.settings import settings
from models.DocModel import DocModel
from schemas.DocSchema import DocSchemaIn, DocSchemaOut
from services.async_database import async_database
from services.async_elastic import async_elasticsearch

tested_class = DocModel
data = {
    'text': 'text',
    'rubrics': [
        'rubric',
        'rubric',
    ],
}
date_format = '%H-%M %d-%m-%Y'


async def test_When_CallCreate_Should_CreateInPostgresAndInElastic(
        clear_elasticsearch,
):
    local_data = DocSchemaIn(**data)

    async with async_database.session() as db, db.begin():
        await tested_class.create(local_data, db)

    doc_in_elastic = await async_elasticsearch.options(**{
        'ignore_status': [400, 404, ],
    }).get(**{
        'id': 1,
        'index': settings.ELASTICSEARCH_DOCS_INDEX,
    })

    expected_source = {
        'text': 'text',
    }
    real_source = doc_in_elastic.body.get('_source')

    assert expected_source == real_source


async def test_When_CallDelete_Should_DeleteFromPostgresAndFromElastic(
        filling_docs,
):
    async with async_database.session() as db, db.begin():
        await tested_class.delete(1, db)

    doc_in_elastic = await async_elasticsearch.options(**{
        'ignore_status': [400, 404, ],
    }).get(**{
        'id': 1,
        'index': settings.ELASTICSEARCH_DOCS_INDEX,
    })

    expected_found = False
    real_found = doc_in_elastic.body.get('found')

    assert expected_found == real_found


async def test_When_CallSearchWithNotFoundIndex_Should_ReturnEmptyData(
        clear_elasticsearch,
):
    async with async_database.session() as db, db.begin():
        docs_orm = await tested_class.elastic_search('test_text', db)

    expected_docs_orm = []
    real_docs_orm = docs_orm

    assert expected_docs_orm == real_docs_orm


async def test_When_CallSearchWithNotFoundText_Should_ReturnEmptyData(
        filling_docs,
):
    await asyncio.sleep(1)

    async with async_database.session() as db, db.begin():
        docs_orm = await tested_class.elastic_search('search_text', db)

    expected_docs_orm = []
    real_docs_orm = docs_orm

    assert expected_docs_orm == real_docs_orm


async def test_When_CallSearchWithFoundText_Should_ReturnDataFromPostgres(
        filling_docs,
):
    await asyncio.sleep(1)

    async with async_database.session() as db, db.begin():
        search_docs_orm = await tested_class.elastic_search('test_text', db)
        search_docs = parse_obj_as(List[DocSchemaOut], search_docs_orm)

    expected_docs = {
        'id': 2,
        'text': 'test_text',
        'rubrics': [
            'test_rubric',
            'test_rubric',
        ],
    }
    real_docs = search_docs[0].dict()

    expected_created_date = datetime.utcnow().strftime(date_format)
    real_created_date = real_docs.pop('created_date').strftime(date_format)

    assert expected_docs == real_docs
    assert expected_created_date == real_created_date
