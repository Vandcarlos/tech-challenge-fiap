import logging

from fastapi import FastAPI

from .lifespan import lifespan
from .middlewares import register_middlewares
from .routes import include_routers

logger = logging.getLogger(__name__)


def create_app():
    logger.debug("Criando aplicação")
    app = FastAPI(title="FIAP Tech Challenge - MLOps", lifespan=lifespan)

    register_middlewares(app)

    include_routers(app)

    return app
