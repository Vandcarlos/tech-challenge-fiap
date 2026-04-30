from dataclasses import dataclass

import torch

from .transformer import Transformer


@dataclass
class Tensors:
    X_train: torch.Tensor
    y_train: torch.Tensor
    X_val: torch.Tensor
    y_val: torch.Tensor
    X_test: torch.Tensor
    y_test: torch.Tensor

    def __init__(self, transformer: Transformer):
        self.X_train = torch.tensor(transformer.X_train, dtype=torch.float32)
        self.y_train = torch.tensor(transformer.y_train.values, dtype=torch.float32).view(-1, 1)

        self.X_val = torch.tensor(transformer.X_val, dtype=torch.float32)
        self.y_val = torch.tensor(transformer.y_val.values, dtype=torch.float32).view(-1, 1)

        self.X_test = torch.tensor(transformer.X_test, dtype=torch.float32)
        self.y_test = torch.tensor(transformer.y_test.values, dtype=torch.float32).view(-1, 1)
