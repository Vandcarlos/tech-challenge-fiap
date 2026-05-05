from dataclasses import asdict
from pathlib import Path

import mlflow

from core.modules.eval import EvaluaterModule
from core.utils.mlflow_util import mlflow_start_run

from .dataset import Dataset
from .loader import load_data
from .preprocessor import CATEGORICAL_FEATURES, NUMERIC_FEATURES, Preprocessor
from .tensors import Tensors
from .trainer import Trainer
from .writer import Writer


class TrainService:
    @mlflow_start_run("train_model")
    def train(self, data_source_path: Path, data_target_path: Path, artifacts_target_path: Path):
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
        mlflow.log_artifact(str(writer.preprocessor_path))
        mlflow.log_artifact(str(writer.metrics_path))
        mlflow.log_artifact(str(writer.model_path))
