import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

MLFLOW_HOST = os.getenv("MLFLOW_HOST") or "http://localhost"
MLFLOW_PORT = os.getenv("MLFLOW_PORT") or "5500"
MLFLOW_TRACKING_URI = f"{MLFLOW_HOST}:{MLFLOW_PORT}"
MLFLOW_EXPERIMENT_NAME = "FIAP_Tech_Challenge-Churn_Prediction"
