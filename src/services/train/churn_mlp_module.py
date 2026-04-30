import torch.nn as torch_nn


class ChurnMLPModule(torch_nn.Module):
    _layers: torch_nn.Sequential

    def __init__(self, input_dim: int):
        super(ChurnMLPModule, self).__init__()

        self._layers = torch_nn.Sequential(
            torch_nn.Linear(input_dim, 64),
            torch_nn.ReLU(),
            torch_nn.Linear(64, 32),
            torch_nn.ReLU(),
            torch_nn.Linear(32, 1),
            torch_nn.Sigmoid(),
        )

    def forward(self, x):
        return self._layers(x)
