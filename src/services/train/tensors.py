from dataclasses import dataclass

import torch

from .preprocessor import Preprocessor


@dataclass
class Tensors:
    X_train: torch.Tensor
    y_train: torch.Tensor
    X_val: torch.Tensor
    y_val: torch.Tensor
    X_test: torch.Tensor
    y_test: torch.Tensor

    def __init__(self, preprocessor: Preprocessor):
        self.X_train = torch.tensor(preprocessor.X_train, dtype=torch.float32)
        self.y_train = torch.tensor(preprocessor.y_train.values, dtype=torch.float32).view(-1, 1)

        self.X_val = torch.tensor(preprocessor.X_val, dtype=torch.float32)
        self.y_val = torch.tensor(preprocessor.y_val.values, dtype=torch.float32).view(-1, 1)

        self.X_test = torch.tensor(preprocessor.X_test, dtype=torch.float32)
        self.y_test = torch.tensor(preprocessor.y_test.values, dtype=torch.float32).view(-1, 1)
