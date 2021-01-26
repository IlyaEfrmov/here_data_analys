import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import geojson
import re

ROOT_URL = "https://astanapark.kz/api/2.41/"
OPTIONS = ["terminals", "parkomats"]

def get_data (option=None):
    if option is None:
        return False

    response = requests.get(ROOT_URL + option)
    return response.json()[option]

def save_data (option, data=None):
    if data is None:
        return False

    with open(option + '.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True
    
def to_geojson(data_frame, option):
    features = []

    for row in data_frame: 
        feature = {
            "type": "Feature",
            "properties": {
                'type': option,
                'address': row['address']["street"]["ru"] + ", " + row['address']["house"]["ru"],
                'name': row['description']["ru"] if option == "terminal" else row['description']["ru"].split(" |")[0] 
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row["location"]["coordinates"][0], row["location"]["coordinates"][1]]
            }
        }

        features.append(feature)
    
    featureCollection = {
        "type": "FeatureCollection",
        "features": features
    }

    return featureCollection

if __name__ == "__main__":

    for option in OPTIONS:
        data = get_data(option)
        geojson_data = to_geojson(data, option)

        if geojson_data:
            result = save_data(option, geojson_data)
            if result:
                print("Data successfully saved")
            else:
                print("Error while saving data")
