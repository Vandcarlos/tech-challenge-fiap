from pathlib import Path
from typing import Any, cast

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import average_precision_score, classification_report, roc_auc_score

from domain.evaluation_metrics import EvaluationMetrics

from .predict import PredictorModule


class EvaluaterModule:
    artifacats_path: Path
    preprocessor_name: str
    model_name: str

    @staticmethod
    def evaluate_model(
        model: bytes | Path,
        preprocessor: ColumnTransformer,
        input: pd.DataFrame,
        true_probs: pd.Series,
    ) -> EvaluationMetrics:
        prediction_probs = PredictorModule.predict_model_probs(model, preprocessor, input)
        metrics = EvaluaterModule.build_metrics(true_probs, prediction_probs)
        return metrics

    @staticmethod
    def build_metrics(true_probs: pd.Series, prediction_probs: pd.Series) -> EvaluationMetrics:
        prediction_preds = (prediction_probs > 0.5).astype(int)
        report = classification_report(true_probs, prediction_preds, output_dict=True)
        report = cast(dict[str, Any], report)

        auc_roc = roc_auc_score(true_probs, prediction_probs)
        pr_auc = average_precision_score(true_probs, prediction_probs)

        metrics = EvaluationMetrics(
            accuracy=report.get("accuracy", 0.0),
            precision=report.get("weighted avg", {}).get("precision", 0.0),
            recall=report.get("weighted avg", {}).get("recall", 0.0),
            f1_score=report.get("weighted avg", {}).get("f1-score", 0.0),
            auc_roc=cast(float, auc_roc),
            pr_auc=cast(float, pr_auc),
        )

        return metrics

    @property
    def predictor(self) -> PredictorModule:
        predictor = PredictorModule(
            artifacats_path=self.artifacats_path,
            preprocessor_name=self.preprocessor_name,
            model_name=self.model_name,
        )
        return predictor

    def evaluate(
        self, version: str, input: pd.DataFrame, true_probs: pd.Series
    ) -> EvaluationMetrics:
        prediction_probs = self.predictor.predict_probs(version, input)
        metrics = EvaluaterModule.build_metrics(true_probs, prediction_probs)
        return metrics
