import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import geojson
import re

URL = "https://mts.ru/json/offices/points"

def update_location(feature_list):
    modified_feature_list = []

    for feature in feature_list:

        if feature['Latitude'] == 0 or feature['Longitude'] == 0: continue

        modified_feature = {
            'address': feature['Address'],
            'lat': feature['Longitude'],
            'lng': feature['Latitude'],
        }

        modified_feature_list.append(modified_feature)
    
    return modified_feature_list

def get_data (url=None):
    if url is None:
        return False

    response = requests.get(url)
    data = response.json()
    return update_location(data)

def save_data (data=None):
    if data is None:
        return False

    with open('data.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True
    
def to_geojson(data_frame):
    features = []

    for row in data_frame: 
        feature = {
            "type": "Feature",
            "properties": {
                'address': row["address"],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(row["lng"]), float(row["lat"])]
            }
        }

        features.append(feature)
    
    featureCollection = {
        "type": "FeatureCollection",
        "features": features
    }

    return featureCollection

if __name__ == "__main__":

    data = get_data(URL)
    geojson_data = to_geojson(data)

    if geojson_data:
        result = save_data(geojson_data)
        if result:
            print("Data successfully saved")
        else:
            print("Error while saving data")
