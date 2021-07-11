# install the pyotp package first
import pyotp
import requests
import json
#import pandas as pd
import csv
import time
from datetime import date
import os

# get a token that's valid right now
my_secret = '2CB3MNZRQ44SD2TB'
my_token = pyotp.TOTP(my_secret)

# print the valid token
print(my_token.now()) # in python3

#data clean
data = requests.get("https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key=6c2fe611-6e27-41f4-99f7-6a8f638b6953&code=" + str(my_token.now())+ "&app_id=730")
data = data.json()['data']['items']

#bitskins lowest prices
dct_lowestprice = {}
for item in data:
    if float(item['lowest_price']) > 10: # min price
        dct_lowestprice[item['market_hash_name']] = float(item['lowest_price'])    
print(dct_lowestprice)




#make dir
path = ("C:/Users/Fun_B/OneDrive/Desktop/STEAM PROJECT FILE/jsons/" + str(date.today()) + "/jsons/")
if not os.path.exists(path):
    os.mkdir(path)

#steam price
i= 1
for name in dct_lowestprice.keys():
    steam = requests.get("https://api.steamapis.com/market/item/730/" + name + "?api_key=8B8gEHTKzjf-bDw69FAkD7NbLb4")
    steam = steam.json()
    with open(path + str(steam['nameID'])+ ".json", 'w') as f:
        json.dump(steam, f)
    i+=1
    if i == 100:
        time.sleep(61)
        i = 0
