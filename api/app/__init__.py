import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor

from app.requests import HTTP_POOL
from app.logger import setup_logger
from app.settings import settings
from app.views import router


THREAD_POOL_WORKERS = 5


async def startup_task():
    setup_logger()
    
    if settings.IS_LOCAL and settings.DEBUG:
        print(settings)
    
    loop = asyncio.get_event_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=THREAD_POOL_WORKERS))


async def shutdown_task():
    await HTTP_POOL.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="ES API",
        version="0.1.0",
        debug=settings.DEBUG,
        docs_url="/docs" if settings.IS_LOCAL else None,
        redoc_url="/redoc" if settings.IS_LOCAL else None,
        openapi_url="/openapi.json" if settings.IS_LOCAL else None,
        on_startup=[startup_task],
        on_shutdown=[shutdown_task],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.IS_LOCAL else settings.CORS_ALLOWED,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app


app = create_app()
