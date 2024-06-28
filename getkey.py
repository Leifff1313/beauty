import requests
import json
import datetime
import pandas as pd
import os

#從網站上獲取資料上的key
app_id = 'sssun-09d597db-5ec8-446e'
app_key = '8ffe4bd6-dc2e-40e1-8f9e-2c5d62e13ab1'
#要查詢的ＡＰＩ、參數
#獲取資料的class
class Auth():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'
        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }
class data():
    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response
    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')
        return{
            'authorization': 'Bearer ' + access_token,
            'Accept-Encoding': 'gzip'
        }



def merge_address(address):
    if address:
        return f"{address.get('City', '')}{address.get('Town', '')}{address.get('StreetAddress', '')}"
    return None


def getjson(url, filename):
    auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
  
    a = Auth(app_id, app_key)
    auth_response = requests.post(auth_url, a.get_auth_header())
    d = data(app_id, app_key, auth_response)
    national_scenic_response = requests.get(url, headers=d.get_data_header())

    #將獲得到的資料以json方式載入
    json_national_scenic = national_scenic_response.text
    json_national_scenic = json.loads(json_national_scenic)

    with open(f'./data/{filename}.json', 'w') as json_file:
        json.dump(json_national_scenic, json_file)

def getSpotData():
    getjson(" https://tdx.transportdata.tw/api/basic/v2/Tourism/ScenicSpot/Taipei?%24format=JSON", "spots")
    with open('data/spots.json', 'r', encoding='utf-8') as f:
        Spots = json.load(f)
    pd_spots = pd.DataFrame(Spots)
    pd_spots = pd_spots[['ScenicSpotName','DescriptionDetail','Address']]
    # print(pd_spots)
    return pd_spots

def getHotelData():
    getjson("https://tdx.transportdata.tw/api/basic/v2/Tourism/Hotel/Taipei?%24format=JSON", "hotels")
    with open('data/hotels.json', 'r', encoding='utf-8') as f:
        Hotels = json.load(f)
    pd_hotels = pd.DataFrame(Hotels)
    pd_hotels = pd_hotels[['HotelName','Description','Address']]
    # print(pd_hotels)
    return pd_hotels

def getRestDataG():
    with open('data/RestaurantList.json', 'r', encoding='utf-8-sig') as f:
        Restaurants = json.load(f)
    pd_Restaurants = pd.DataFrame(Restaurants)
    pd_Restaurants =pd.DataFrame(pd_Restaurants['Restaurants'])
    pd_Restaurants['Restaurantname'] = pd_Restaurants['Restaurants'].apply(lambda x : x['RestaurantName'])
    pd_Restaurants['Description'] = pd_Restaurants['Restaurants'].apply(lambda x : x['Description'])
    pd_Restaurants['PostalAddress'] = pd_Restaurants['Restaurants'].apply(lambda x : x['PostalAddress'])
    pd_Restaurants = pd_Restaurants.drop(columns='Restaurants')
    pd_Restaurants['City'] = pd_Restaurants['PostalAddress'].apply(lambda x :x['City']) 
    pd_Restaurants['Town'] = pd_Restaurants['PostalAddress'].apply(lambda x :x['Town']) 
    pd_Restaurants['StreetAddress'] = pd_Restaurants['PostalAddress'].apply(lambda x :x['StreetAddress']) 
    pd_Restaurants['Address'] = pd_Restaurants['PostalAddress'].apply(merge_address)   
    pd_Restaurants = pd_Restaurants.drop(columns='PostalAddress') 
    pd_Restaurants = pd_Restaurants.drop(columns='City') 
    pd_Restaurants = pd_Restaurants.drop(columns='Town') 
    pd_Restaurants = pd_Restaurants.drop(columns='StreetAddress') 

    print(pd_Restaurants)

    return pd_Restaurants


def getRestDataTDX():
    getjson("https://tdx.transportdata.tw/api/basic/v2/Tourism/Restaurant/?%24format=JSON", "restaurants")
    with open('data/restaurants.json', 'r', encoding='utf-8') as f:
        Restaurants = json.load(f)
    pd_Restaurants = pd.DataFrame(Restaurants)
    pd_Restaurants = pd_Restaurants[['RestaurantName','Description','Address']]
    print(pd_Restaurants)
    return pd_Restaurants
    

def getActData():
    getjson("https://tdx.transportdata.tw/api/basic/v2/Tourism/Activity/Taipei?%24format=JSON", "activity")
    with open('data/activity.json', 'r', encoding='utf-8') as f:
        Activitys = json.load(f)
    pd_Activitys = pd.DataFrame(Activitys)
    pd_Activitys = pd_Activitys[['ActivityName','Description','Address']]
    # print(pd_Activitys)
    return pd_Activitys
# getSpotData()
# getHotelData()

getRestDataTDX()
# getActData()

# print(os.path.abspath("RestaurantList.json"))

# getRestDataG()