import pytest

from services.ingest import service as sut


@pytest.mark.parametrize("use_fake", [(False), (True)])
def test_run_etl(use_fake, spark_session, tmp_path):
    service = sut.IngestService(spark_session)

    source_path = tmp_path / "source"
    target_path = tmp_path / "target"

    service.ingest(source_path, target_path, use_fake=use_fake)

    assert target_path.exists()

    parquet_files = list(target_path.glob("**/*.parquet"))
    assert len(parquet_files) > 0

    df_result = spark_session.read.parquet(str(target_path))
    assert df_result.count() > 0


def test_run_etl_empty_data(spark_session, bronze_data_build, monkeypatch, tmp_path):
    def generate_empty_df(self, output_dir):
        bronze_data_build(min_rows=0, max_rows=0, target_path=output_dir)
        return output_dir

    monkeypatch.setattr(sut.ExtracterFake, "run_extract", generate_empty_df)
    service = sut.IngestService(spark_session)

    source_path = tmp_path / "source"
    target_path = tmp_path / "target"

    service.ingest(source_path, target_path, use_fake=True)
    df_result = spark_session.read.parquet(str(target_path))
    assert df_result.count() == 0
