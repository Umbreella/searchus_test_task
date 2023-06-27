import asyncio
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
        search_docs_orm = await tested_class.elastic_search('text', db)
        search_docs = parse_obj_as(List[DocSchemaOut], search_docs_orm)

    expected_docs = [2, 1, ]
    real_docs = [doc.id for doc in search_docs]

    assert expected_docs == real_docs


async def test_When_CallSearchWithManyData_Should_ReturnOnlyFirst20Docs(
        filling_many_docs,
):
    await asyncio.sleep(1)

    async with async_database.session() as db, db.begin():
        search_docs_orm = await tested_class.elastic_search('text', db)

    expected_len_docs = 20
    real_len_docs = len(search_docs_orm)

    assert expected_len_docs == real_len_docs
