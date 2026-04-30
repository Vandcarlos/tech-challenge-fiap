import glob
import os

from services.train import service as sut
from services.train import trainer


def test_train(silver_data_build, monkeypatch, tmp_path):
    monkeypatch.setattr(trainer, "LOSS_PATIENCE", 1)
    monkeypatch.setattr(trainer, "TRAIN_NUM_EPOCHS", 1)
    data_source_path = tmp_path / "source"
    data_target_path = tmp_path / "target"
    artifacts_target_path = tmp_path / "target"

    silver_data_build(target_path=data_source_path)

    train_service = sut.TrainService()
    train_service.train(data_source_path, data_target_path, artifacts_target_path)

    target_files_path = os.path.join(data_target_path, "*.parquet")
    target_files = glob.glob(target_files_path)

    assert len(target_files) == 6

    model_files_path = os.path.join(artifacts_target_path, "churn_mlp_model.onnx")
    model_files = glob.glob(model_files_path)
    assert len(model_files) == 1

    preprocessor_files_path = os.path.join(artifacts_target_path, "preprocessor.pkl")
    preprocessor_files = glob.glob(preprocessor_files_path)
    assert len(preprocessor_files) == 1
