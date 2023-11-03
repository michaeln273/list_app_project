import requests

base_url = "https://store.steampowered.com/api"

urls = {
    "details": "/appdetails",
    "search": "/storesearch"
}

# Sends a get request to base steam api url plus the location passed to the function
# Each request requires the wanted language and country code as url parameters. This function automatically sends
# those parameters as well as the parameters passed to this function
def steam_request(location, params={}):
    full_url = base_url + location
    response = requests.get(full_url, params={"l": "english", "cc": "us", **params})
    parsed = response.json()
    
    return parsed
