from mlflow import artifacts as mlflow_artifacts
from mlflow.tracking import MlflowClient

from src import env
from src.core.modules import PredictorModule


class ProductionPredictor:
    _instance = None
    _module: PredictorModule | None
    _metadata = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._setup_production_assets()
        return cls._instance

    @classmethod
    def _setup_production_assets(cls):
        base_metada: dict[str, str | None] = {
            "name": env.MLFLOW_MODEL_NAME,
            "version": env.PREDICT_MODEL_VERSION,
            "model_path": str(env.PREDICT_MODELS_PATH / env.PREDICT_MODEL_VERSION),
            "engine": "ONNX",
        }
        try:
            model_path = env.PREDICT_MODELS_PATH / env.PREDICT_MODEL_VERSION
            model_path.mkdir(parents=True, exist_ok=True)

            model_version_info = MlflowClient().get_model_version_by_alias(
                env.MLFLOW_MODEL_NAME, env.PREDICT_MODEL_VERSION
            )

            run_id = model_version_info.run_id

            if not (model_path / env.MODEL_NAME).exists():
                mlflow_artifacts.download_artifacts(
                    artifact_uri=f"models:/{env.MLFLOW_MODEL_NAME}@{env.PREDICT_MODEL_VERSION}",
                    dst_path=str(model_path),
                )

            if not (model_path / env.PREPROCESSOR_NAME).exists():
                mlflow_artifacts.download_artifacts(
                    run_id=run_id,
                    artifact_path=env.PREPROCESSOR_NAME,
                    dst_path=str(model_path),
                )

            cls._module = PredictorModule(
                artifacats_path=env.PREDICT_MODELS_PATH,
                preprocessor_name=env.PREPROCESSOR_NAME,
                model_name=env.MODEL_NAME,
            )
            base_metada["status"] = "ready"
            base_metada["error"] = None
        except Exception as e:
            base_metada["status"] = "error"
            base_metada["error"] = f"Model failed to load: {str(e)}"

            cls._module = None

        cls._metadata = base_metada

    def predict(self, input_df):
        if self._module is None:
            raise ValueError("Modelo não disponível")

        return self._module.predict(
            version=env.PREDICT_MODEL_VERSION,
            input=input_df,
        )

    @classmethod
    def get_metadata(cls):
        return cls._metadata
