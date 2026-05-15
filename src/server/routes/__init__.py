from fastapi import FastAPI

from .monitor import router as monitor_router
from .operations import router as ops_router
from .serving import router as serving_router


def include_routers(app: FastAPI):
    app.include_router(ops_router)
    app.include_router(monitor_router)
    app.include_router(serving_router)


__all__ = ["include_routers"]
