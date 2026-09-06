from typing_extensions import override

from app.repo.backend.base import AsyncBaseBackend
from app.repo.client.memory import AsyncInMemoryClient


class AsyncInMemoryBackend(AsyncBaseBackend[AsyncInMemoryClient]):
    @override
    def _create_client(self) -> AsyncInMemoryClient:
        return AsyncInMemoryClient()

    @override
    async def connect(self) -> bool:
        """初始化内存后端"""
        return True

    @override
    async def close(self) -> None:
        """关闭内存后端"""
        pass
