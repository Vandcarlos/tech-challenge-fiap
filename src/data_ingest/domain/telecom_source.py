import pandera.pandas as pa

COUNT_VALUE = 1
COUNTRY_VALUE = "United States"
STATE_VALUE = "California"
CITY_OPTIONS = ["Los Angeles", "San Diego", "San Jose", "San Francisco", "Sacramento"]
ZIP_CODE_RANGE = (90001, 96162)
GENDER_OPTIONS = ["Male", "Female"]
BOOLEAN_OPTIONS = ["Yes", "No"]
INTERNET_SERVICE_OPTIONS = ["No", "DSL", "Fiber optic", "Cable"]
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
    City: str = pa.Field(isin=CITY_OPTIONS)
    ZipCode: int = pa.Field(alias="Zip Code", ge=ZIP_CODE_RANGE[0], le=ZIP_CODE_RANGE[1])
    LatLong: str = pa.Field(alias="Lat Long")
    Latitude: float = pa.Field()
    Longitude: float = pa.Field()

    # Perfil do Cliente
    Gender: str = pa.Field(isin=GENDER_OPTIONS)
    SeniorCitizen: str = pa.Field(alias="Senior Citizen", isin=BOOLEAN_OPTIONS)
    Partner: str = pa.Field(isin=BOOLEAN_OPTIONS)
    Dependents: str = pa.Field(isin=BOOLEAN_OPTIONS)
    TenureMonths: int = pa.Field(alias="Tenure Months")

    # Serviços
    PhoneService: str = pa.Field(alias="Phone Service", isin=BOOLEAN_OPTIONS)
    MultipleLines: str = pa.Field(alias="Multiple Lines", isin=BOOLEAN_OPTIONS)
    InternetService: str = pa.Field(alias="Internet Service", isin=INTERNET_SERVICE_OPTIONS)
    OnlineSecurity: str = pa.Field(alias="Online Security", isin=BOOLEAN_OPTIONS)
    OnlineBackup: str = pa.Field(alias="Online Backup", isin=BOOLEAN_OPTIONS)
    DeviceProtection: str = pa.Field(alias="Device Protection", isin=BOOLEAN_OPTIONS)
    TechSupport: str = pa.Field(alias="Tech Support", isin=BOOLEAN_OPTIONS)
    StreamingTV: str = pa.Field(alias="Streaming TV", isin=BOOLEAN_OPTIONS)
    StreamingMovies: str = pa.Field(alias="Streaming Movies", isin=BOOLEAN_OPTIONS)

    # Contrato e Faturamento
    Contract: str = pa.Field(isin=CONTRACT_OPTIONS)
    PaperlessBilling: str = pa.Field(alias="Paperless Billing", isin=BOOLEAN_OPTIONS)
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
