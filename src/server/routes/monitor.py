from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from src import env
from src.core.utils import mlflow_util
from src.domain import APIMetrics
from src.server.middlewares.observability import get_metrics
from src.services import PredictionService

router = APIRouter(prefix="/monitor", tags=["Monitoramento"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Retorna o estado atual da API e do motor Spark."""
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }


@router.get("/metrics", response_model=APIMetrics)
async def metrics():
    """Retorna métricas de latência das últimas 50 chamadas da API."""
    return get_metrics()


@router.get("/mlflow")
async def open_mlflow():
    """Redireciona diretamente para a UI do MLflow para análise de experimentos."""
    return RedirectResponse(url=env.MLFLOW_TRACKING_URI)


@router.get("/model-status")
async def get_model_status():
    """Retorna metadados do modelo que o Singleton do Predict carregou do MLflow."""

    service = PredictionService()
    metadata = service.get_model_metadata()

    return {
        "context": "CURRENT_MODEL_STATUS",
        "healthy": metadata.get("status") == "ready",
        "data": metadata,
    }


@router.get("/latest-training")
async def get_latest_training_metrics():
    """Busca no MLflow os resultados do último run finalizado."""

    return {
        "context": "LATEST_EXPERIMENT_RESULTS",
        "data": mlflow_util.get_latest_training_info(),
    }
