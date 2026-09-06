import logging

from elasticsearch import dsl
from typing_extensions import override

from app.config import settings
from app.models.es import AsyncSpan
from app.repo.backend.base import AsyncBaseBackend
from app.repo.client.es import AsyncElasticsearchClient

logger = logging.getLogger(__name__)


class AsyncElasticsearchBackend(AsyncBaseBackend[AsyncElasticsearchClient]):
    """Elasticsearch 后端"""

    MODELS: list[type[dsl.AsyncDocument]] = [AsyncSpan]

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
    async def init(self) -> None:
        """初始化 ES 客户端"""
        if not await self.connect():
            return
        for model_cls in self.MODELS:
            await model_cls.init()
            logger.info(
                f"✅ [AsyncElasticsearchBackend] {model_cls.__name__} 索引初始化完成"
            )
        logger.info("✅ [AsyncElasticsearchBackend] Elasticsearch 后端初始化完成")
        return

    @override
    async def close(self) -> None:
        """关闭客户端连接"""
        await self.client.close()
