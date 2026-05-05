import logging
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def year_month_to_bronze_layer(year_month: str | None) -> str:
    return year_month if year_month is not None else datetime.now().strftime("%Y%m")


def year_month_to_silver_layer(year_month: str | None, bronze_layer_path: Path) -> str:
    if year_month is not None:
        return year_month

    logger.info(
        "⚠️ Parâmetro de data não fornecido. Tentando inferir a última data disponível em: %s",
        bronze_layer_path,
    )

    try:
        path_dirs = os.listdir(bronze_layer_path)
    except Exception as e:
        logger.exception("❌ Problema ao listar os diretórios em %s: %s", bronze_layer_path, e)
        raise e

    year_months = [d for d in path_dirs if os.path.isdir(bronze_layer_path / d)]

    if not year_months:
        logger.error("❌ Nenhuma data encontrada em: %s", bronze_layer_path)
        raise ValueError("Nenhuma data encontrada encontrada.")

    year_month = sorted(year_months)[-1]
    return year_month
