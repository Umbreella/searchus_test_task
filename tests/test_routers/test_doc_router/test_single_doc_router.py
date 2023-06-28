from fastapi import status
from sqlalchemy import select

from models.DocModel import DocModel
from services.async_database import async_database

url = '/api/documentation/'


async def test_When_GetForSingleDoc_Should_ErrorWith405(client):
    response = await client.get(f'{url}1/')

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForSingleDoc_Should_ErrorWith405(client):
    response = await client.post(f'{url}1/', json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForSingleDoc_Should_ErrorWith405(client):
    response = await client.put(f'{url}1/', json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForSingleDoc_Should_ErrorWith405(client):
    response = await client.patch(f'{url}1/', json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForSingleDocWithNotFoundId_Should_NotFound(client):
    response = await client.delete(f'{url}1/')

    expected_status = status.HTTP_404_NOT_FOUND
    real_status = response.status_code

    expected_body = ''
    real_body = response.text

    assert expected_status == real_status
    assert expected_body == real_body


async def test_When_DeleteForSingleDocWithFoundId_Should_DeleteFromDatabase(
        client, filling_docs,
):
    response = await client.delete(f'{url}1/')

    async with async_database.session() as db, db.begin():
        docs_orm = await db.execute(select(DocModel))
        docs = docs_orm.scalars().all()

    expected_status = status.HTTP_204_NO_CONTENT
    real_status = response.status_code

    expected_body = ''
    real_body = response.text

    expected_len_docs = 1
    real_len_docs = len(docs)

    assert expected_status == real_status
    assert expected_body == real_body
    assert expected_len_docs == real_len_docs
