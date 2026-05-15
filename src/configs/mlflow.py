import logging
import os

import mlflow

from src import env

logger = logging.getLogger(__name__)


def setup_mlfow():
    logger.debug("MLFlow configurando...")

    os.environ["MLFLOW_HTTP_REQUEST_TIMEOUT"] = "5"
    os.environ["MLFLOW_HTTP_REQUEST_MAX_RETRIES"] = "2"

    try:
        mlflow.set_tracking_uri(env.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(env.MLFLOW_EXPERIMENT_NAME)
        logger.debug("MLFLOW configurado!")
    except Exception as e:
        logger.critical("MLFLOW erro no setup", e)
        raise e
