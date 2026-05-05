import json
import logging
from functools import wraps

import mlflow
from mlflow import artifacts as mlflow_artifacts
from mlflow.tracking import MlflowClient

from src import env

logger = logging.getLogger(__name__)


def mlflow_start_run(run_name: str | None = None, nested: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = run_name if run_name else func.__name__
            with mlflow.start_run(run_name=name, nested=nested):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def get_latest_training_info():
    client = MlflowClient()

    experiment = client.get_experiment_by_name(env.MLFLOW_EXPERIMENT_NAME)
    if not experiment:
        return {"error": "Experimento não encontrado"}

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="attributes.run_name = 'train_model' status = 'FINISHED'",
        max_results=1,
        order_by=["attributes.start_time DESC"],
    )

    if not runs:
        return {"status": "Nenhum treino encontrado"}

    last_run = runs[0]
    run_id = last_run.info.run_id

    try:
        local_path = mlflow_artifacts.download_artifacts(
            run_id=run_id, artifact_path=env.MLFLOW_METRICS_NAME
        )

        with open(local_path, "r") as f:
            metrics_asset = json.load(f)
    except Exception as e:
        logger.warning("Não foi possível baixar as métricas: %s", e)
        metrics_asset = {"warning": "Asset de métricas não disponível"}

    return {
        "run_id": run_id,
        "tag_version": last_run.data.tags.get("model_version", "N/A"),
        "start_time": last_run.info.start_time,
        "metrics": {
            "mlflow": last_run.data.metrics,
            "assets": metrics_asset,
        },
        "params": last_run.data.params,
        "tags": last_run.data.tags,
    }
