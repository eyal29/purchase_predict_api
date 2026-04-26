import os

import joblib
import mlflow
from mlflow.tracking import MlflowClient

ENV = os.getenv("ENV")
MLFLOW_REGISTRY_NAME = os.getenv("MLFLOW_REGISTRY_NAME")

# Le warning est déjà guardé par le fichier __init__.py, pas besoin de le répéter ici
mlflow.set_tracking_uri(os.getenv("MLFLOW_SERVER"))  # ty: ignore[invalid-argument-type]

import os

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.tracking import MlflowClient

ENV = os.getenv("ENV")
MLFLOW_REGISTRY_NAME = os.getenv("MLFLOW_REGISTRY_NAME")

mlflow.set_tracking_uri(os.getenv("MLFLOW_SERVER"))


class Model:
    def __init__(self):
        self.model = None
        self.transform_pipeline = None
        self.load_model()

    def load_model(self):
        client = MlflowClient()
        alias = ENV

        model_version = client.get_model_version_by_alias(
            MLFLOW_REGISTRY_NAME,
            alias,
        )

        artifact_uri = f"runs:/{model_version.run_id}/transform_pipeline.pkl"

        pipeline_path = mlflow.artifacts.download_artifacts(
            artifact_uri=artifact_uri
        )

        if pipeline_path is None:
            raise RuntimeError(
                f"Failed to download transform_pipeline.pkl for run_id={model_version.run_id}"
            )

        self.model = mlflow.sklearn.load_model(
            f"models:/{MLFLOW_REGISTRY_NAME}@{alias}"
        )

        self.transform_pipeline = joblib.load(pipeline_path)

    def predict(self, X: pd.DataFrame):
        if self.model is None:
            return None

        if self.transform_pipeline:
            for name, encoder in self.transform_pipeline.items():
                X[name] = X[name].astype("string").fillna("unknown")
                X[name] = encoder.transform(X[name])

        for col in ["user_id", "user_session", "purchased"]:
            if col in X.columns:
                X = X.drop(col, axis=1)

        return self.model.predict(X)