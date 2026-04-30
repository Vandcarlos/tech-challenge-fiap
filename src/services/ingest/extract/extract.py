"""Extrai os dados da kaggle e salva raw na camada bronze"""

import logging
from pathlib import Path

import kagglehub
import pandera.pandas as pa

from core.utils import logger_util
from domain.telecon import TelecomPandasIn

logger_util.configure_logging()
logger = logging.getLogger(__name__)

DATASET_KAGGLE_ID = "yeanzc/telco-customer-churn-ibm-dataset"


class Extracter:
    @pa.check_output(TelecomPandasIn)
    def run_extract(self, output_path: Path) -> Path: ...


class ExtracterImp(Extracter):
    def run_extract(self, output_path: Path) -> Path:
        try:
            path = kagglehub.dataset_download(DATASET_KAGGLE_ID, output_dir=str(output_path))
            logger.info("✅ Extração concluída com sucesso.")
        except Exception as e:
            logger.error("❌ Erro durante a extração: %s", str(e))
            raise

        return Path(path)
