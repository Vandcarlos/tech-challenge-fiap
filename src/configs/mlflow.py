import mlflow

from src import env


def setup_mlfow():
    mlflow.set_tracking_uri(env.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(env.MLFLOW_EXPERIMENT_NAME)
