from pathlib import Path

import pandas as pd
import pandera.pandas as pa

from domain import telecon


@pa.check_output(telecon.TelecomPandas)
def load_data(data_source_path: Path) -> pd.DataFrame:
    df = pd.read_parquet(data_source_path)
    return df
