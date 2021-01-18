import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import geojson
import re

URL = "https://www.verno-info.ru/shops"

def get_data (url=None):
    
    if url is None:
        return False

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    scripts = soup.findAll("script")

    for index, script in enumerate(scripts):
        script_content = script.string
        
        if script_content is not None and "var shops =" in script_content:
            match = re.search(r"var shops = \[(.+)\]", str(script_content))
            data = json.loads(match.group(0).split('=')[1])

            return data
            

def save_data (data=None):
    if data is None:
        return False

    with open('verny.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True
    
def to_geojson(data_frame):
    features = []

    for row in data_frame: 
        feature = {
            "type": "Feature",
            "properties": {
                'address': row['address'],
                'worktime_weekdays': row['worktime_weekdays'],
                'worktime_weekends': row['worktime_weekends']
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            }
        }

        features.append(feature)
    
    featureCollection = {
        "type": "FeatureCollection",
        "features": features
    }

    return featureCollection

if __name__ == "__main__":
    data = get_data(url=URL)
    
    geojson_data = to_geojson(data)
    
    if geojson_data:
        result = save_data(geojson_data)
        if result:
            print("Data successfully saved")
        else:
            print("Error while saving data")