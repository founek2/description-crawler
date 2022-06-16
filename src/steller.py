import os
import requests

API_STELLER_PLACE_URL = os.environ.get('API_STELLER_PLACE_URL', "https://api.demo.steller.co/v1/places/internal")

def get_place_by_id(id: str):
    res = requests.get(f"{API_STELLER_PLACE_URL}/{id}")
    return res.json()