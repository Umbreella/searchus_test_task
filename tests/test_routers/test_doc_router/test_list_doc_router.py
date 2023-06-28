import asyncio

from fastapi import status

url = '/api/documentation/'


async def test_When_PostForListDocs_Should_ErrorWith405(client):
    response = await client.post(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForListDocs_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForListDocs_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForListDocs_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListDocsWithEmptyQueryParams_Should_ErrorWith405(
        client, filling_docs,
):
    await asyncio.sleep(1)

    response = await client.get(url)

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_response = []
    real_response = response.json()

    assert expected_status == real_status
    assert expected_response == real_response


async def test_When_GetForListDocsWithQueryParams_Should_ErrorWith405(
        client, filling_docs,
):
    await asyncio.sleep(1)

    response = await client.get(f'{url}?search=text')

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_response = [
        {
            'id': 2,
            'text': 'text',
            'rubrics': ['test_rubric', 'test_rubric', ],
        },
        {
            'id': 1,
            'text': 'text',
            'rubrics': ['rubric', 'rubric', ],
        },
    ]
    real_response = response.json()

    all_has_created_date = all([
        doc.pop('created_date') is not None for doc in real_response
    ])

    assert expected_status == real_status
    assert expected_response == real_response
    assert all_has_created_date is True
