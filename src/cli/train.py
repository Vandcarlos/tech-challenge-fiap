import logging
from pathlib import Path

from core.utils import arg_util, logger_util
from services.train.service import TrainService

logger_util.configure_logging()
logger = logging.getLogger(__name__)

YEAR_MONTH_ARG = "YEAR_MONTH"
DATA_SOURCE_PATH_ARG = "SOURCE_PATH"
DATA_TARGET_PATH_ARG = "TARGET_PATH"
ARTIFACTS_TARGET_PATH_ARG = "ARTIFACTS_PATH"


class InputArgs:
    _year_month: str
    _data_source_path: Path
    _data_target_path: Path
    _artifacts_target_path: Path

    @property
    def data_source_path(self) -> Path:
        return self._data_source_path / self._year_month

    @property
    def data_target_path(self) -> Path:
        return self._data_target_path / self._year_month

    @property
    def artifacts_target_path(self) -> Path:
        return self._artifacts_target_path / self._year_month

    def __init__(self):
        data_source = arg_util.get_arg(DATA_SOURCE_PATH_ARG)
        data_target_path = arg_util.get_arg(DATA_TARGET_PATH_ARG)
        artifacts_target_path = arg_util.get_arg(ARTIFACTS_TARGET_PATH_ARG)

        if not data_source or not data_target_path or not artifacts_target_path:
            raise ValueError("❌ Algum dos paths não foram forcenidos")

        self._data_source_path = Path(data_source)
        self._data_target_path = Path(data_target_path)
        self._artifacts_target_path = Path(artifacts_target_path)

        year_month = arg_util.get_arg(YEAR_MONTH_ARG)

        if year_month is None:
            year_month = arg_util.define_year_month(self._data_source_path)

        self._year_month = year_month


def main():
    """Função principal do módulo de ingestão local."""

    try:
        input_args = InputArgs()
    except ValueError as e:
        logger.error("❌ Erro de configuração: %s", e)
        raise e

    try:
        train_service = TrainService()
        train_service.train(
            data_source_path=input_args.data_source_path,
            data_target_path=input_args.data_target_path,
            artifacts_target_path=input_args.artifacts_target_path,
        )
    except Exception as e:
        logger.exception("❌ Erro treinamento: %s", str(e))
        raise e


if __name__ == "__main__":
    main()
