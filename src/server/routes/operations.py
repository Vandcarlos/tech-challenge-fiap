from fastapi import APIRouter, BackgroundTasks, status
from pydantic import BaseModel

from core.modules import SparkSessionX
from core.utils import datalake_util
from src import env
from src.services import IngestService, TrainService

router = APIRouter(prefix="/ops", tags=["Operations"])


class IngestRequest(BaseModel):
    use_fake: bool = False
    year_month: str | None = None


@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest(background_tasks: BackgroundTasks, request: IngestRequest):
    processed_year_month = datalake_util.year_month_to_bronze_layer(request.year_month)

    service = IngestService(spark_session=SparkSessionX())

    background_tasks.add_task(
        service.ingest,
        env.DATA_LAKE_BRONZE_PATH / processed_year_month,
        env.DATA_LAKE_SIVER_PATH / processed_year_month,
        request.use_fake,
    )

    return {
        "status": "ETL disparada com sucesso",
        "target": processed_year_month,
    }


class TrainRequest(BaseModel):
    year_month: str


@router.post("/train", status_code=status.HTTP_202_ACCEPTED)
async def train(background_tasks: BackgroundTasks, request: TrainRequest):
    service = TrainService()

    processed_year_month = datalake_util.year_month_to_silver_layer(
        request.year_month,
        env.DATA_LAKE_BRONZE_PATH,
    )

    data_source_path = env.DATA_LAKE_SIVER_PATH / processed_year_month
    data_target_path = env.DATA_LAKE_GOLD_PATH / processed_year_month
    artifacts_target_path = env.MODELS_PATH / processed_year_month
    background_tasks.add_task(
        service.train, data_source_path, data_target_path, artifacts_target_path
    )

    return {
        "status": "Treinamento iniciado",
        "mlflow_url": env.MLFLOW_TRACKING_URI,
    }
