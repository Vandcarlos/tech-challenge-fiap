from pathlib import Path

from core.modules.eval import EvaluaterModule

from .dataset import Dataset
from .loader import load_data
from .preprocessor import Preprocessor
from .tensors import Tensors
from .trainer import Trainer
from .writer import Writer


class TrainService:
    def train(self, data_source_path: Path, data_target_path: Path, artifacts_target_path: Path):
        # Prepara
        df = load_data(data_source_path)
        dataset = Dataset(df)
        preprocessor = Preprocessor(dataset)
        tensors = Tensors(preprocessor)
        trainer = Trainer(tensors)

        # Treina
        model = trainer.run_train()

        # Avalia
        model_evaluation = EvaluaterModule.evaluate_model(
            model, preprocessor.transformer, dataset.X_test, dataset.y_test
        )

        # Salva
        writer = Writer(data_target_path, artifacts_target_path)
        writer.write_data(dataset, model_evaluation)
        writer.write_artifacts(preprocessor, model)
