import csv
import time
import constants
import requests
import json
from decouple import config

def get_metadata(side=None, name_dir=None):
    #Open the file 'Sales_price.csv' and obtain the information
    citizens_sales = []
    print("Getting citizens metadata...")
    with open(f"{name_dir}/Sales_price.csv", "r", newline="\n") as file:
        data = csv.DictReader(file)
        for i in data:
            time.sleep(1.05)               #Timer: 1 call per second
            try:
                attr = get_attributes(i['Token_ID'], side)
                c = {
                    'DateTime': i['DateTime'],
                    'Txhash': i['Txhash'],
                    'Token_ID': i['Token_ID'],
                    'Sale_price': i['Sale_price'],
                    'Rank': attr[0],
                    'Gender': attr[1],
                    'Generation': attr[2],
                    'Strength': attr[3],
                    'Endurance': attr[4],
                    'Charisma': attr[5],
                    'Intelligence': attr[6],
                    'Agility': attr[7],
                    'Luck': attr[8]
                    }
            except:
                c = {
                'DateTime': i['DateTime'],
                'Txhash': i['Txhash'],
                'Token_ID': i['Token_ID'],
                'Sale_price': i['Sale_price'],
                'Rank': "null",
                'Gender': "null",
                'Generation': "null",
                'Strength': "null",
                'Endurance': "null",
                'Charisma': "null",
                'Intelligence': "null",
                'Agility': "null",
                'Luck': "null"
                }
            citizens_sales.append(c)
            print(c)                     #To see the process

    #Create a new file called 'citizens_sales.csv' and add the metadata
    with open(f"{name_dir}/Citizens_sales.csv", "w", newline="\n") as file:
        campos = ["DateTime","Txhash","Token_ID","Sale_price","Rank","Gender","Generation","Strength","Endurance","Charisma","Intelligence","Agility","Luck"]
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        for i in citizens_sales:
            writer.writerow(i)

# Limit: 1 call per second
def get_attributes(token_id, side):

    address = constants.address_eth if side==0 else constants.address_trx
    url = f"https://deep-index.moralis.io/api/v2/nft/{address}/{token_id}?chain=polygon&format=decimal"
    apikey = config('MORALIS_APIKEY')

    headers = {
        "accept": "application/json",
        "X-API-Key": f"{apikey}"                        #You can get the ApiKey from moralis.io
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    metadata = data["metadata"]
    metadata_dict = json.loads(metadata)
    attributes = metadata_dict["attributes"]

    attributes_list = []

    for i in attributes:
        t = i['value']
        attributes_list.append(t)

    return attributes_list