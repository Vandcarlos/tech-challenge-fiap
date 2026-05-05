from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_mlflow():
    """Faz mock de todas as chamadas do MLflow automaticamente para todos os testes"""
    # Pular inicialização do ProductionPredictor em testes
    from src.services.prediction.predictor import ProductionPredictor

    ProductionPredictor.set_skip_setup(True)

    # Mock do MlflowClient
    mock_client = MagicMock()
    mock_model_version = MagicMock()
    mock_model_version.run_id = "test_run_id"
    mock_client.get_model_version_by_alias.return_value = mock_model_version

    # Mock das funções de artifacts
    mock_artifacts = MagicMock()

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
        patch("mlflow.tracking.MlflowClient", return_value=mock_client),
        patch("mlflow.artifacts", mock_artifacts),
        patch("mlflow.artifacts.download_artifacts"),
        patch("mlflow.set_tracking_uri"),
        patch("mlflow.set_experiment"),
        patch("mlflow.set_tag"),
    ):
        mock_info = mock_log.return_value
        mock_info.registered_model_version = "1"
        yield
