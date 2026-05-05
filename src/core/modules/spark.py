from pyspark.sql import SparkSession

from src import env


class SparkSessionX:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = (
                SparkSession.builder.appName(env.SPARK_SESSION_NAME)
                .config("spark.sql.shuffle.partitions", "5")
                .getOrCreate()
            )
        return cls._instance

    @classmethod
    def get_session(cls):
        return cls()
