import csv
import time
import requests
import constants
from decouple import config
from metadata import get_metadata

#Limit: 5 call per second
def eth_price(block, side):
    address= constants.contract_eth if side==0 else constants.contract_trx
    topic = constants.topic
    apikey = config('POLYGONSCAN_APIKEY')                                                 #You can get the ApiKey from polygonscan
    multiplier = 10**18 if side==0 else 10**6

    r = requests.get(f"https://api.polygonscan.com/api?module=logs&action=getLogs&fromBlock={block}&toBlock={block}&address={address}&topic0={topic}&apikey={apikey}")

    data = r.json()
    result = data['result']
    result_dict = dict(result[-1])
    raw_valor_hex = result_dict['data']
    valor_hex = raw_valor_hex[66:130]
    valor_int = float(int(valor_hex, 16))

    return valor_int / multiplier, result_dict['transactionHash']


def get_sales(side=None):
    name_dir = "eth" if side==0 else "trx"
    token_sales = []
    #Open the file 'Sales.csv' with the sales and obtain the data
    with open(f"{name_dir}/Sales.csv", "r", newline="\n") as file:
        data = csv.DictReader(file)
        for i in data:
            time.sleep(0.25)                            #Timer: 5 call per second
            a, b = eth_price(int(i['Blockno']), side)
            if b == i['Txhash']:                       #Check if more than 1 citizen has been sold in the same block (very unlikely :D )
                t = {'DateTime': i['DateTime'], 'Txhash': i['Txhash'], 'Token_ID': i['Token_ID'], 'Sale_price': a}
                token_sales.append(t)



    #Create a new file called 'Sales_price.csv' and add the sales prices
    with open(f"{name_dir}/Sales_price.csv", "w", newline="\n") as file:
        campos = ["DateTime","Txhash","Token_ID","Sale_price"]
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        for i in token_sales:
            writer.writerow(i)
    
    get_metadata(side, name_dir)
