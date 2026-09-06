import logging

from typing_extensions import override

from app.config import settings
from app.repo.backend.base import AsyncBaseBackend
from app.repo.client.es import AsyncElasticsearchClient

logger = logging.getLogger(__name__)


class AsyncElasticsearchBackend(AsyncBaseBackend[AsyncElasticsearchClient]):
    @override
    def _create_client(self) -> AsyncElasticsearchClient:
        """创建客户端实例"""
        return AsyncElasticsearchClient()

    @override
    async def connect(self) -> bool:
        """初始化 ES 客户端连接池"""
        if not settings.es.es_enabled:
            return False
        return await self.client.connect()

    @override
    async def close(self) -> None:
        """关闭客户端连接"""
        await self.client.close()
