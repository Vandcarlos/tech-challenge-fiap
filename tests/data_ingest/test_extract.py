from pathlib import Path

import pytest

from data_ingest import extract as sut


@pytest.fixture(autouse=True)
def setup_kagglehub(monkeypatch):
    """Fixture para mockar a função dataset_download do kagglehub durante os testes."""

    def mock_dataset_download(dataset_id, output_dir):
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(sut.kagglehub, "dataset_download", mock_dataset_download)


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


def test_extract(setup_args, tmp_path):
    dest_dir = tmp_path / "destination"
    setup_args(year_month="2024-06", destination_path=str(dest_dir))
    # Chama a função main do módulo de extração
    sut.main()

    # Verifica se o diretório de destino foi criado (ou seja, a extração ocorreu)
    expected_path = dest_dir / "2024-06"
    assert expected_path.exists(), f"O diretório {expected_path} deve existir após a extração."


def test_extract_missing_args(setup_args):
    # Testa ausência do argumento de partição
    setup_args(year_month=None, destination_path="/some/destination")
    with pytest.raises(ValueError, match="Parâmetro de partição não fornecido"):
        sut.main()

    # Testa ausência do argumento de destino
    setup_args(year_month="2024-06", destination_path=None)
    with pytest.raises(ValueError, match="Caminho de destino não fornecido"):
        sut.main()


def test_extract_kagglehub_error(monkeypatch, setup_args):
    # Mocka a função dataset_download para simular um erro
    def mock_dataset_download(dataset_id, output_dir):
        raise Exception("Erro simulado do KaggleHub")

    monkeypatch.setattr(sut.kagglehub, "dataset_download", mock_dataset_download)

    setup_args(year_month="2024-06", destination_path="/some/destination")
    with pytest.raises(Exception, match="Erro simulado do KaggleHub"):
        sut.main()
