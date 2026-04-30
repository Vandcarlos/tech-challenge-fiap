"""
Módulo de transformação de dados.
- mapeia colunas para nomes mais padronizados
- remove colunas irrelevantes
- ajusta o campo TotalCharges
"""

import logging
from dataclasses import dataclass

import pandas as pd
import pandera.pyspark as pa
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.types import DoubleType, LongType, StringType, StructField, StructType

from core.utils import logger_util
from domain.telecon import TelecomPandasIn, TelecomSpark

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
        StructField("Tenure Months", LongType(), True),
        StructField("Monthly Charges", DoubleType(), True),
        StructField("Total Charges", StringType(), True),
        StructField("Churn Value", LongType(), True),
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
    "Churn Value": "churn_value",
}


@dataclass
class Transformer:
    spark_session: SparkSession

    @pa.check_output(TelecomSpark)
    def run_transform(self, df: pd.DataFrame) -> DataFrame:
        """
        Transforma os dados lidos de um arquivo Parquet aplicando uma série de transformações.
        Esta função lê um DataFrame do pandas, transforma em Spark e aplica transformações:
            - remoção de colunas irrelevantes com mapeamento das colunas
            - ajuste dos dados
        Parâmetros:
            df (pd.DataFrame): Dataframe Pandas da origem.
        Retorna:
            DataFrame: O DataFrame transformado após a aplicação das operações de transformação.
        """

        df_filterd = self._filter_source_df(df)

        df_spark = self.spark_session.createDataFrame(df_filterd, schema=RAW_SCHEMA)

        transformed_df = (
            df_spark.transform(self._map_columns).transform(self._data_wrangling).coalesce(1)
        )
        return transformed_df

    @pa.check_input(TelecomPandasIn)
    def _filter_source_df(self, df: pd.DataFrame) -> pd.DataFrame:
        cols_to_use = [field.name for field in RAW_SCHEMA.fields]
        df = df[cols_to_use].copy()
        return df

    def _map_columns(self, df: DataFrame) -> DataFrame:
        selected_cols = [col(original).alias(new) for original, new in MAPPING_COLUMNS.items()]

        return df.select(selected_cols)

    def _data_wrangling(self, df: DataFrame) -> DataFrame:
        df_wrangled = df.withColumn(
            "total_charges",
            when((col("total_charges") == " ") | (col("total_charges").isNull()), 0.0).otherwise(
                col("total_charges").cast("double")
            ),
        )
        return df_wrangled
