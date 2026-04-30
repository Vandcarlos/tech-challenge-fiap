from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

DATASET_RANDOM_STATE = 42
DATASET_TEST_SIZE = 0.2
DATASET_VALIDATION_SIZE = 0.16  # 0.16 é 20% do restante após separar o teste
TORCH_TRAIN_BATCH_SIZE = 32
TARGET_COLUMN = "churn_value"


@dataclass
class Dataset:
    X_train: pd.DataFrame
    y_train: pd.Series
    X_val: pd.DataFrame
    y_val: pd.Series
    X_test: pd.DataFrame
    y_test: pd.Series

    def __init__(self, df: pd.DataFrame):
        X = df.drop(columns=[TARGET_COLUMN])
        y = df[TARGET_COLUMN]

        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X,
            y,
            test_size=DATASET_TEST_SIZE,
            random_state=DATASET_RANDOM_STATE,
        )

        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val,
            y_train_val,
            test_size=DATASET_VALIDATION_SIZE,
            random_state=DATASET_RANDOM_STATE,
        )

        self.X_train = X_train
        self.y_train = y_train
        self.X_val = X_val
        self.y_val = y_val
        self.X_test = X_test
        self.y_test = y_test
