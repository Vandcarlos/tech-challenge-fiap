"""
Módulo de transformação de dados localmente.
- extrai dados de uma fonte
- aplica transformações
- salva os dados transformados em um arquivo Parquet
"""

import glob
import logging
import os

from pyspark.sql import SparkSession

from data_ingest import arg_util, logger_util, transform

logger_util.configure_logging()
logger = logging.getLogger(__name__)

SOURCE_PATH_ARG = "SOURCE_PATH"
DEST_PATH_ARG = "DESTINATION_PATH"
PARTITION_ARG = "YEAR_MONTH"


def _get_spark_session() -> SparkSession:
    spark = SparkSession.builder.appName("LocalDataIngest").getOrCreate()
    return spark


def _run_etl(
    spark: SparkSession,
    source_path: str,
    source_file_name: str,
    dest_path: str,
) -> None:
    transformed_df = transform.transform_data(spark, source_path, source_file_name)

    if transformed_df.isEmpty():
        logger.warning("⚠️ DataFrame transformado está vazio.")
        return

    logger.info("Escrevendo %d registros em: %s", transformed_df.count(), dest_path)

    transformed_df.write.mode("overwrite").parquet(dest_path)
    logger.info("✅ Processamento concluído com sucesso.")


def _get_source_root() -> str:
    source_root = arg_util.get_arg(SOURCE_PATH_ARG)

    if not source_root:
        logger.error("❌ Parâmetro de origem não fornecido. Use --%s.", SOURCE_PATH_ARG)
        raise ValueError("Caminho de origem não fornecido.")

    return source_root


def _get_partition_arg(source_root: str) -> str:
    partition_arg = arg_util.get_arg(PARTITION_ARG)

    if partition_arg:
        return partition_arg

    logger.info(
        "⚠️ Parâmetro de partição não fornecido. Tentando inferir a última partição disponível em: %s",
        source_root,
    )

    try:
        partitions = [
            d for d in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, d))
        ]
        if not partitions:
            logger.error("❌ Nenhuma partição encontrada em: %s", source_root)
            raise ValueError("Nenhuma partição encontrada.")
        partition_arg = sorted(partitions)[-1]
        logger.info("✅ Partição inferida: %s", partition_arg)
    except Exception as e:
        logger.error("❌ Erro ao inferir partição: %s", str(e))
        raise ValueError("Erro ao inferir partição.") from e

    return partition_arg


def _get_source_file_name(source_path: str) -> str:
    files = glob.glob(os.path.join(source_path, "*.xls*"))

    if not files:
        raise FileNotFoundError(f"Nenhum Excel local: {source_path}")

    return files[0].split("/")[-1]


def _get_destination_path(year_month: str) -> str:
    destination_root = arg_util.get_arg(DEST_PATH_ARG)

    if not destination_root:
        logger.error("❌ Parâmetro de destino não fornecido. Use --%s.", DEST_PATH_ARG)
        raise ValueError("Caminho de destino não fornecido.")

    return os.path.join(destination_root, year_month)


def main():
    """Função principal do módulo de ingestão local."""
    spark = _get_spark_session()

    try:
        source_root = _get_source_root()
        year_month = _get_partition_arg(source_root)
        source_path = os.path.join(source_root, year_month)
        source_file_name = _get_source_file_name(source_path)
        destination_path = _get_destination_path(year_month)
    except ValueError as e:
        logger.error("❌ Erro de configuração: %s", e)
        return

    try:
        _run_etl(spark, source_path, source_file_name, destination_path)
    except (IOError, RuntimeError) as e:
        logger.error("❌ Erro de execução ou IO: %s", e)
    except Exception as e:
        logger.exception("❌ Erro inesperado: %s", str(e))
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
