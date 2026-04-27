import glob
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from data_ingest import local_job as sut


def mock_source_file(year_month: str, source_dir: Path) -> Path:
    file_path = source_dir / year_month / "data.xls"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch()
    return file_path


def build_args(
    year_month: str | None, source_path: str | None, destination_path: str | None
) -> list[str]:
    args = ["script.py"]

    if year_month is not None:
        args.append(f"--{sut.PARTITION_ARG}")
        args.append(year_month)

    if source_path is not None:
        args.append(f"--{sut.SOURCE_PATH_ARG}")
        args.append(source_path)

    if destination_path is not None:
        args.append(f"--{sut.DEST_PATH_ARG}")
        args.append(destination_path)

    return args


@pytest.mark.parametrize("pass_year_month_arg", [True, False])
def test_main(pass_year_month_arg, monkeypatch, tmp_path):
    spark_mock = MagicMock()
    monkeypatch.setattr("pyspark.sql.SparkSession.Builder.getOrCreate", lambda x: spark_mock)

    year_month = "2023-08"
    source_dir = tmp_path / "source"
    destination_dir = tmp_path / "destination"

    file_path = mock_source_file(year_month, source_dir)

    monkeypatch.setattr(
        "sys.argv",
        build_args(
            year_month if pass_year_month_arg else None, str(source_dir), str(destination_dir)
        ),
    )

    transform_data_mock = MagicMock()
    transform_data_mock.isEmpty.return_value = False

    def write_parquet(dest_path):
        assert dest_path == str(destination_dir / year_month)
        files = glob.glob(os.path.join(dest_path, "*.xls*"))

        assert len(files) == 1, "Deve haver exatamente um arquivo de origem processado."
        assert files[0] == str(file_path), "O arquivo processado deve ser o correto."
        return None

    transform_data_mock.write.mode.return_value.parquet.return_value = write_parquet
    monkeypatch.setattr(
        sut.transform,
        "transform_data",
        lambda spark, source_path, source_file_name: transform_data_mock,
    )

    sut.main()


def test_source_path_missing(monkeypatch):
    monkeypatch.setattr("sys.argv", build_args(None, None, None))

    with pytest.raises(ValueError, match="Caminho de origem não fornecido."):
        sut.main()


def test_no_partition_to_infer(monkeypatch, tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("sys.argv", build_args(None, str(source_dir), None))

    with pytest.raises(ValueError, match="Erro ao inferir partição."):
        sut.main()


def test_no_files_for_partition(monkeypatch, tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("sys.argv", build_args("2023-08", str(source_dir), None))

    with pytest.raises(FileNotFoundError, match="Nenhum Excel local"):
        sut.main()


def test_destination_path_missing(monkeypatch, tmp_path):
    source_dir = tmp_path / "source"
    mock_source_file("2023-08", source_dir)

    monkeypatch.setattr("sys.argv", build_args(None, str(source_dir), None))

    with pytest.raises(ValueError, match="Caminho de destino não fornecido."):
        sut.main()


@pytest.mark.parametrize(
    "erros",
    [
        IOError("Simulated IO error"),
        RuntimeError("Simulated RuntimeError"),
        Exception("Simulated unexpected error"),
    ],
)
def test_etl_error(erros, monkeypatch, tmp_path):
    source_dir = tmp_path / "source"
    mock_source_file("2023-08", source_dir)
    destination_dir = tmp_path / "destination"

    monkeypatch.setattr("sys.argv", build_args("2023-08", str(source_dir), str(destination_dir)))

    def raise_error(*args, **kwargs):
        raise erros

    transform_data_mock = MagicMock()
    transform_data_mock.isEmpty.return_value = False
    transform_data_mock.write.mode.return_value.parquet.side_effect = raise_error

    monkeypatch.setattr(
        sut.transform,
        "transform_data",
        lambda spark, source_path, source_file_name: transform_data_mock,
    )

    with pytest.raises(type(erros), match=erros.args[0]):
        sut.main()


def test_etl_empty_data(monkeypatch, tmp_path):
    source_dir = tmp_path / "source"
    mock_source_file("2023-08", source_dir)
    destination_dir = tmp_path / "destination"

    monkeypatch.setattr("sys.argv", build_args("2023-08", str(source_dir), str(destination_dir)))

    transform_data_mock = MagicMock()
    transform_data_mock.isEmpty.return_value = True

    monkeypatch.setattr(
        sut.transform,
        "transform_data",
        lambda spark, source_path, source_file_name: transform_data_mock,
    )

    sut.main()
