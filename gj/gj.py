import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import geojson
import re

URL = "https://corp.gloria-jeans.ru/store-locator?_ga=2.97319711.1410876870.1581940982-2071125492.1581940982&_gac=1.254019900.1581940982.EAIaIQobChMI856KqMXY5wIVCM53Ch0e3woIEAAYASAAEgJMwPD_BwE"

def update_location (feature_list):
    modified_feature_list = []

    for feature in feature_list:
        modified_feature = {
            'address': feature['data-address'],
            'lat': feature['data-latitude'],
            'lng': feature['data-longitude'],
            'name': feature['data-name'], 
            "workTime": feature['data-hours'],
        }

        modified_feature_list.append(modified_feature)
    
    return modified_feature_list

def get_data (url=None):
    if url is None:
        return False

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')

    feature_list = soup.findAll("div", {"class": "store"})

    updated_location_data = update_location(feature_list)

    return updated_location_data

def save_data (name, data=None):
    if data is None:
        return False

    with open(name + '.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True
    
def to_geojson(data_frame):
    features = []

    for row in data_frame: 
        feature = {
            "type": "Feature",
            "properties": {
                'workTime': row['workTime'],
                'address': row['address'],
                'name': row['name'],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row['lng'], row['lat']]
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
        result = save_data("data", geojson_data)
        if result:
            print("Data successfully saved")
        else:
            print("Error while saving data")