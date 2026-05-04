from pathlib import Path

import kagglehub
import pandas as pd
import pyspark.sql
import pytest

from domain.evaluation_metrics import EvaluationMetrics
from services.ingest import extract, transform
from services.train.dataset import Dataset
from services.train.writer import Writer


def make_and_ensure_file_path_exists(path: Path, extension: str) -> Path:
    final_path = path if path.suffix == extension else path / f"data.{extension}"
    Path(final_path).parent.mkdir(parents=True, exist_ok=True)
    return final_path


@pytest.fixture
def bronze_data_build(monkeypatch):
    def generate_data(
        min_rows: int | None = None, max_rows: int | None = None, target_path: Path | None = None
    ) -> pd.DataFrame:
        extracter = extract.extract_fake.ExtracterFake()
        extracter.min_rows = min_rows if min_rows is not None else 100
        extracter.max_rows = max_rows if max_rows is not None else 300

        df = extracter._generate_data()

        if target_path is not None:
            path = make_and_ensure_file_path_exists(target_path, "xlsx")
            df.to_excel(path)

        return df

    return generate_data


@pytest.fixture
def silver_data_build(bronze_data_build, spark_session):
    def generate_data(
        df_base: pd.DataFrame | None = None,
        target_path: Path | None = None,
        *,
        min_rows: int | None = None,
        max_rows: int | None = None,
    ) -> pyspark.sql.DataFrame:
        if df_base is None:
            df_base = bronze_data_build(min_rows, max_rows)

        assert df_base is not None
        df = transform.Transformer(spark_session).run_transform(df_base)

        if target_path is not None:
            path = make_and_ensure_file_path_exists(target_path, "parquet")
            df.toPandas().to_parquet(path)

        return df

    return generate_data


@pytest.fixture
def gold_data_build(silver_data_build, tmp_path):
    def generate_data(
        df_base: pd.DataFrame | None = None,
        metrics: EvaluationMetrics | None = None,
        target_path: Path | None = None,
        *,
        min_rows: int | None = None,
        max_rows: int | None = None,
    ) -> Dataset:
        if df_base is None:
            df_base = silver_data_build(min_rows, max_rows).toPandas()

        assert df_base is not None
        dataset = Dataset(df_base)

        if metrics is None:
            metrics = EvaluationMetrics(0, 0, 0, 0, 0, 0)

        if target_path is not None:
            Writer(target_path, tmp_path).write_data(dataset, metrics)

        return dataset

    return generate_data


@pytest.fixture(autouse=True)
def setup_kagglehub(monkeypatch, bronze_data_build):
    """Fixture para mockar a função dataset_download do kagglehub durante os testes."""

    def mock_dataset_download(dataset_id, output_dir):
        bronze_data_build(target_path=Path(output_dir))
        return output_dir

    monkeypatch.setattr(kagglehub, "dataset_download", mock_dataset_download)
