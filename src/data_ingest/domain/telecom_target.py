import pandera.pyspark as pa
from pyspark.sql.types import DoubleType, IntegerType, StringType

from . import telecom_source


class TelecomTarget(pa.DataFrameModel):
    """
    Schema final para validar os dados após a transformação.
    Reflete as colunas em snake_case e tipos convertidos.
    """

    # Identificação
    gender: StringType = pa.Field(isin=telecom_source.GENDER_OPTIONS)
    senior_citizen: StringType = pa.Field(isin=telecom_source.SENIOR_CITIZEN_OPTIONS)
    partner: StringType = pa.Field(isin=telecom_source.PARTNER_OPTIONS)
    dependents: StringType = pa.Field(isin=telecom_source.DEPENDENTS_OPTIONS)

    # Métricas de tempo
    tenure_months: IntegerType = pa.Field(ge=0)

    # Serviços (padronizados)
    phone_service: StringType = pa.Field(isin=telecom_source.PHONE_SERVICE_OPTIONS)
    multiple_lines: StringType = pa.Field(isin=telecom_source.MULTIPLE_LINES_OPTIONS)
    internet_service: StringType = pa.Field(isin=telecom_source.INTERNET_SERVICE_OPTIONS)
    online_security: StringType = pa.Field(isin=telecom_source.ONLINE_SECURITY_OPTIONS)
    online_backup: StringType = pa.Field(isin=telecom_source.ONLINE_BACKUP_OPTIONS)
    device_protection: StringType = pa.Field(isin=telecom_source.DEVICE_PROTECTION_OPTIONS)
    tech_support: StringType = pa.Field(isin=telecom_source.TECH_SUPPORT_OPTIONS)
    streaming_tv: StringType = pa.Field(isin=telecom_source.STREAMING_TV_OPTIONS)
    streaming_movies: StringType = pa.Field(isin=telecom_source.STREAMING_MOVIES_OPTIONS)

    # Faturamento
    contract: StringType = pa.Field(isin=telecom_source.CONTRACT_OPTIONS)
    paperless_billing: StringType = pa.Field(isin=telecom_source.PAPERLESS_BILLING_OPTIONS)
    payment_method: StringType = pa.Field(isin=telecom_source.PAYMENT_METHOD_OPTIONS)
    monthly_charges: DoubleType = pa.Field(ge=0)
    total_charges: DoubleType = pa.Field(nullable=True, ge=0)

    class Config:
        strict = True
        coerce = True
