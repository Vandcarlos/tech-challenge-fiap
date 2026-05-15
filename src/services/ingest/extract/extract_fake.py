"""Gera dados fakes para simular a chegada de novos dados na camada bronze."""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import pandera.pyspark as pa

from core.utils import logger_util
from domain import telecon

from .extract import Extracter

logger_util.configure_logging()
logger = logging.getLogger(__name__)


DEFAULT_MIN_ROWS = 2000
DEFAULT_MAX_ROWS = 5000
DEFAULT_FILE_NAME = "fake_telco_data.xlsx"


class ExtracterFake(Extracter):
    min_rows: int = DEFAULT_MIN_ROWS
    max_rows: int = DEFAULT_MAX_ROWS
    file_name: str = DEFAULT_FILE_NAME

    def run_extract(self, output_path: Path) -> Path:
        df = self._generate_data()

        self._save_data(df, output_path)

        return output_path

    @property
    def n_rows(self) -> int:
        n_rows = np.random.randint(self.min_rows, self.max_rows + 1)
        return n_rows

    @pa.check_output(telecon.TelecomPandasIn)
    def _generate_data(self) -> pd.DataFrame:
        n_rows = self.n_rows

        print("NUMERO DE LINHAS ", n_rows)

        churn_reasons = [
            "Competitor made better offer",
            "Service dissatisfaction",
            "Price too high",
            "Moved",
        ]

        city_options = ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "Fresno"]

        data = {
            "CustomerID": [f"{np.random.randint(1000, 9999)}-FAKE-{i:04d}" for i in range(n_rows)],
            "Count": [telecon.COUNT_VALUE_OPTION] * n_rows,
            "Country": [telecon.COUNTRY_VALUE_OPTION] * n_rows,
            "State": [telecon.STATE_VALUE_OPTION] * n_rows,
            "City": np.random.choice(city_options, n_rows),
            "Zip Code": np.random.randint(
                telecon.ZIP_CODE_RANGE_OPTION[0], telecon.ZIP_CODE_RANGE_OPTION[1], n_rows
            ),
            "Lat Long": ["34.0522, -118.2437"] * n_rows,
            "Latitude": np.random.uniform(32.5, 42.0, n_rows),
            "Longitude": np.random.uniform(-124.0, -114.0, n_rows),
            "Gender": np.random.choice(telecon.GENDER_OPTIONS, n_rows),
            "Senior Citizen": np.random.choice(telecon.SENIOR_CITIZEN_OPTIONS, n_rows),
            "Partner": np.random.choice(telecon.PARTNER_OPTIONS, n_rows),
            "Dependents": np.random.choice(telecon.DEPENDENTS_OPTIONS, n_rows),
            "Tenure Months": np.random.randint(0, 73, n_rows),
            "Phone Service": np.random.choice(telecon.PHONE_SERVICE_OPTIONS, n_rows),
            "Multiple Lines": np.random.choice(telecon.MULTIPLE_LINES_OPTIONS, n_rows),
            "Internet Service": np.random.choice(telecon.INTERNET_SERVICE_OPTIONS, n_rows),
            "Online Security": np.random.choice(telecon.ONLINE_SECURITY_OPTIONS, n_rows),
            "Online Backup": np.random.choice(telecon.ONLINE_BACKUP_OPTIONS, n_rows),
            "Device Protection": np.random.choice(telecon.DEPENDENTS_OPTIONS, n_rows),
            "Tech Support": np.random.choice(telecon.TECH_SUPPORT_OPTIONS, n_rows),
            "Streaming TV": np.random.choice(telecon.STREAMING_MOVIES_OPTIONS, n_rows),
            "Streaming Movies": np.random.choice(telecon.STREAMING_MOVIES_OPTIONS, n_rows),
            "Contract": np.random.choice(telecon.CONTRACT_OPTIONS, n_rows),
            "Paperless Billing": np.random.choice(telecon.PAPERLESS_BILLING_OPTIONS, n_rows),
            "Payment Method": np.random.choice(telecon.PAYMENT_METHOD_OPTIONS, n_rows),
            "Monthly Charges": np.random.uniform(18.0, 118.0, n_rows).round(2),
            "Total Charges": [
                " " if np.random.random() < 0.01 else str(round(np.random.uniform(20, 8000), 2))
                for _ in range(n_rows)
            ],
            "Churn Label": np.random.choice(telecon.CHURN_LABEL_OPTIONS, n_rows),
            "Churn Value": np.random.choice(telecon.CHURN_VALUE_OPTIONS, n_rows),
            "Churn Score": np.random.randint(
                telecon.CHURN_SCORE_RANGE_OPTION[0], telecon.CHURN_SCORE_RANGE_OPTION[1] + 1, n_rows
            ),
            "CLTV": np.random.randint(2000, 6501, n_rows),
            "Churn Reason": [
                np.random.choice(churn_reasons) if val == "Yes" else None
                for val in np.random.choice(telecon.CHURN_LABEL_OPTIONS, n_rows)
            ],
        }

        df = pd.DataFrame(data)
        return df

    def _save_data(self, df: pd.DataFrame, dest_path: Path):
        dest_path.mkdir(parents=True, exist_ok=True)
        file_path = dest_path / self.file_name

        df.to_excel(file_path, index=False)

        logger.info("✅ Dados fakes (33 colunas) gerados com sucesso: %s", file_path)
        logger.info("📊 Total de registros: %d", len(df))
