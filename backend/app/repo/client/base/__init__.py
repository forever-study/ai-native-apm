from abc import ABC, abstractmethod


class AsyncBaseClient(ABC):
    @abstractmethod
    async def connect(self) -> bool:
        """初始化客户端连接池"""
        ...

    @abstractmethod
    async def close(self) -> None:
        """关闭客户端连接"""
        ...

    @abstractmethod
    async def ping(self) -> bool:
        """检查客户端连接是否正常"""
        ...
