from elasticsearch import AsyncElasticsearch
from typing_extensions import override

from app.config import settings
from app.repo.client.base import AsyncBaseClient


class AsyncElasticsearchClient(AsyncBaseClient):
    def __init__(self, client: AsyncElasticsearch | None = None):
        self._client: AsyncElasticsearch | None = client

    def _create_client(self) -> AsyncElasticsearch:
        return AsyncElasticsearch(
            hosts=[settings.es.elasticsearch_url],
            api_key=settings.es.elastic_api_key,
            retry_on_timeout=True,
            retry_backoff_base=0.5,
            retry_backoff_cap=5.0,
        )

    @property
    def client(self) -> AsyncElasticsearch:
        if self._client is None:
            self._client = self._create_client()
        return self._client

    @override
    async def connect(self) -> bool:
        """初始化 Elasticsearch 客户端连接池"""
        return await self.client.ping()

    @override
    async def close(self) -> None:
        """关闭 Elasticsearch 客户端连接"""
        await self.client.close()
        self._client = None

    @override
    async def ping(self) -> bool:
        """检查 Elasticsearch 客户端连接是否正常"""
        return await self.client.ping()
