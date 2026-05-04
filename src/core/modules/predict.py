import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import onnxruntime as ort
import pandas as pd
from sklearn.compose import ColumnTransformer

from domain.prediction import Prediction


@dataclass
class PredictorModule:
    artifacats_path: Path
    preprocessor_name: str
    model_name: str

    @staticmethod
    def predict_model_probs(
        model: bytes | Path, preprocessor: ColumnTransformer, input: pd.DataFrame
    ) -> pd.Series:
        model_session = ort.InferenceSession(model)

        processed_input = cast(np.ndarray, preprocessor.transform(input)).astype(np.float32)
        input_name = model_session.get_inputs()[0].name
        output_name = model_session.get_outputs()[0].name
        results = model_session.run([output_name], {input_name: processed_input})

        y_probs = np.array(results[0]).flatten()
        return pd.Series(y_probs, index=input.index)

    def predict(self, version: str, input: pd.DataFrame) -> list[Prediction]:
        y_probs = self.predict_probs(version, input)
        y_preds = (y_probs > 0.5).astype(int)

        predictions = [
            Prediction(is_churn=bool(p_val == 1), confiance=float(p_prob))
            for p_prob, p_val in zip(y_probs, y_preds)
        ]

        return predictions

    def predict_probs(self, version: str, input: pd.DataFrame) -> pd.Series:
        model_path = self.artifacats_path / version / self.model_name
        preprocessor = self.load_preprocessor(version)

        probs = PredictorModule.predict_model_probs(model_path, preprocessor, input)
        return probs

    def load_preprocessor(self, version: str) -> ColumnTransformer:
        with open(self.artifacats_path / version / self.preprocessor_name, "rb") as f:
            preprocessor = pickle.load(f)

        return preprocessor
