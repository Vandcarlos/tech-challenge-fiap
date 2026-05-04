import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .dataset import Dataset


class Preprocessor:
    X_train: np.ndarray | spmatrix
    y_train: pd.Series
    X_val: np.ndarray | spmatrix
    y_val: pd.Series
    X_test: np.ndarray | spmatrix
    y_test: pd.Series
    transformer: ColumnTransformer

    def __init__(self, dataset: Dataset):
        transformer = _build_transformer()

        X_train_processed = transformer.fit_transform(dataset.X_train)
        X_val_processed = transformer.transform(dataset.X_val)
        X_test_processed = transformer.transform(dataset.X_test)

        self.X_train = X_train_processed
        self.y_train = dataset.y_train
        self.X_val = X_val_processed
        self.y_val = dataset.y_val
        self.X_test = X_test_processed
        self.y_test = dataset.y_test
        self.transformer = transformer


def _build_transformer():
    categorical_features = [
        "gender",
        "senior_citizen",
        "partner",
        "dependents",
        "phone_service",
        "multiple_lines",
        "internet_service",
        "online_security",
        "online_backup",
        "device_protection",
        "tech_support",
        "streaming_tv",
        "streaming_movies",
        "contract",
        "paperless_billing",
        "payment_method",
    ]
    numeric_features = ["tenure_months", "monthly_charges", "total_charges"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_features),
        ]
    )

    return preprocessor
