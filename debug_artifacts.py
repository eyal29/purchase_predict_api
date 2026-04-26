import os
import mlflow
from mlflow.tracking import MlflowClient
from dotenv import load_dotenv

load_dotenv()

mlflow.set_tracking_uri(os.getenv("MLFLOW_SERVER"))

run_id = "2ab8c24eb06a4c8793ccc4f07dcf6e7d"

client = MlflowClient()
artifacts = client.list_artifacts(run_id)

print("Artifacts à la racine :")
for artifact in artifacts:
    print(artifact.path)