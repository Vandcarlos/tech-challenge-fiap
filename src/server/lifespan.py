import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.services import PredictionService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_up(app)

    yield

    shutdown(app)


def start_up(app: FastAPI):
    logger.info("Executando método para iniciar a aplicação. %s", app.title)
    PredictionService.warm_up_model()
    logger.info("Executado método para iniciar a aplicação. %s", app.title)


def shutdown(app: FastAPI):
    logger.info("Executando método para encerrar a aplicação. %s", app.title)
    PredictionService.warm_down_model()
    logger.info("Executado método para encerrar a aplicação. %s", app.title)
