"""
Módulo de transformação de dados.
- mapeia colunas para nomes mais padronizados
- remove colunas irrelevantes
- ajusta o campo TotalCharges
"""

import logging
import os

import pandas as pd
import pandera.pyspark as pa
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import DoubleType, IntegerType, StringType, StructField, StructType

from data_ingest import logger_util
from data_ingest.domain import TelecomSource, TelecomTarget

logger = logging.getLogger(__name__)
logger_util.configure_logging()

RAW_SCHEMA = StructType(
    [
        StructField("Gender", StringType(), True),
        StructField("Senior Citizen", StringType(), True),
        StructField("Partner", StringType(), True),
        StructField("Dependents", StringType(), True),
        StructField("Phone Service", StringType(), True),
        StructField("Multiple Lines", StringType(), True),
        StructField("Internet Service", StringType(), True),
        StructField("Online Security", StringType(), True),
        StructField("Online Backup", StringType(), True),
        StructField("Device Protection", StringType(), True),
        StructField("Tech Support", StringType(), True),
        StructField("Streaming TV", StringType(), True),
        StructField("Streaming Movies", StringType(), True),
        StructField("Contract", StringType(), True),
        StructField("Paperless Billing", StringType(), True),
        StructField("Payment Method", StringType(), True),
        StructField("Tenure Months", IntegerType(), True),
        StructField("Monthly Charges", DoubleType(), True),
        StructField("Total Charges", StringType(), True),
    ]
)

MAPPING_COLUMNS = {
    "Gender": "gender",
    "Senior Citizen": "senior_citizen",
    "Partner": "partner",
    "Dependents": "dependents",
    "Phone Service": "phone_service",
    "Multiple Lines": "multiple_lines",
    "Internet Service": "internet_service",
    "Online Security": "online_security",
    "Online Backup": "online_backup",
    "Device Protection": "device_protection",
    "Tech Support": "tech_support",
    "Streaming TV": "streaming_tv",
    "Streaming Movies": "streaming_movies",
    "Contract": "contract",
    "Paperless Billing": "paperless_billing",
    "Payment Method": "payment_method",
    "Tenure Months": "tenure_months",
    "Monthly Charges": "monthly_charges",
    "Total Charges": "total_charges",
}

FOOTER_SKIP_ROWS = 1


def _get_pandas_df_from_excel(source_path: str) -> pd.DataFrame:
    df_excel = pd.read_excel(source_path, skipfooter=FOOTER_SKIP_ROWS, dtype={"Total Charges": str})
    df_excel.columns = df_excel.columns.str.strip()

    TelecomSource.validate(df_excel)

    cols_to_use = [field.name for field in RAW_SCHEMA.fields]
    df_excel = df_excel[cols_to_use].copy()
    return df_excel


def _map_columns(df: DataFrame) -> DataFrame:
    selected_cols = [col(original).alias(new) for original, new in MAPPING_COLUMNS.items()]

    return df.select(selected_cols)


def _data_wrangling(df: DataFrame) -> DataFrame:
    # Total charges
    df_wrangled = df.withColumn(
        "total_charges",
        when(col("total_charges") == " ", None).otherwise(col("total_charges").cast("double")),
    )
    return df_wrangled


@pa.check_output(TelecomTarget)
def transform_data(spark: SparkSession, source_path: str, file_name: str) -> DataFrame:
    """
    Transforma os dados lidos de um arquivo Parquet aplicando uma série de transformações.
    Esta função lê um DataFrame do Spark a partir de um caminho de arquivo Parquet especificado
    e aplica transformações sequenciais:
        - remoção de colunas irrelevantes com mapeamento das colunas
        - ajuste dos dados
    Parâmetros:
        spark (SparkSession): A sessão do Spark utilizada para ler e processar os dados.
        source_path (str): O caminho para o arquivo Parquet de origem.
        file_name (str): O nome do arquivo a ser transformado.
    Retorna:
        DataFrame: O DataFrame transformado após a aplicação das operações de transformação.
    """

    source = os.path.join(source_path, file_name)

    logger.info("Reading Excel file via Pandas bridge...")
    df_excel = _get_pandas_df_from_excel(source)

    df = spark.createDataFrame(df_excel, schema=RAW_SCHEMA)

    transformed_df = df.transform(_map_columns).transform(_data_wrangling).coalesce(1)
    return transformed_df
