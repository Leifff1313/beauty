import json
import pandas as pd
import requests
import csv

# 從網站上獲取資料上的key
app_id = 'sssun-09d597db-5ec8-446e'
app_key = '8ffe4bd6-dc2e-40e1-8f9e-2c5d62e13ab1'
# 要查詢的ＡＰＩ、參數
# 獲取資料的class


class Auth():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'
        return {
            'content-type': content_type,
            'grant_type': grant_type,
            'client_id': self.app_id,
            'client_secret': self.app_key
        }


class data():
    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')
        return {
            'authorization': 'Bearer ' + access_token,
            'Accept-Encoding': 'gzip'
        }


def getjson(url, filename):
    auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
    a = Auth(app_id, app_key)
    auth_response = requests.post(auth_url, a.get_auth_header())
    d = data(app_id, app_key, auth_response)
    national_scenic_response = requests.get(url, headers=d.get_data_header())

    # 將獲得到的資料以json方式載入
    json_national_scenic = national_scenic_response.text
    json_national_scenic = json.loads(json_national_scenic)

    with open(f'./data/{filename}.json', 'w') as json_file:
        json.dump(json_national_scenic, json_file)


def getSpotData():
    getjson(" https://tdx.transportdata.tw/api/basic/v2/Tourism/ScenicSpot/Taipei?%24format=JSON", "spots")
    with open('data/spots.json', 'r', encoding='utf-8') as f:
        Spots = json.load(f)
    pd_spots = pd.DataFrame(Spots)
    pd_spots = pd_spots[['ScenicSpotName', 'DescriptionDetail', 'Address']]
    # print(pd_spots)
    return pd_spots


def getHotelData():
    getjson("https://tdx.transportdata.tw/api/basic/v2/Tourism/Hotel/Taipei?%24format=JSON", "hotels")
    with open('data/hotels.json', 'r', encoding='utf-8') as f:
        Hotels = json.load(f)
    pd_hotels = pd.DataFrame(Hotels)
    pd_hotels = pd_hotels[['HotelName', 'Description', 'Address']]
    # print(pd_hotels)
    return pd_hotels


def getRestData():
    getjson("https://tdx.transportdata.tw/api/basic/v2/Tourism/Restaurant/Taipei?%24format=JSON", "restaurants")
    with open('data/restaurants.json', 'r', encoding='utf-8') as f:
        Restaurants = json.load(f)
    pd_Restaurants = pd.DataFrame(Restaurants)
    pd_Restaurants = pd_Restaurants[['RestaurantName' 'Description', 'Address']]

    return pd_Restaurants


def getActData():
    getjson("https://tdx.transportdata.tw/api/basic/v2/Tourism/Activity/Taipei?%24format=JSON", "activity")
    with open('data/activity.json', 'r', encoding='utf-8') as f:
        Activitys = json.load(f)
    pd_Activitys = pd.DataFrame(Activitys)
    pd_Activitys = pd_Activitys[['ActivityName', 'Description', 'Address']]

    return pd_Activitys


def getEcoStoreData():
    file = open('data/臺北市綠色商店1130429.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    pd_eco_store = pd.DataFrame(reader)
    pd_eco_store = pd_eco_store[[1, 2, 8]]
    pd_eco_store['Name'] = pd_eco_store[1]
    pd_eco_store['Address'] = pd_eco_store[2]
    pd_eco_store['Type'] = pd_eco_store[8]
    pd_eco_store = pd_eco_store.drop(columns=1)
    pd_eco_store = pd_eco_store.drop(columns=2)
    pd_eco_store = pd_eco_store.drop(columns=8)
    return pd_eco_store


def getEcoHotelData():
    file = open('data/臺北市環保標章旅館1130429.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    pd_eco_hotel = pd.DataFrame(reader)
    pd_eco_hotel = pd_eco_hotel[[2, 3, 7]]
    pd_eco_hotel['Name'] = pd_eco_hotel[2]
    pd_eco_hotel['Address'] = pd_eco_hotel[3]
    pd_eco_hotel['Type'] = pd_eco_hotel[7]
    pd_eco_hotel = pd_eco_hotel.drop(columns=2)
    pd_eco_hotel = pd_eco_hotel.drop(columns=3)
    pd_eco_hotel = pd_eco_hotel.drop(columns=7)
    return pd_eco_hotel


def getEcoLivingData():
    file = open('data/臺北市環保旅店.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    pd_eco_living = pd.DataFrame(reader)
    pd_eco_living = pd_eco_living[[1, 3, 4]]
    pd_eco_living = pd_eco_living[pd_eco_living[3] == "臺北市"]
    pd_eco_living['Name'] = pd_eco_living[1]
    pd_eco_living['Address'] = pd_eco_living[4]
    pd_eco_living = pd_eco_living.drop(columns=1)
    pd_eco_living = pd_eco_living.drop(columns=3)
    pd_eco_living = pd_eco_living.drop(columns=4)
    return pd_eco_living


def getEcoRestaurantData():
    file = open('data/臺北市環保餐廳.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    pd_eco_restaurant = pd.DataFrame(reader)
    pd_eco_restaurant = pd_eco_restaurant[[2, 6, 7]]
    pd_eco_restaurant['Name'] = pd_eco_restaurant[2]
    pd_eco_restaurant['Address'] = pd_eco_restaurant[6]
    pd_eco_restaurant['Type'] = pd_eco_restaurant[7]
    pd_eco_restaurant = pd_eco_restaurant.drop(columns=2)
    pd_eco_restaurant = pd_eco_restaurant.drop(columns=6)
    pd_eco_restaurant = pd_eco_restaurant.drop(columns=7)
    return pd_eco_restaurant
