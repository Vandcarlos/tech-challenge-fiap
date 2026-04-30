"""Carrega os dados de um determinado path"""

import glob
import logging
from pathlib import Path

import pandas as pd
import pandera.pandas as pa

from core.utils import logger_util
from domain.telecon import TelecomPandasIn

logger_util.configure_logging()
logger = logging.getLogger(__name__)


DEFAULT_FOOTER_SKIP_ROWS = 1


class Loader:
    footer_skip_rows: int = DEFAULT_FOOTER_SKIP_ROWS

    @pa.check_output(TelecomPandasIn)
    def run_load(self, source_path: Path) -> pd.DataFrame:
        files_pattern = source_path / "*.xlsx"
        files_source = glob.glob(str(files_pattern))

        df = pd.concat([self._read_excel(Path(fs)) for fs in files_source])
        return df

    def _read_excel(self, source_path: Path) -> pd.DataFrame:
        df = pd.read_excel(
            source_path, skipfooter=self.footer_skip_rows, dtype={"Total Charges": str}
        )
        return df
