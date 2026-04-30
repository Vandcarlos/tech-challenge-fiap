import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from pyspark.sql import DataFrame, SparkSession

from .extract import Extracter, ExtracterFake, ExtracterImp
from .load import Loader
from .transform import Transformer

logger = logging.getLogger(__name__)


@dataclass
class IngestService:
    spark_session: SparkSession

    def ingest(self, source_path: Path, target_path: Path, use_fake: bool = False) -> DataFrame:
        extracter: Extracter = ExtracterImp() if not use_fake else ExtracterFake()
        extract_path = self._extract(extracter, source_path)

        load_df = self._load(extract_path)

        transform_df = self._transform(load_df, target_path)

        return transform_df

    # ETL
    def _extract(self, extracter: Extracter, output_path: Path) -> Path:
        return extracter.run_extract(output_path)

    def _load(self, source_path: Path) -> pd.DataFrame:
        return Loader().run_load(source_path)

    def _transform(self, df_source: pd.DataFrame, output_path: Path) -> DataFrame:
        df = Transformer(self.spark_session).run_transform(df_source)

        if df.isEmpty():
            logger.warning("⚠️ DataFrame transformado está vazio.")

        if output_path is not None:
            logger.info("Escrevendo %d registros em: %s", df.count(), output_path)
            df.write.mode("overwrite").parquet(str(output_path))

        return df
