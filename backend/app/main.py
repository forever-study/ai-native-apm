import dotenv

dotenv.load_dotenv()

# ruff: noqa: E402
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from mcp.server.mcpserver import MCPServer
from opentelemetry import trace

from app.core.mcp import mcp_server
from app.core.observability.otel import OTelInitializer, otel_initializer

logger = logging.getLogger(__name__)


def create_app(mcp_server: MCPServer, otel_initializer: OTelInitializer) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
        try:
            async with mcp_server.session_manager.run():
                yield
        finally:
            otel_initializer.stop()

    app = FastAPI(lifespan=lifespan)
    otel_initializer.setup(app)
    mcp_app = mcp_server.streamable_http_app(streamable_http_path="/")
    app.mount("/mcp", mcp_app)
    return app


app = create_app(mcp_server, otel_initializer)


@mcp_server.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b


@app.get("/")
def home() -> dict[str, str]:
    tracer = trace.get_tracer("hello world")
    with tracer.start_as_current_span("home"):
        logger.info("start_as_current_span")
    logger.error("Test logger export ERROR")
    return {"Hello": "World"}
