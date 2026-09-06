from typing_extensions import override

from app.repo.client.base import AsyncBaseClient


class AsyncInMemoryClient(AsyncBaseClient):
    """内存客户端：无真实连接，所有生命周期操作恒成功。"""

    @override
    async def connect(self) -> bool:
        """初始化客户端连接池"""
        return True

    @override
    async def close(self) -> None:
        """关闭客户端连接"""
        pass

    @override
    async def ping(self) -> bool:
        """检查客户端连接是否正常"""
        return True
