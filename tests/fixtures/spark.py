import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session():
    spark = (
        SparkSession.builder.master("local[1]")
        .appName("PyTest-Spark-Local")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.ui.enabled", "false")
        .config("spark.driver.host", "localhost")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    yield spark

    spark.stop()


@pytest.fixture(autouse=True)
def protect_spark_stop(spark_session, monkeypatch):
    """Automatically prevents spark.stop() from working during tests."""
    monkeypatch.setattr(spark_session, "stop", lambda: None)
