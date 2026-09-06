import logging

from typing_extensions import override

from app.repo.backend.base import AsyncBaseBackend
from app.repo.client.memory import AsyncInMemoryClient

logger = logging.getLogger(__name__)


class AsyncInMemoryBackend(AsyncBaseBackend[AsyncInMemoryClient]):
    @override
    def _create_client(self) -> AsyncInMemoryClient:
        return AsyncInMemoryClient()

    @override
    async def connect(self) -> bool:
        """初始化内存后端"""
        logger.info("✅ Connected to in-memory backend")
        return True

    @override
    async def close(self) -> None:
        """关闭内存后端"""
        logger.info("✅ Closed in-memory backend")
        pass

    @override
    async def init(self) -> None:
        """初始化内存后端"""
        logger.info("✅ Initialized in-memory backend")
        return
