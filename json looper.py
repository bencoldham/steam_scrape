# install the pyotp package first
import pyotp
import requests
import json
import pandas as pd
import csv
import time
import glob
import os

# get a token that's valid right now
my_secret = '2CB3MNZRQ44SD2TB'
my_token = pyotp.TOTP(my_secret)

# print the valid token
print(my_token.now()) # in python3

#data clean
bitskins = requests.get("https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key=6c2fe611-6e27-41f4-99f7-6a8f638b6953&code=" + str(my_token.now())+ "&app_id=730")
bitskins = bitskins.json()['data']['items']

#bitskins lowest prices
dct_lowestprice = {}
for item in bitskins:
    if float(item['lowest_price']) > 10: # min price
        dct_lowestprice[item['market_hash_name']] = float(item['lowest_price'])    
print(dct_lowestprice)

steam_dct = {}
path = 'C:/Users/Fun_B/OneDrive/Desktop/STEAM PROJECT FILE/jsons'
for filename in glob.glob(os.path.join(path, '*.json')):
   with open(os.path.join(os.getcwd(), filename), 'r') as file:
       data = json.load(file)
       #print(data['market_name'])
       #print(data['histogram']['highest_buy_order'])
       market_name = data['market_name']
       price = data['histogram']['highest_buy_order']
       steam_dct[market_name] = price
       
diff_dct = {}
for item in steam_dct.keys():
    try:
        diff_dct[item] = [(float(steam_dct[item]) - float(dct_lowestprice[item])), dct_lowestprice[item]]
    except:
        None
        
with open('output.csv', 'w+',encoding='utf-8-sig') as output:
    writer = csv.writer(output)
    for key, value in diff_dct.items():
        writer.writerow([key, value])