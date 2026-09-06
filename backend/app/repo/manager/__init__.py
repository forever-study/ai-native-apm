import logging

from app.repo.backend import (
    AsyncBackendProtocol,
    AsyncElasticsearchBackend,
    AsyncInMemoryBackend,
)

logger = logging.getLogger(__name__)


class RepoManager:
    BACKENDS: list[type[AsyncBackendProtocol]] = [
        AsyncElasticsearchBackend,
        AsyncInMemoryBackend,
    ]

    def __init__(self, backend: AsyncBackendProtocol | None = None) -> None:
        self._backend: AsyncBackendProtocol | None = backend

    @property
    def backend(self) -> AsyncBackendProtocol:
        if not self._backend:
            raise RuntimeError("❌ [RepoManager] Failed to connect to any backend")
        return self._backend

    async def connect(self) -> None:
        """初始化存储后端。

        优先使用注入的后端；否则按 BACKENDS 顺序探测（ES 失败自动降级内存）。
        全部失败时抛出 RuntimeError，由调用方（lifespan）终止启动。
        """
        if self._backend is not None:
            if not await self.backend.connect():
                raise RuntimeError(
                    f"❌ [RepoManager] Failed to connect to backend {type(self.backend).__name__}"
                )
            return

        for backend_cls in self.BACKENDS:
            backend = backend_cls()
            if await backend.connect():
                self._backend = backend
                logger.info(f"✅ [RepoManager] Connected to {backend_cls.__name__}")
                return

        raise RuntimeError("❌ [RepoManager] Failed to connect to any backend")

    async def init(self) -> None:
        """初始化后端"""
        await self.connect()
        await self.backend.init()
        logger.info(f"✅ [RepoManager] Initialized {type(self.backend).__name__}")

    async def close(self) -> None:
        """关闭后端连接（幂等：未连接时直接返回）"""
        if self._backend is None:
            return
        await self.backend.close()
        logger.info(
            f"✅ [RepoManager] Closed connection to backend {type(self.backend).__name__}"
        )


repo_manager = RepoManager()
