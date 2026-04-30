import pandera.pandas as pa
import pandera.pyspark as pas
from pyspark.sql.types import DoubleType, LongType, StringType

GENDER_OPTIONS = ["Male", "Female"]
SENIOR_CITIZEN_OPTIONS = ["Yes", "No"]
PARTNER_OPTIONS = ["Yes", "No"]
DEPENDENTS_OPTIONS = ["Yes", "No"]
PHONE_SERVICE_OPTIONS = ["Yes", "No"]
MULTIPLE_LINES_OPTIONS = ["Yes", "No", "No phone service"]
INTERNET_SERVICE_OPTIONS = ["No", "DSL", "Fiber optic", "Cable"]
ONLINE_SECURITY_OPTIONS = ["Yes", "No", "No internet service"]
ONLINE_BACKUP_OPTIONS = ["Yes", "No", "No internet service"]
DEVICE_PROTECTION_OPTIONS = ["Yes", "No", "No internet service"]
TECH_SUPPORT_OPTIONS = ["Yes", "No", "No internet service"]
STREAMING_TV_OPTIONS = ["Yes", "No", "No internet service"]
STREAMING_MOVIES_OPTIONS = ["Yes", "No", "No internet service"]
PAPERLESS_BILLING_OPTIONS = ["Yes", "No"]
CONTRACT_OPTIONS = ["Month-to-month", "One year", "Two year"]
PAYMENT_METHOD_OPTIONS = [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)",
]
CHURN_VALUE_OPTIONS = [0, 1]

# Only source options
COUNT_VALUE_OPTION = 1
COUNTRY_VALUE_OPTION = "United States"
STATE_VALUE_OPTION = "California"
ZIP_CODE_RANGE_OPTION = (90001, 96162)
CHURN_LABEL_OPTIONS = ["Yes", "No"]
CHURN_SCORE_RANGE_OPTION = (0, 100)


class TelecomPandas(pa.DataFrameModel):
    # Identificação
    gender: str = pa.Field(isin=GENDER_OPTIONS)
    senior_citizen: str = pa.Field(isin=SENIOR_CITIZEN_OPTIONS)
    partner: str = pa.Field(isin=PARTNER_OPTIONS)
    dependents: str = pa.Field(isin=DEPENDENTS_OPTIONS)

    # Métricas de tempo
    tenure_months: int = pa.Field(ge=0)

    # Serviços (padronizados)
    phone_service: str = pa.Field(isin=PHONE_SERVICE_OPTIONS)
    multiple_lines: str = pa.Field(isin=MULTIPLE_LINES_OPTIONS)
    internet_service: str = pa.Field(isin=INTERNET_SERVICE_OPTIONS)
    online_security: str = pa.Field(isin=ONLINE_SECURITY_OPTIONS)
    online_backup: str = pa.Field(isin=ONLINE_BACKUP_OPTIONS)
    device_protection: str = pa.Field(isin=DEVICE_PROTECTION_OPTIONS)
    tech_support: str = pa.Field(isin=TECH_SUPPORT_OPTIONS)
    streaming_tv: str = pa.Field(isin=STREAMING_TV_OPTIONS)
    streaming_movies: str = pa.Field(isin=STREAMING_MOVIES_OPTIONS)

    # Faturamento
    contract: str = pa.Field(isin=CONTRACT_OPTIONS)
    paperless_billing: str = pa.Field(isin=PAPERLESS_BILLING_OPTIONS)
    payment_method: str = pa.Field(isin=PAYMENT_METHOD_OPTIONS)
    monthly_charges: float = pa.Field(ge=0)
    total_charges: float = pa.Field(nullable=True, ge=0)

    # Target
    churn_value: int = pa.Field(isin=CHURN_VALUE_OPTIONS)


class TelecomSpark(pas.DataFrameModel):
    gender: StringType = pa.Field(isin=GENDER_OPTIONS)
    senior_citizen: StringType = pa.Field(isin=SENIOR_CITIZEN_OPTIONS)
    partner: StringType = pa.Field(isin=PARTNER_OPTIONS)
    dependents: StringType = pa.Field(isin=DEPENDENTS_OPTIONS)

    # Métricas de tempo
    tenure_months: LongType = pa.Field(ge=0)

    # Serviços (padronizados)
    phone_service: StringType = pa.Field(isin=PHONE_SERVICE_OPTIONS)
    multiple_lines: StringType = pa.Field(isin=MULTIPLE_LINES_OPTIONS)
    internet_service: StringType = pa.Field(isin=INTERNET_SERVICE_OPTIONS)
    online_security: StringType = pa.Field(isin=ONLINE_SECURITY_OPTIONS)
    online_backup: StringType = pa.Field(isin=ONLINE_BACKUP_OPTIONS)
    device_protection: StringType = pa.Field(isin=DEVICE_PROTECTION_OPTIONS)
    tech_support: StringType = pa.Field(isin=TECH_SUPPORT_OPTIONS)
    streaming_tv: StringType = pa.Field(isin=STREAMING_TV_OPTIONS)
    streaming_movies: StringType = pa.Field(isin=STREAMING_MOVIES_OPTIONS)

    # Faturamento
    contract: StringType = pa.Field(isin=CONTRACT_OPTIONS)
    paperless_billing: StringType = pa.Field(isin=PAPERLESS_BILLING_OPTIONS)
    payment_method: StringType = pa.Field(isin=PAYMENT_METHOD_OPTIONS)
    monthly_charges: DoubleType = pa.Field(ge=0)
    total_charges: DoubleType = pa.Field(nullable=True, ge=0)

    # Target
    churn_value: LongType = pa.Field(isin=CHURN_VALUE_OPTIONS)

    class Config:
        strict = True
        coerce = True


class TelecomPandasIn(pa.DataFrameModel):
    """
    Schema Pandera para validar os dados crus (Raw) vindos do Excel.
    Reflete as 33 colunas geradas pelo fake_generator.
    """

    # Identificação e Localização
    CustomerID: str = pa.Field(alias="CustomerID")
    Count: int = pa.Field(eq=COUNT_VALUE_OPTION)
    Country: str = pa.Field(eq=COUNTRY_VALUE_OPTION)
    State: str = pa.Field(eq=STATE_VALUE_OPTION)
    City: str = pa.Field()
    ZipCode: int = pa.Field(
        alias="Zip Code", ge=ZIP_CODE_RANGE_OPTION[0], le=ZIP_CODE_RANGE_OPTION[1]
    )
    LatLong: str = pa.Field(alias="Lat Long")
    Latitude: float = pa.Field()
    Longitude: float = pa.Field()

    # Perfil do Cliente
    Gender: str = pa.Field(isin=GENDER_OPTIONS)
    SeniorCitizen: str = pa.Field(alias="Senior Citizen", isin=SENIOR_CITIZEN_OPTIONS)
    Partner: str = pa.Field(isin=PARTNER_OPTIONS)
    Dependents: str = pa.Field(isin=DEPENDENTS_OPTIONS)
    TenureMonths: int = pa.Field(alias="Tenure Months")

    # Serviços
    PhoneService: str = pa.Field(alias="Phone Service", isin=PHONE_SERVICE_OPTIONS)
    MultipleLines: str = pa.Field(alias="Multiple Lines", isin=MULTIPLE_LINES_OPTIONS)
    InternetService: str = pa.Field(alias="Internet Service", isin=INTERNET_SERVICE_OPTIONS)
    OnlineSecurity: str = pa.Field(alias="Online Security", isin=ONLINE_SECURITY_OPTIONS)
    OnlineBackup: str = pa.Field(alias="Online Backup", isin=ONLINE_BACKUP_OPTIONS)
    DeviceProtection: str = pa.Field(alias="Device Protection", isin=DEVICE_PROTECTION_OPTIONS)
    TechSupport: str = pa.Field(alias="Tech Support", isin=TECH_SUPPORT_OPTIONS)
    StreamingTV: str = pa.Field(alias="Streaming TV", isin=STREAMING_TV_OPTIONS)
    StreamingMovies: str = pa.Field(alias="Streaming Movies", isin=STREAMING_MOVIES_OPTIONS)

    # Contrato e Faturamento
    Contract: str = pa.Field(isin=CONTRACT_OPTIONS)
    PaperlessBilling: str = pa.Field(alias="Paperless Billing", isin=PAPERLESS_BILLING_OPTIONS)
    PaymentMethod: str = pa.Field(alias="Payment Method", isin=PAYMENT_METHOD_OPTIONS)

    MonthlyCharges: float = pa.Field(alias="Monthly Charges")
    TotalCharges: str = pa.Field(alias="Total Charges", nullable=True)

    # Churn e Métricas
    ChurnLabel: str = pa.Field(alias="Churn Label", isin=CHURN_LABEL_OPTIONS)
    ChurnValue: int = pa.Field(alias="Churn Value", isin=CHURN_VALUE_OPTIONS)
    ChurnScore: int = pa.Field(
        alias="Churn Score", ge=CHURN_SCORE_RANGE_OPTION[0], le=CHURN_SCORE_RANGE_OPTION[1]
    )
    CLTV: int = pa.Field(alias="CLTV")
    ChurnReason: str = pa.Field(alias="Churn Reason", nullable=True)

    class Config:
        strict = "filter"
        coerce = True
