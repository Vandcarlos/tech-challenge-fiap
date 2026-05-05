from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_mlflow():
    """Faz mock de todas as chamadas do MLflow automaticamente para todos os testes"""
    with (
        patch("mlflow.start_run"),
        patch("mlflow.log_param"),
        patch("mlflow.log_params"),
        patch("mlflow.log_metric"),
        patch("mlflow.log_metrics"),
        patch("mlflow.log_artifact"),
        patch("mlflow.log_dict"),
        patch("mlflow.log_text"),
        patch("mlflow.onnx.log_model") as mock_log,
    ):
        mock_info = mock_log.return_value
        mock_info.registered_model_version = "1"
        yield
