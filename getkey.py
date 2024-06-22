import requests
import json
import datetime
import pandas as pd

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

def getData():
    getjson(" https://tdx.transportdata.tw/api/basic/v2/Tourism/ScenicSpot/Taipei?%24format=JSON", "spots")
    with open('data/Spots.json', 'r', encoding='utf-8') as f:
        Spots = json.load(f)
    pd_spots = pd.DataFrame(Spots)
    pd_spots = pd_spots[['ScenicSpotName','DescriptionDetail']]
    # print(pd_spots)
    return pd_spots

getData()
