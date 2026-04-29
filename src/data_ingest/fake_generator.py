"""Gera dados fakes para simular a chegada de novos dados na camada bronze."""

import logging
import os

import numpy as np
import pandas as pd
import pandera.pyspark as pa

from data_ingest import arg_util, logger_util
from data_ingest.domain import telecom_source

logger_util.configure_logging()
logger = logging.getLogger(__name__)

DEST_PATH_ARG = "DESTINATION_PATH"
DEST_PATH_LAMBDA_ENV = "DESTINATION_PATH"
PARTITION_ARG = "YEAR_MONTH"
FILE_FAKE_NAME = "fake_telco_data.xlsx"
MIN_DEFAULT_FAKE_ROWS = 2000
MIN_FAKE_ROWS_ENV = "MIN_FAKE_ROWS"
MAX_DEFAULT_FAKE_ROWS = 5000
MAX_FAKE_ROWS_ENV = "MAX_FAKE_ROWS"


def _get_fake_rows_range() -> int:
    min_rows = int(os.getenv(MIN_FAKE_ROWS_ENV, MIN_DEFAULT_FAKE_ROWS))
    max_rows = int(os.getenv(MAX_FAKE_ROWS_ENV, MAX_DEFAULT_FAKE_ROWS))

    if min_rows < 1 or max_rows < 1:
        logger.warning(
            "Valores de linhas fakes inválidos (min: %d, max: %d). Usando valores padrão.",
            min_rows,
            max_rows,
        )
        min_rows = MIN_DEFAULT_FAKE_ROWS
        max_rows = MAX_DEFAULT_FAKE_ROWS

    if min_rows > max_rows:
        logger.warning(
            "Valor mínimo de linhas fakes (%d) é maior que o máximo (%d). Invertendo os valores.",
            min_rows,
            max_rows,
        )
        max_rows, min_rows = min_rows, max_rows

    return np.random.randint(min_rows, max_rows + 1)


@pa.check_output(telecom_source.TelecomSource)
def _generate_data() -> pd.DataFrame:
    n_rows = _get_fake_rows_range()

    churn_reasons = [
        "Competitor made better offer",
        "Service dissatisfaction",
        "Price too high",
        "Moved",
    ]

    city_options = ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "Fresno"]

    data = {
        "CustomerID": [f"{np.random.randint(1000, 9999)}-FAKE-{i:04d}" for i in range(n_rows)],
        "Count": [telecom_source.COUNT_VALUE] * n_rows,
        "Country": [telecom_source.COUNTRY_VALUE] * n_rows,
        "State": [telecom_source.STATE_VALUE] * n_rows,
        "City": np.random.choice(city_options, n_rows),
        "Zip Code": np.random.randint(
            telecom_source.ZIP_CODE_RANGE[0], telecom_source.ZIP_CODE_RANGE[1], n_rows
        ),
        "Lat Long": ["34.0522, -118.2437"] * n_rows,
        "Latitude": np.random.uniform(32.5, 42.0, n_rows),
        "Longitude": np.random.uniform(-124.0, -114.0, n_rows),
        "Gender": np.random.choice(telecom_source.GENDER_OPTIONS, n_rows),
        "Senior Citizen": np.random.choice(telecom_source.SENIOR_CITIZEN_OPTIONS, n_rows),
        "Partner": np.random.choice(telecom_source.PARTNER_OPTIONS, n_rows),
        "Dependents": np.random.choice(telecom_source.DEPENDENTS_OPTIONS, n_rows),
        "Tenure Months": np.random.randint(0, 73, n_rows),
        "Phone Service": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Multiple Lines": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Internet Service": np.random.choice(telecom_source.INTERNET_SERVICE_OPTIONS, n_rows),
        "Online Security": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Online Backup": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Device Protection": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Tech Support": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Streaming TV": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Streaming Movies": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Contract": np.random.choice(telecom_source.CONTRACT_OPTIONS, n_rows),
        "Paperless Billing": np.random.choice(telecom_source.PAPERLESS_BILLING_OPTIONS, n_rows),
        "Payment Method": np.random.choice(telecom_source.PAYMENT_METHOD_OPTIONS, n_rows),
        "Monthly Charges": np.random.uniform(18.0, 118.0, n_rows).round(2),
        "Total Charges": [
            " " if np.random.random() < 0.01 else str(round(np.random.uniform(20, 8000), 2))
            for _ in range(n_rows)
        ],
        "Churn Label": np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows),
        "Churn Value": np.random.choice(telecom_source.CHURN_VALUE_OPTIONS, n_rows),
        "Churn Score": np.random.randint(
            telecom_source.CHURN_SCORE_RANGE[0], telecom_source.CHURN_SCORE_RANGE[1] + 1, n_rows
        ),
        "CLTV": np.random.randint(2000, 6501, n_rows),
        "Churn Reason": [
            np.random.choice(churn_reasons) if val == "Yes" else None
            for val in np.random.choice(telecom_source.BOOLEAN_OPTIONS, n_rows)
        ],
    }

    df = pd.DataFrame(data)
    return df


def _save_data(df: pd.DataFrame, destination: str, year_month: str) -> str:
    file_path = os.path.join(destination, year_month, FILE_FAKE_NAME)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

    logger.info("✅ Dados fakes (33 colunas) gerados com sucesso: %s", file_path)
    logger.info("📊 Total de registros: %d", len(df))
    return file_path


def main():
    year_month = arg_util.get_arg(PARTITION_ARG)

    if not year_month:
        logger.error("❌ Parâmetro de partição não fornecido. Use --%s.", PARTITION_ARG)
        raise ValueError("Parâmetro de partição não fornecido.")

    destination = arg_util.get_arg(DEST_PATH_ARG)

    if not destination:
        logger.error("❌ Parâmetro de destino não fornecido. Use --%s.", DEST_PATH_ARG)
        raise ValueError("Caminho de destino não fornecido.")

    logger.info("Iniciando geração de dados sintéticos para %s...", year_month)
    df = _generate_data()
    _save_data(df, destination, year_month)


# Para suporte a Lambda
def lambda_handler(event, context):
    year_month = event.get(PARTITION_ARG)

    if not year_month:
        logger.error("❌ Parâmetro de partição não fornecido. Use --%s.", PARTITION_ARG)
        raise ValueError("Parâmetro de partição não fornecido.")

    destination = os.getenv(DEST_PATH_LAMBDA_ENV)

    if not destination:
        logger.error("❌ Parâmetro de destino não fornecido. Use --%s.", DEST_PATH_ARG)
        raise ValueError("Caminho de destino não fornecido.")

    df = _generate_data()
    file_path = _save_data(df, destination, year_month)
    return {"status": "success", "path": file_path}


if __name__ == "__main__":
    main()
