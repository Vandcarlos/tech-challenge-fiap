from dataclasses import dataclass


@dataclass
class Prediction:
    is_churn: bool
    confiance: float
