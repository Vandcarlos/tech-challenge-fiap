import json
import pickle
from dataclasses import asdict, dataclass
from pathlib import Path

from domain.evaluation_metrics import EvaluationMetrics

from .dataset import Dataset
from .preprocessor import Preprocessor

NAME_X_TRAIN = "x_train.parquet"
NAME_Y_TRAIN = "y_train.parquet"
NAME_X_VAL = "x_val.parquet"
NAME_Y_VAL = "y_val.parquet"
NAME_X_TEST = "x_test.parquet"
NAME_Y_TEST = "y_test.parquet"

NAME_METRICS = "metrics.json"

NAME_PREPROCESSOR = "preprocessor.pkl"
NAME_MODEL = "churn_mlp_model.onnx"


@dataclass
class Writer:
    data_target_path: Path
    artifacts_target_path: Path

    @property
    def x_train_data_path(self) -> Path:
        return self.data_target_path / NAME_X_TRAIN

    @property
    def y_train_data_path(self) -> Path:
        return self.data_target_path / NAME_Y_TRAIN

    @property
    def x_val_data_path(self) -> Path:
        return self.data_target_path / NAME_X_VAL

    @property
    def y_val_data_path(self) -> Path:
        return self.data_target_path / NAME_Y_VAL

    @property
    def x_test_data_path(self) -> Path:
        return self.data_target_path / NAME_X_TEST

    @property
    def y_test_data_path(self) -> Path:
        return self.data_target_path / NAME_Y_TEST

    @property
    def metrics_path(self) -> Path:
        return self.data_target_path / NAME_METRICS

    @property
    def preprocessor_path(self) -> Path:
        return self.artifacts_target_path / NAME_PREPROCESSOR

    @property
    def model_path(self) -> Path:
        return self.artifacts_target_path / NAME_MODEL

    def write_data(self, dataset: Dataset, metrics: EvaluationMetrics):
        self.data_target_path.mkdir(parents=True, exist_ok=True)

        dataset.X_train.to_parquet(self.x_train_data_path)
        dataset.y_train.to_frame().to_parquet(self.y_train_data_path)

        dataset.X_val.to_parquet(self.x_val_data_path)
        dataset.y_val.to_frame().to_parquet(self.y_val_data_path)

        dataset.X_test.to_parquet(self.x_test_data_path)
        dataset.y_test.to_frame().to_parquet(self.y_test_data_path)

        with open(self.metrics_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=4)

    def write_artifacts(self, preprocessor: Preprocessor, model: bytes):
        self.artifacts_target_path.mkdir(parents=True, exist_ok=True)

        with open(self.preprocessor_path, "wb") as f:
            pickle.dump(preprocessor.transformer, f)

        with open(self.model_path, "wb") as f:
            f.write(model)
