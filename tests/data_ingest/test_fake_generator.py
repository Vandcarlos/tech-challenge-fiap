import pytest

from data_ingest import fake_generator as sut


@pytest.fixture
def setup_args(monkeypatch):
    def setup(year_month: str | None, destination_path: str | None):
        args = ["script.py"]

        if year_month is not None:
            args.append(f"--{sut.PARTITION_ARG}")
            args.append(year_month)

        if destination_path is not None:
            args.append(f"--{sut.DEST_PATH_ARG}")
            args.append(destination_path)

        monkeypatch.setattr("sys.argv", args)

    return setup


def test_generate_fake_data(setup_args, tmp_path):
    dest_dir = tmp_path / "fake_dir"
    year_month = "2024-06"

    setup_args(year_month=year_month, destination_path=str(dest_dir))

    sut.main()

    expected_path = dest_dir / year_month
    expected_file = expected_path / sut.FILE_FAKE_NAME

    assert expected_path.exists(), "O arquivo de dados sintéticos deve ser criado."
    assert expected_file.exists(), "O arquivo gerado deve ter o nome correto."


def test_generate_fake_data_missing_args(setup_args):
    setup_args(year_month=None, destination_path="/some/destination")
    with pytest.raises(ValueError, match="Parâmetro de partição não fornecido"):
        sut.main()

    setup_args(year_month="2024-06", destination_path=None)
    with pytest.raises(ValueError, match="Caminho de destino não fornecido"):
        sut.main()


def test_lambda_handler(monkeypatch, tmp_path):
    dest_dir = tmp_path / "fake_dir"
    year_month = "2024-06"

    monkeypatch.setenv(sut.DEST_PATH_LAMBDA_ENV, str(dest_dir))

    event = {sut.PARTITION_ARG: year_month}
    result = sut.lambda_handler(event, None)

    expected_path = dest_dir / year_month
    expected_file = expected_path / sut.FILE_FAKE_NAME

    assert result["status"] == "success", "O status retornado deve ser 'success'."
    assert expected_path.exists(), "O arquivo gerado pela Lambda deve existir."
    assert expected_file.exists(), "O arquivo gerado deve ter o nome correto."


def test_lambda_handler_missing_args():
    event = {}
    with pytest.raises(ValueError, match="Parâmetro de partição não fornecido"):
        sut.lambda_handler(event, None)

    event = {sut.PARTITION_ARG: "2024-06"}
    with pytest.raises(ValueError, match="Caminho de destino não fornecido"):
        sut.lambda_handler(event, None)
