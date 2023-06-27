from elasticsearch import AsyncElasticsearch

from app.settings import settings

async_elasticsearch = AsyncElasticsearch(
    settings.ELASTICSEARCH_URL
)
