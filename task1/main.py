from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.db import create_redis_pool
from app.logger import LOGGER
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.debug("startup event - start")
    # create redis connection pool on startup to reuse it on every Redis dependency call
    app.state.redis_pool = create_redis_pool()
    LOGGER.debug("startup event - finish")
    yield
    LOGGER.debug("shutdown event - start")
    await app.state.redis_pool.disconnect()
    LOGGER.debug("shutdown event - finish")


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Lexicom",
        description="Address service Service",
        version="1.0.0",
        lifespan=lifespan
    )
    app_.include_router(router)
    app_.logger = LOGGER
    return app_


app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
