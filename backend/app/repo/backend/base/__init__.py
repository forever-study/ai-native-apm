from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar

from app.repo.client.base import AsyncBaseClient

TClient = TypeVar("TClient", bound=AsyncBaseClient)


class AsyncBaseBackend(Generic[TClient], ABC):
    def __init__(self, client: TClient | None = None) -> None:
        self.client: TClient = client or self._create_client()

    @abstractmethod
    def _create_client(self) -> TClient:
        """创建客户端实例"""
        ...

    @abstractmethod
    async def connect(self) -> bool:
        """初始化后端连接池"""
        ...

    @abstractmethod
    async def close(self) -> None:
        """关闭后端连接"""
        ...


class AsyncBackendProtocol(Protocol):
    """后端协议接口"""

    async def connect(self) -> bool: ...
    async def close(self) -> None: ...
