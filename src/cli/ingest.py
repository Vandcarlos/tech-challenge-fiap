"""
Módulo de transformação de dados localmente.
- extrai dados de uma fonte
- aplica transformações
- salva os dados transformados em um arquivo Parquet
"""

import logging
from datetime import datetime
from pathlib import Path

from pyspark.sql import SparkSession

from core.utils import arg_util, logger_util
from services.ingest.service import IngestService

logger_util.configure_logging()
logger = logging.getLogger(__name__)

SPARK_NAME = "LocalDataIngest"

DATA_SOURCE_PATH_ARG = "SOURCE_PATH"
DATA_TARGET_PATH_ARG = "TARGET_PATH"
YEAR_MONTH_ARG = "YEAR_MONTH"
USE_FAKE_DATA_ARG = "USE_FAKE_DATA"


class InputArgs:
    _data_source_path: Path
    _data_target_path: Path
    _year_month: str

    use_fake_data: bool

    @property
    def data_source_path(self) -> Path:
        return self._data_source_path / self._year_month

    @property
    def data_target_path(self) -> Path:
        return self._data_target_path / self._year_month

    def __init__(self):
        data_source = arg_util.get_arg(DATA_SOURCE_PATH_ARG)
        if data_source is None:
            raise ValueError(
                "❌ Necessário path para salvar dados de origem. --SOURCE_PATH='some/path/bronze'"
            )

        data_target = arg_util.get_arg(DATA_TARGET_PATH_ARG)

        if data_target is None:
            raise ValueError(
                "❌ Necessário path para salvar dados tratados. --TARGET_PATH='some/path/silver'"
            )

        self._data_source_path = Path(data_source)
        self._data_target_path = Path(data_target)

        year_month = arg_util.get_arg(YEAR_MONTH_ARG)

        if year_month is None:
            year_month = datetime.now().strftime("%Y%m")

        self._year_month = year_month

        self.use_fake_data = arg_util.get_arg(USE_FAKE_DATA_ARG) == "True"


def _get_spark_session() -> SparkSession:
    spark = SparkSession.builder.appName(SPARK_NAME).getOrCreate()
    return spark


def main():
    """Função principal do módulo de ingestão local."""
    spark = _get_spark_session()

    try:
        input_args = InputArgs()
    except ValueError as e:
        logger.error("❌ Erro de configuração: %s", e)
        raise

    try:
        ingest_service = IngestService(spark)

        logger.info("Inciando ingestão de dados")
        ingest_service.ingest(
            input_args.data_source_path, input_args.data_target_path, input_args.use_fake_data
        )
        logger.info("Finalizado ingestão de dados com sucesso")

    except (IOError, RuntimeError) as e:
        logger.error("❌ Erro de execução ou IO: %s", e)
        raise
    except Exception as e:
        logger.exception("❌ Erro inesperado: %s", str(e))
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
