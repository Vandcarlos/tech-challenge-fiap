import pickle
from dataclasses import dataclass
from pathlib import Path

from sklearn.compose import ColumnTransformer

from .dataset import Dataset

NAME_X_TRAIN = "x_train.parquet"
NAME_Y_TRAIN = "y_train.parquet"
NAME_X_VAL = "x_val.parquet"
NAME_Y_VAL = "y_val.parquet"
NAME_X_TEST = "x_test.parquet"
NAME_Y_TEST = "y_test.parquet"

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
    def preprocessor_path(self) -> Path:
        return self.artifacts_target_path / NAME_PREPROCESSOR

    @property
    def model_path(self) -> Path:
        return self.artifacts_target_path / NAME_MODEL

    def write_data(self, dataset: Dataset):
        self.data_target_path.mkdir(parents=True, exist_ok=True)

        print("dataset criado")
        print("X", len(dataset.X_train), "\n")
        print("Y", len(dataset.y_train), "\n")
        print("X", len(dataset.X_val), "\n")
        print("Y", len(dataset.y_val), "\n")
        print("X", len(dataset.X_test), "\n")
        print("Y", len(dataset.y_test), "\n")

        print("paths")
        print("X", self.x_train_data_path, "\n")
        print("Y", self.y_train_data_path, "\n")
        print("X", self.x_val_data_path, "\n")
        print("Y", self.y_val_data_path, "\n")
        print("X", self.x_test_data_path, "\n")
        print("Y", self.y_test_data_path, "\n")

        dataset.X_train.to_parquet(self.x_train_data_path)
        dataset.y_train.to_frame().to_parquet(self.y_train_data_path)

        dataset.X_val.to_parquet(self.x_val_data_path)
        dataset.y_val.to_frame().to_parquet(self.y_val_data_path)

        dataset.X_test.to_parquet(self.x_test_data_path)
        dataset.y_test.to_frame().to_parquet(self.y_test_data_path)

    def write_artifacts(self, preprocessor: ColumnTransformer, model: bytes):
        self.artifacts_target_path.mkdir(parents=True, exist_ok=True)

        with open(self.preprocessor_path, "wb") as f:
            pickle.dump(preprocessor, f)

        with open(self.model_path, "wb") as f:
            f.write(model)
