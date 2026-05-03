import os

import pandas as pd
import requests

path_kedro = r"C:\Users\eyala\Documents\Cytech\ING3 GIA\MLOps\purchase-predict"

dataset = pd.read_csv(os.path.join(path_kedro, "data", "03_primary", "primary.csv"))

dataset = dataset.drop(["user_session", "user_id", "purchased"], axis=1)

# response = requests.post(
#     "http://146.148.67.208/predict",
#     json=dataset.sample(n=10).to_json(),
# )

response = requests.post(
    "https://purchase-predict-api-102907634051.europe-west1.run.app/predict",
    json=dataset.sample(n=10).to_json(),
)
print(response.status_code)
print(response.json())