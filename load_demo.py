import asyncio
import csv
import json

from progress.bar import Bar

import alembic.config
from app.settings import settings
from models.DocModel import DocModel
from schemas.DocSchema import DocSchemaIn
from services.async_database import async_database


async def main():
    pg_host = settings.DATABASE_URL_HOST
    pg_port = settings.DATABASE_URL_PORT
    pg_user = settings.DATABASE_URL_USER
    pg_password = settings.DATABASE_URL_PASSWORD
    pg_db = settings.DATABASE_URL_DB

    connection_str = ''.join((
        'postgresql+psycopg://',
        f'{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}',
    ))

    async_database.init_db(connection_str)

    async with async_database.session() as db, db.begin():
        with Bar('Init database ...', max=1500) as bar:
            with open('demo/init_data.csv', newline='',
                      encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for item in reader:
                    data = DocSchemaIn(**{
                        'text': item.get('text'),
                        'created_date': item.get('created_date'),
                        'rubrics': json.loads(
                            item.get('rubrics').replace('\'', '\"')
                        ),
                    })

                    await DocModel.create(data, db)
                    bar.next()


if __name__ == '__main__':
    alembic.config.main(argv=[
        '--raiseerr', 'downgrade', 'base',
    ])
    alembic.config.main(argv=[
        '--raiseerr', 'upgrade', 'head',
    ])
    asyncio.run(main())
