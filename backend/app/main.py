from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("ai_native_apm_mcp")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan)
mcp_app = mcp.streamable_http_app(streamable_http_path="/")
app.mount("/mcp", mcp_app)


@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的和。"""
    return a + b


@app.get("/")
def home() -> dict[str, str]:
    return {"Hello": "World"}
