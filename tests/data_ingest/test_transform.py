import pandas as pd
import pytest

from data_ingest import fake_generator
from data_ingest import transform as sut


@pytest.fixture
def data_mock(monkeypatch, tmp_path) -> tuple[pd.DataFrame, str]:
    monkeypatch.setattr(fake_generator, "MIN_DEFAULT_FAKE_ROWS", 100)
    monkeypatch.setattr(fake_generator, "MAX_DEFAULT_FAKE_ROWS", 300)
    df = fake_generator._generate_data()
    path = fake_generator._save_data(df, tmp_path, "2023-08")
    return df, path


def test_transform_data(spark, data_mock, tmp_path):
    df_mock, file_name = data_mock

    df = sut.transform_data(spark, tmp_path, file_name)

    assert df.count() == len(df_mock) - sut.FOOTER_SKIP_ROWS
    assert set(df.columns) == set(sut.MAPPING_COLUMNS.values())
