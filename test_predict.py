import os

import pandas as pd
import requests

path_kedro = r"C:\Users\eyala\Documents\Cytech\ING3 GIA\MLOps\purchase-predict"

dataset = pd.read_csv(os.path.join(path_kedro, "data", "03_primary", "primary.csv"))

dataset = dataset.drop(["user_session", "user_id", "purchased"], axis=1)

response = requests.post(
    "http://127.0.0.1:5001/predict",
    json=dataset.sample(n=10).to_json(),
)

print(response.status_code)
print(response.json())