import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import geojson
import re

URL = "https://gemotest.ru/"

def update_location(data):
    
    for i in range(len(data)):
        tmp = data[i]["geometry"]["coordinates"][0]
        data[i]["geometry"]["coordinates"][0] = data[i]["geometry"]["coordinates"][1]
        data[i]["geometry"]["coordinates"][1] = tmp

    return data

def get_cities (url=None):
    if url is None:
        return False

    result = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    items_list = soup.findAll("div", {"class": "city_list"})

    for item in items_list:
        cities_list = item.findAll("a")
        for city in cities_list:
            result.append(city["href"].split("=")[1])

    return result


def get_data (city, url=None):
    if url is None:
        return False

    response = requests.get(url + "/" + city + "/address")
    soup = BeautifulSoup(response.text, 'lxml')

    scripts = soup.findAll("script")

    for index, script in enumerate(scripts):
        script_content = script.string
    
        if script_content is not None and "var arMapObjects =" in script_content:
            script_content = script_content.replace("'", '"')
            match = re.search(r"var arMapObjects = \{(.+)\}", str(script_content))
            data = json.loads(match.group(0).split('var arMapObjects = ')[1])

            return data["features"]
    
    return []


def save_data (data=None):
    if data is None:
        return False

    with open('gemotest.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True
    


if __name__ == "__main__":
    cities = get_cities(url=URL)
    data = []

    for city in cities:
        data = data + get_data(city, url = URL)
    print("her")
    data = update_location(data)

    featureCollection = {
        "type": "FeatureCollection",
        "features": data
    }

    if featureCollection:
        result = save_data(featureCollection)
        if result:
            print("Data successfully saved")
        else:
            print("Error while saving data")
    