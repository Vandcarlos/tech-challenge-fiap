from datetime import datetime

import pytest

from cli import ingest as sut


def build_argv(
    data_source_path: str | None = None,
    data_target_path: str | None = None,
    year_month: str | None = None,
    use_fake: str | None = None,
) -> list[str]:
    args = ["script.py"]

    if data_source_path is not None:
        args.append(f"--{sut.DATA_SOURCE_PATH_ARG}")
        args.append(data_source_path)

    if data_target_path is not None:
        args.append(f"--{sut.DATA_TARGET_PATH_ARG}")
        args.append(data_target_path)

    if year_month is not None:
        args.append(f"--{sut.YEAR_MONTH_ARG}")
        args.append(year_month)

    if use_fake is not None:
        args.append(f"--{sut.USE_FAKE_DATA_ARG}")
        args.append(use_fake)

    return args


@pytest.mark.parametrize(("pass_year_month_arg", "use_fake_arg"), [(True, None), (False, "True")])
def test_main(pass_year_month_arg, use_fake_arg, spark_session, monkeypatch, tmp_path):
    monkeypatch.setattr("pyspark.sql.SparkSession.Builder.getOrCreate", lambda x: spark_session)

    year_month = datetime.now().strftime("%Y%m")

    data_source_path = tmp_path / "source"
    data_target_path = tmp_path / "target"

    year_month_arg = year_month if pass_year_month_arg else None

    argv = build_argv(data_source_path, data_target_path, year_month_arg, use_fake_arg)
    monkeypatch.setattr(sut.arg_util.sys, "argv", argv)

    def ingest_func(self, source_path, target_path, use_fake):
        assert source_path == data_source_path / year_month
        assert target_path == data_target_path / year_month
        assert use_fake is (False if use_fake_arg is None else use_fake_arg == "True")

    monkeypatch.setattr(sut.IngestService, "ingest", ingest_func)

    sut.main()


@pytest.mark.parametrize(
    ("data_source_path", "data_target_path"),
    [(None, None), ("data_source_path", None)],
)
def test_input_errors(data_source_path, data_target_path, monkeypatch):
    argv = build_argv(data_source_path, data_target_path)
    monkeypatch.setattr(sut.arg_util.sys, "argv", argv)
    with pytest.raises(ValueError):
        sut.main()


@pytest.mark.parametrize(
    "error",
    [
        IOError("Simulated IO error"),
        RuntimeError("Simulated RuntimeError"),
        Exception("Simulated unexpected error"),
    ],
)
def test_run_etl_error(error, monkeypatch):
    argv = build_argv("data_source_path", "data_target_path", "year_month_arg")
    monkeypatch.setattr(sut.arg_util.sys, "argv", argv)

    def raise_error(self, x, y, z):
        raise error

    monkeypatch.setattr(sut.IngestService, "ingest", raise_error)

    with pytest.raises(type(error), match=error.args[0]):
        sut.main()
