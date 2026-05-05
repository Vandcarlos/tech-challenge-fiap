from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import mlflow
from mlflow import onnx as mlflow_onnx
from mlflow.tracking import MlflowClient

from core.modules.eval import EvaluaterModule
from core.utils.mlflow_util import mlflow_start_run
from src import env

from .dataset import Dataset
from .loader import load_data
from .preprocessor import CATEGORICAL_FEATURES, NUMERIC_FEATURES, Preprocessor
from .tensors import Tensors
from .trainer import Trainer
from .writer import Writer


class TrainService:
    @mlflow_start_run("train_model")
    def train(self, data_source_path: Path, data_target_path: Path, artifacts_target_path: Path):
        current_version = f"v{datetime.now().strftime('%Y%m%d_%H%M')}"
        mlflow.set_tag("model_version", current_version)

        mlflow.log_params(
            {
                "data_source": str(data_source_path),
                "data_target": str(data_target_path),
            }
        )

        # Prepara
        df = load_data(data_source_path)
        dataset = Dataset(df)

        mlflow.log_metrics(
            {
                "dataset_train_rows": len(dataset.X_train),
                "dataset_test_rows": len(dataset.X_test),
                "dataset_val_rows": len(dataset.X_val),
            }
        )

        preprocessor = Preprocessor(dataset)
        # Após criar o preprocessor
        mlflow.log_param("features_numeric", NUMERIC_FEATURES)
        mlflow.log_param("features_categorical", CATEGORICAL_FEATURES)
        tensors = Tensors(preprocessor)
        trainer = Trainer(tensors)

        # Treina
        model = trainer.run_train()

        # Avalia
        model_evaluation = EvaluaterModule.evaluate_model(
            model, preprocessor.transformer, dataset.X_test, dataset.y_test
        )
        mlflow.log_metrics(asdict(model_evaluation))

        # Salva
        writer = Writer(data_target_path, artifacts_target_path)
        writer.write_data(dataset, model_evaluation)
        writer.write_artifacts(preprocessor, model)

        mlflow.log_artifact(str(writer.metrics_path))

        model_info = mlflow_onnx.log_model(
            onnx_model=model,
            name="model",
            registered_model_name=env.MLFLOW_MODEL_NAME,
        )

        client = MlflowClient()
        client.set_registered_model_alias(
            name=env.MLFLOW_MODEL_NAME,
            alias=current_version,
            version=str(model_info.registered_model_version),
        )
        mlflow.log_artifact(str(writer.preprocessor_path))
        mlflow.log_artifact(str(writer.model_path))
