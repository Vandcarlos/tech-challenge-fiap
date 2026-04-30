import io
from dataclasses import dataclass
from typing import Any

import torch
import torch.nn as torch_nn
import torch.optim as torch_optim
from torch.utils.data import DataLoader, TensorDataset

from .churn_mlp_module import ChurnMLPModule
from .tensors import Tensors

TRAIN_BATCH_SIZE = 32
TRAIN_NUM_EPOCHS = 100
LOSS_PATIENCE = 10


@dataclass
class Trainer:
    tensors: Tensors

    def __post_init__(self):
        self._input_dim = self.tensors.X_train.shape[1]
        self._loss_criterion = torch_nn.BCELoss()
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self._train_loader = DataLoader(
            TensorDataset(self.tensors.X_train, self.tensors.y_train),
            batch_size=TRAIN_BATCH_SIZE,
            shuffle=True,
        )

    def run_train(self) -> bytes:
        best_model_state = self.__run_loop()
        onnx_file = self.__generate_onnx(best_model_state)
        return onnx_file

    @property
    def module(self) -> ChurnMLPModule:
        return ChurnMLPModule(self._input_dim).to(self._device)

    def __run_loop(self) -> dict[str, Any]:
        module = self.module
        optimizer = torch_optim.Adam(module.parameters(), lr=0.001)
        best_loss = float("inf")
        counter = 0

        best_model_state: dict[str, Any] = {}

        for epoch in range(TRAIN_NUM_EPOCHS):
            module.train()
            epoch_loss = 0.0

            for inputs, labels in self._train_loader:
                inputs, labels = inputs.to(self._device), labels.to(self._device)
                optimizer.zero_grad()
                outputs = module(inputs)
                loss = self._loss_criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

            avg_train_loss = epoch_loss / len(self._train_loader)
            print(f"Epoch {epoch + 1}/{TRAIN_NUM_EPOCHS}, Loss: {avg_train_loss:.4f}")

            module.eval()
            with torch.no_grad():
                X_val = self.tensors.X_val.to(self._device)
                y_val = self.tensors.y_val.to(self._device)
                val_outputs = module(X_val)
                val_loss = self._loss_criterion(val_outputs, y_val).item()
                # mlflow.log_metric("val_loss", val_loss, step=epoch)

            if val_loss < best_loss:
                best_loss = val_loss
                counter = 0
                best_model_state = module.state_dict().copy()
            else:
                counter += 1
                if counter >= LOSS_PATIENCE:
                    print(f"Early stopping na época {epoch}. Best Val Loss: {best_loss:.4f}")
                    break

        return best_model_state

    def __generate_onnx(self, best_model_state: dict[str, Any]) -> bytes:
        module = self.module
        module.load_state_dict(best_model_state)
        module.eval()

        dummy_input = torch.randn(TRAIN_BATCH_SIZE, self._input_dim).to(self._device)

        buffer = io.BytesIO()
        torch.onnx.export(
            module,
            dummy_input,
            buffer,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=["input"],
            output_names=["output"],
            dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
        )

        return buffer.getvalue()
