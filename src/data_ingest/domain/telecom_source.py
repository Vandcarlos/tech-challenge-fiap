import pandera.pandas as pa

COUNT_VALUE = 1
COUNTRY_VALUE = "United States"
STATE_VALUE = "California"
ZIP_CODE_RANGE = (90001, 96162)
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
BOOLEAN_OPTIONS = ["Yes", "No"]
CONTRACT_OPTIONS = ["Month-to-month", "One year", "Two year"]
PAYMENT_METHOD_OPTIONS = [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)",
]
CHURN_VALUE_OPTIONS = [0, 1]
CHURN_SCORE_RANGE = (0, 100)


class TelecomSource(pa.DataFrameModel):
    """
    Schema Pandera para validar os dados crus (Raw) vindos do Excel.
    Reflete as 33 colunas geradas pelo fake_generator.
    """

    # Identificação e Localização
    CustomerID: str = pa.Field(alias="CustomerID")
    Count: int = pa.Field(eq=COUNT_VALUE)
    Country: str = pa.Field(eq=COUNTRY_VALUE)
    State: str = pa.Field(eq=STATE_VALUE)
    City: str = pa.Field()
    ZipCode: int = pa.Field(alias="Zip Code", ge=ZIP_CODE_RANGE[0], le=ZIP_CODE_RANGE[1])
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
    ChurnLabel: str = pa.Field(alias="Churn Label", isin=BOOLEAN_OPTIONS)
    ChurnValue: int = pa.Field(alias="Churn Value", isin=CHURN_VALUE_OPTIONS)
    ChurnScore: int = pa.Field(
        alias="Churn Score", ge=CHURN_SCORE_RANGE[0], le=CHURN_SCORE_RANGE[1]
    )
    CLTV: int = pa.Field(alias="CLTV")
    ChurnReason: str = pa.Field(alias="Churn Reason", nullable=True)

    class Config:
        strict = True
        coerce = False
