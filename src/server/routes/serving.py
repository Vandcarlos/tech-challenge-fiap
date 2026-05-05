import logging
from dataclasses import asdict

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.domain import Prediction
from src.services import PredictionService

router = APIRouter(tags=["Serving"])

logger = logging.getLogger(__name__)


class TelecomDataRequest(BaseModel):
    gender: str
    senior_citizen: str
    partner: str
    dependents: str
    tenure_months: int
    phone_service: str
    multiple_lines: str
    internet_service: str
    online_security: str
    online_backup: str
    device_protection: str
    tech_support: str
    streaming_tv: str
    streaming_movies: str
    contract: str
    paperless_billing: str
    payment_method: str
    monthly_charges: float
    total_charges: float | None
    churn_value: int


class PredictRequest(BaseModel):
    data: list[TelecomDataRequest]


@router.post(
    "/predict",
    response_model=list[Prediction],
    status_code=status.HTTP_200_OK,
    summary="Realiza a predição de Churn",
    description="Recebe uma lista de dados de clientes e retorna a probabilidade de Churn.",
)
async def predict(request: PredictRequest):
    """
    Endpoint principal para consumo do modelo.
    """
    try:
        service = PredictionService()

        request_as_dicts = [item.model_dump() for item in request.data]
        predictions = service.predict(request_as_dicts)
        response_as_dicts = [asdict(p) for p in predictions]
        return response_as_dicts

        return predictions

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error("Erro na predição: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a predição.",
        )
