from dataclasses import dataclass


@dataclass
class EvaluationMetrics:
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    auc_roc: float
    pr_auc: float
