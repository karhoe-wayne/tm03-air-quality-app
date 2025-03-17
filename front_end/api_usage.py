import json
import requests

# Fetch the list of cities from API after formatting for better visuals 
def obtain_formatted_cities_list():
    url = "http://100.27.167.26:5001/formatted-cities"
    text = requests.get(url).text
    return json.loads(text)["data"]

# Fetch the data from a specific city according to the API (coordinates, pollutant level, etc.)
def obtain_data(keyword="kl"):
    url = "http://100.27.167.26:5001/city-data"
    headers = {"Content-Type": "application/json"}
    data = {"city": keyword}
    text = requests.post(url, headers=headers, data=json.dumps(data)).text
    return json.loads(text)

print(obtain_data('Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia'))