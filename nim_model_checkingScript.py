import requests
import os
from dotenv import load_dotenv

load_dotenv()
nvidia_key = os.getenv('NVIDIA_NIM_KEY')
url = "https://integrate.api.nvidia.com/v1/models"

headers = {
    "Authorization": f"Bearer {nvidia_key}",
    "Accept": "application/json"
}

usable_model = []

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Iterate through the data and append model IDs to the list
    for model_info in data.get('data', []):
        model_id = model_info.get('id')
        if model_id:
            usable_model.append(model_id)

    print(f"Successfully found {len(usable_model)} models.")
    
    for model in usable_model:
        print(model)

except Exception as e:
    print(f"Failed to fetch models: {e}")