import pandera.pyspark as pa
from pyspark.sql.types import DoubleType, IntegerType, StringType


class TelecomTarget(pa.DataFrameModel):
    """
    Schema final para validar os dados após a transformação.
    Reflete as colunas em snake_case e tipos convertidos.
    """

    # Identificação
    gender: StringType = pa.Field(isin=["Female", "Male"])
    senior_citizen: StringType = pa.Field(isin=["No", "Yes"])
    partner: StringType = pa.Field(isin=["Yes", "No"])
    dependents: StringType = pa.Field(isin=["Yes", "No"])

    # Métricas de tempo
    tenure_months: IntegerType = pa.Field(ge=0)

    # Serviços (padronizados)
    phone_service: StringType = pa.Field(isin=["Yes", "No"])
    multiple_lines: StringType = pa.Field(isin=["No", "Yes"])
    internet_service: StringType = pa.Field(isin=["No", "DSL", "Fiber optic", "Cable"])
    online_security: StringType = pa.Field(isin=["Yes", "No"])
    online_backup: StringType = pa.Field(isin=["Yes", "No"])
    device_protection: StringType = pa.Field(isin=["Yes", "No"])
    tech_support: StringType = pa.Field(isin=["Yes", "No"])
    streaming_tv: StringType = pa.Field(isin=["Yes", "No"])
    streaming_movies: StringType = pa.Field(isin=["Yes", "No"])

    # Faturamento
    contract: StringType = pa.Field(isin=["Month-to-month", "One year", "Two year"])
    paperless_billing: StringType = pa.Field(isin=["Yes", "No"])
    payment_method: StringType = pa.Field(
        isin=[
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)",
        ]
    )
    monthly_charges: DoubleType = pa.Field(ge=0)
    total_charges: DoubleType = pa.Field(nullable=True, ge=0)

    class Config:
        strict = True
        coerce = True
