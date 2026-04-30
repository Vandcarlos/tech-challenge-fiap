from unittest.mock import MagicMock

import onnx
import pytest
import torch

from services.train import trainer as sut
from services.train.tensors import Tensors


@pytest.fixture
def mock_tensors():
    tensors = MagicMock(spec=Tensors)
    # Create tiny tensors: 10 rows, 4 features
    # Input dim will be 4
    tensors.X_train = torch.randn(10, 4)
    tensors.y_train = torch.randint(0, 2, (10, 1)).float()
    tensors.X_val = torch.randn(5, 4)
    tensors.y_val = torch.randint(0, 2, (5, 1)).float()
    return tensors


@pytest.fixture
def trainer_instance(mock_tensors):
    trainer = sut.Trainer(tensors=mock_tensors)
    trainer._device = torch.device("cpu")
    return trainer


def test_trainer_initialization(trainer_instance):
    # Our mock_tensors has 4 features
    assert trainer_instance._input_dim == 4
    assert trainer_instance._device.type in ["cpu", "cuda"]


def test_early_stopping_triggered(trainer_instance, monkeypatch):
    monkeypatch.setattr(sut, "LOSS_PATIENCE", 2)
    monkeypatch.setattr(sut, "TRAIN_NUM_EPOCHS", 20)

    trainer_instance._loss_criterion = MagicMock(return_value=torch.tensor(1.0, requires_grad=True))
    trainer_instance.run_train()

    assert trainer_instance._loss_criterion.call_count < 10


def test_trainer_saves_best_model(trainer_instance, monkeypatch):
    monkeypatch.setattr(sut, "TRAIN_NUM_EPOCHS", 2)
    trainer_instance._loss_criterion = MagicMock()
    trainer_instance._loss_criterion.side_effect = [
        torch.tensor(0.5, requires_grad=True),
        torch.tensor(0.5, requires_grad=True),
        torch.tensor(0.4, requires_grad=True),
        torch.tensor(0.8, requires_grad=True),
    ]

    onnx_bytes = trainer_instance.run_train()
    assert len(onnx_bytes) > 0


def test_run_train_returns_valid_onnx(trainer_instance, monkeypatch, tmp_path):
    monkeypatch.setattr(sut, "TRAIN_NUM_EPOCHS", 1)

    onnx_bytes = trainer_instance.run_train()

    model_path = tmp_path / "model.onnx"
    model_path.write_bytes(onnx_bytes)

    assert model_path.exists()
    assert model_path.stat().st_size > 0

    loaded_model = onnx.load(str(model_path))
    onnx.checker.check_model(loaded_model)

    input_dim = loaded_model.graph.input[0].type.tensor_type.shape.dim[1].dim_value
    assert input_dim == 4

    assert loaded_model.graph.input[0].name == "input"
    assert loaded_model.graph.output[0].name == "output"
