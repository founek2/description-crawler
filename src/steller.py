import requests

def get_place_by_id(id: str):
    res = requests.get(f"https://api.demo.steller.co/v1/places/internal/{id}")
    return res.json()