import requests

base_url = "https://store.steampowered.com/api"

urls = {
    "details": "/appdetails",
    "search": "/storesearch"
}

def steam_request(location, params={}):
    full_url = base_url + location
    response = requests.get(full_url, params={"l": "english", "cc": "us", **params})
    parsed = response.json()
    
    return parsed