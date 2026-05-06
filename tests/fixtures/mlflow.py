from contextlib import ExitStack
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

    with ExitStack() as stack:
        mock_log = stack.enter_context(patch("mlflow.onnx.log_model"))
        stack.enter_context(patch("mlflow.start_run"))
        stack.enter_context(patch("mlflow.log_param"))
        stack.enter_context(patch("mlflow.log_params"))
        stack.enter_context(patch("mlflow.log_metric"))
        stack.enter_context(patch("mlflow.log_metrics"))
        stack.enter_context(patch("mlflow.log_artifact"))
        stack.enter_context(patch("mlflow.log_dict"))
        stack.enter_context(patch("mlflow.log_text"))
        stack.enter_context(patch("mlflow.tracking.MlflowClient", return_value=mock_client))
        stack.enter_context(patch("services.train.service.MlflowClient", return_value=mock_client))
        stack.enter_context(
            patch("src.services.train.service.MlflowClient", return_value=mock_client)
        )
        stack.enter_context(patch("core.utils.mlflow_util.MlflowClient", return_value=mock_client))
        stack.enter_context(
            patch("src.core.utils.mlflow_util.MlflowClient", return_value=mock_client)
        )
        stack.enter_context(
            patch("services.prediction.predictor.MlflowClient", return_value=mock_client)
        )
        stack.enter_context(
            patch("src.services.prediction.predictor.MlflowClient", return_value=mock_client)
        )
        stack.enter_context(patch("mlflow.artifacts", mock_artifacts))
        stack.enter_context(patch("mlflow.artifacts.download_artifacts"))
        stack.enter_context(patch("mlflow.set_tracking_uri"))
        stack.enter_context(patch("mlflow.set_experiment"))
        stack.enter_context(patch("mlflow.set_tag"))

        mock_info = mock_log.return_value
        mock_info.registered_model_version = "1"
        yield
