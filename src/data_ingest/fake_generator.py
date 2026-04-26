"""Gera dados fakes para simular a chegada de novos dados na camada bronze."""

import logging
import os

import numpy as np
import pandas as pd

from data_ingest import arg_util, logger_util

logger_util.configure_logging()
logger = logging.getLogger(__name__)

DEST_PATH_ARG = "DESTINATION_PATH"
DEST_PATH_LAMBDA_ENV = "DESTINATION_PATH"
PARTITION_ARG = "YEAR_MONTH"
ORIGIN_SAMPLE_PATH = "fake_sampling.xlsx"


def generate_data(path: str):
    """Gera o esquema completo de 33 colunas idêntico ao Kaggle."""
    n_rows = np.random.randint(2000, 5000)

    # Listas de categorias baseadas no seu sample
    cities = ["Los Angeles", "San Diego", "San Jose", "San Francisco", "Sacramento"]
    offers = ["None", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"]
    reasons = ["Competitor made better offer", "Service dissatisfaction", "Price too high", "Moved"]

    data = {
        # Identificadores e Localização
        "CustomerID": [f"{np.random.randint(1000, 9999)}-FAKE-{i:04d}" for i in range(n_rows)],
        "Count": [1] * n_rows,
        "Country": ["United States"] * n_rows,
        "State": ["California"] * n_rows,
        "City": np.random.choice(cities, n_rows),
        "Zip Code": np.random.randint(90001, 96162, n_rows),
        "Lat Long": ["34.0522, -118.2437"] * n_rows,  # Mock fixo para simplificar
        "Latitude": np.random.uniform(32.5, 42.0, n_rows),
        "Longitude": np.random.uniform(-124.0, -114.0, n_rows),
        # Demografia
        "Gender": np.random.choice(["Male", "Female"], n_rows),
        "Senior Citizen": np.random.choice(["No", "Yes"], n_rows),
        "Partner": np.random.choice(["Yes", "No"], n_rows),
        "Dependents": np.random.choice(["Yes", "No"], n_rows),
        # Serviços (Onde o Spark estava dando erro de 'DSL')
        "Tenure Months": np.random.randint(0, 73, n_rows),
        "Phone Service": np.random.choice(["Yes", "No"], n_rows),
        "Multiple Lines": np.random.choice(["No", "Yes", "No phone service"], n_rows),
        "Internet Service": np.random.choice(["DSL", "Fiber optic", "No"], n_rows),
        "Online Security": np.random.choice(["Yes", "No", "No internet service"], n_rows),
        "Online Backup": np.random.choice(["Yes", "No", "No internet service"], n_rows),
        "Device Protection": np.random.choice(["Yes", "No", "No internet service"], n_rows),
        "Tech Support": np.random.choice(["Yes", "No", "No internet service"], n_rows),
        "Streaming TV": np.random.choice(["Yes", "No", "No internet service"], n_rows),
        "Streaming Movies": np.random.choice(["Yes", "No", "No internet service"], n_rows),
        # Contrato e Faturamento
        "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n_rows),
        "Paperless Billing": np.random.choice(["Yes", "No"], n_rows),
        "Payment Method": np.random.choice(
            ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], n_rows
        ),
        "Monthly Charges": np.random.uniform(18.0, 118.0, n_rows).round(2),
        # Total Charges: Gerado como String para simular o comportamento real (incluindo o erro de espaço vazio)
        "Total Charges": [
            " " if np.random.random() < 0.01 else str(round(np.random.uniform(20, 8000), 2))
            for _ in range(n_rows)
        ],
        # Churn Status
        "Churn Label": np.random.choice(["No", "Yes"], n_rows),
        "Churn Value": np.random.choice([0, 1], n_rows),
        "Churn Score": np.random.randint(0, 101, n_rows),
        "CLTV": np.random.randint(2000, 6501, n_rows),
        "Churn Reason": [
            np.random.choice(reasons) if val == "Yes" else None
            for val in np.random.choice(["No", "Yes"], n_rows)
        ],  # Simplificado
    }

    df = pd.DataFrame(data)

    # Garante que a ordem das colunas seja exatamente a do seu sample
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_excel(path, index=False)

    logger.info("✅ Dados fakes (33 colunas) gerados com sucesso: %s", path)
    logger.info("📊 Total de registros: %d", len(df))


def main():
    year_month = arg_util.get_arg(PARTITION_ARG)

    if not year_month:
        logger.error("❌ Parâmetro de partição não fornecido. Use --%s.", PARTITION_ARG)
        raise ValueError("Parâmetro de partição não fornecido.")

    destination = arg_util.get_arg(DEST_PATH_ARG)

    if not destination:
        logger.error("❌ Parâmetro de destino não fornecido. Use --%s.", DEST_PATH_ARG)
        raise ValueError("Caminho de destino não fornecido.")

    file_path = os.path.join(destination, year_month, "fake_telco_data.xlsx")

    logger.info("Iniciando geração de dados sintéticos para %s...", year_month)
    generate_data(file_path)


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

    file_path = os.path.join(destination, year_month, "fake_data.xlsx")

    generate_data(file_path)
    return {"status": "success", "path": file_path}


if __name__ == "__main__":
    main()
