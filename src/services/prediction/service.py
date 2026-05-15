import pandas as pd
from fastapi import HTTPException

from src.domain.prediction import Prediction

from .predictor import ProductionPredictor


class PredictionService:
    _predictor: ProductionPredictor

    @staticmethod
    def warm_up_model():
        ProductionPredictor()

    @staticmethod
    def warm_down_model():
        ProductionPredictor._instance = None

    def __init__(self):
        self.predictor = ProductionPredictor()

    def predict(self, data: list[dict]) -> list[Prediction]:
        """
        Recebe uma lista de dicionários (JSON), converte para DataFrame,
        executa a predição e retorna os objetos de domínio.
        """
        df = pd.DataFrame(data)

        try:
            predictions = self.predictor.predict(df)

            return predictions
        except ValueError as e:
            raise HTTPException(
                status_code=503,
                detail="Prediction engine is currently unavailable (Model not loaded).",
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Error.",
            ) from e

    def get_model_metadata(self) -> dict:
        """Exporta os metadados do modelo que está servindo a aplicação."""
        return ProductionPredictor.get_metadata()
