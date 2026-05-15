import os
from pathlib import Path

from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).parent
BASE_DIR = CURRENT_DIR.parent
DOTENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=DOTENV_PATH)

MLFLOW_HOST = os.getenv("MLFLOW_HOST") or "http://localhost"
MLFLOW_PORT = os.getenv("MLFLOW_PORT") or "5500"
MLFLOW_TRACKING_URI = f"{MLFLOW_HOST}:{MLFLOW_PORT}"
MLFLOW_EXPERIMENT_NAME = "FIAP_Tech_Challenge-Churn_Prediction"
MLFLOW_MODEL_NAME = "churn_mlp_model"
MLFLOW_PREPROCESSOR_NAME = "preprocessor.pkl"
MLFLOW_METRICS_NAME = "metrics.json"
MLFLOW_ARTIFACTS_ROOT = os.getenv("MLFLOW_ARTIFACT_ROOT") or "artifacts"
MLFLOW_BACKEND_STORE_URI = os.getenv("MLFLOW_BACKEND_STORE_URI")
MLFLOW_REGISTRY_STORE_URI = os.getenv("MLFLOW_REGISTRY_STORE_URI")
MLFLOW_POSTGRES_DB = os.getenv("MLFLOW_POSTGRES_DB")
MLFLOW_POSTGRES_USER = os.getenv("MLFLOW_POSTGRES_USER")
MLFLOW_POSTGRES_PASSWORD = os.getenv("MLFLOW_POSTGRES_PASSWORD")

# DATA_LAKE
DATA_LAKE_BRONZE_PATH = Path(os.getenv("DATA_LAKE_BRONZE_PATH") or "./data/bronze")
DATA_LAKE_SIVER_PATH = Path(os.getenv("DATA_LAKE_SIVER_PATH") or "./data/silver")
DATA_LAKE_GOLD_PATH = Path(os.getenv("DATA_LAKE_GOLD_PATH") or "./data/gold")
SPARK_SESSION_NAME = os.getenv("SPARK_SESSION_NAME") or "telecon_churn"

DATA_METRICS_CACHE_PATH = Path("./data/metrics")

MODELS_PATH = Path(os.getenv("MODELS_PATH") or "./models")
TRAIN_MODELS_PATH = MODELS_PATH / "train"
PREDICT_MODELS_PATH = MODELS_PATH / "predict"
MODEL_NAME = "model.onnx"
PREPROCESSOR_NAME = "preprocessor.pkl"
PREDICT_MODEL_VERSION = os.getenv("PREDICT_MODEL_VERSION") or "1.0.0"

# SERVER
SERVER_HOST = os.getenv("SERVER_HOST") or "localhost"
SERVER_PORT = int(os.getenv("SERVER_PORT") or "8888")
