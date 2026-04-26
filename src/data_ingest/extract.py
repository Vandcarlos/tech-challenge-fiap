"""Extrai os dados da kaggle e salva raw na camada bronze"""

import logging
import os

import kagglehub

from data_ingest import arg_util, logger_util

logger_util.configure_logging()
logger = logging.getLogger(__name__)

DATASET_KAGGLE_ID = "yeanzc/telco-customer-churn-ibm-dataset"
DEST_PATH_ARG = "DESTINATION_PATH"
PARTITION_ARG = "YEAR_MONTH"


def main():
    """Função principal do módulo de extração."""
    year_month = arg_util.get_arg(PARTITION_ARG)
    if not year_month:
        logger.error("❌ Parâmetro de partição não fornecido. Use --%s.", PARTITION_ARG)
        raise ValueError("Parâmetro de partição não fornecido.")

    destination = arg_util.get_arg(DEST_PATH_ARG)

    if not destination:
        logger.error("❌ Parâmetro de destino não fornecido. Use --%s.", DEST_PATH_ARG)
        raise ValueError("Caminho de destino não fornecido.")

    dataset_destination = os.path.join(destination, year_month)

    logger.info("Iniciando extração dos dados da Kaggle...")
    try:
        kagglehub.dataset_download(DATASET_KAGGLE_ID, output_dir=dataset_destination)
        logger.info("✅ Extração concluída com sucesso.")
    except Exception as e:
        logger.error("❌ Erro durante a extração: %s", str(e))
        raise


if __name__ == "__main__":
    main()
