from pathlib import Path

from .dataset import Dataset
from .loader import load_data
from .tensors import Tensors
from .trainer import Trainer
from .transformer import Transformer
from .writer import Writer


class TrainService:
    def train(self, data_source_path: Path, data_target_path: Path, artifacts_target_path: Path):
        # Prepara
        df = load_data(data_source_path)
        dataset = Dataset(df)
        transformer = Transformer(dataset)
        tensors = Tensors(transformer)
        trainer = Trainer(tensors)

        # Treina
        model = trainer.run_train()

        # Avalia
        # TODO...

        # Salva
        writer = Writer(data_target_path, artifacts_target_path)
        writer.write_data(dataset)
        writer.write_artifacts(transformer.preprocessor, model)
