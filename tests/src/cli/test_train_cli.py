from pathlib import Path

import pytest

from cli import train as sut


def build_args(
    source_path: str | None = None,
    target_path: str | None = None,
    artifacts_path: str | None = None,
    year_month: str | None = None,
) -> list[str]:
    args = ["script.py"]

    if source_path is not None:
        args.append(f"--{sut.DATA_SOURCE_PATH_ARG}")
        args.append(source_path)

    if target_path is not None:
        args.append(f"--{sut.DATA_TARGET_PATH_ARG}")
        args.append(target_path)

    if artifacts_path is not None:
        args.append(f"--{sut.ARTIFACTS_TARGET_PATH_ARG}")
        args.append(artifacts_path)

    if year_month is not None:
        args.append(f"--{sut.YEAR_MONTH_ARG}")
        args.append(year_month)

    return args


@pytest.mark.parametrize(
    ("data_source", "data_target", "artifacts", "year_month", "has_error", "has_content_on_source"),
    [
        (None, None, None, None, True, False),
        ("data_source", None, None, None, True, False),
        ("data_source", "data_target", None, None, True, False),
        ("data_source", "data_target", "artifacts", None, True, False),
        ("data_source", "data_target", "artifacts", None, False, True),
        ("data_source", "data_target", "artifacts", "year_month", False, False),
    ],
)
def test_input_args(
    data_source,
    data_target,
    artifacts,
    year_month,
    has_error,
    has_content_on_source,
    monkeypatch,
    tmp_path,
):
    if data_source is not None:
        data_source = str(tmp_path / data_source)
        Path(data_source).mkdir(parents=True, exist_ok=True)

    args = build_args(data_source, data_target, artifacts, year_month)
    monkeypatch.setattr("sys.argv", args)

    def fake_train(self, data_source_path, data_target_path, artifacts_target_path):
        pass

    monkeypatch.setattr(sut.TrainService, "train", fake_train)

    if has_content_on_source:
        content_path = Path(data_source) / "some_partition"
        content_path.mkdir(parents=True, exist_ok=True)

    if has_error:
        with pytest.raises(ValueError):
            sut.main()

    else:
        sut.main()
