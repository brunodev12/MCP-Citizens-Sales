import csv
import os
from pathlib import Path

#Open .csv file obtained from polygonscan and filter transactions by method
#Check the .csv file name :)
def open_file(path=None):
    sales = []
    with open(f"{path}", "r", newline="\n") as file:
        data = csv.DictReader(file)
        for i in data:
            if i["Method"] == ' "0x075e906b"':
                sales.append(i)
    return sales


#Create new file called 'Sales.cvs'
def new_file(side, path=None):
    name_dir = "eth" if side==0 else "trx"
    sales = open_file(path)
    os.makedirs(f"{name_dir}", exist_ok=True)
    with open(f"{name_dir}/Sales.csv", "w", newline="\n") as file:
        campos = ["Txhash","Blockno","UnixTimestamp","DateTime","From","To","Token_ID","Method"]
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        for i in sales:
            writer.writerow(i)


#Use this command if you want to add data to existing file named 'Sales.csv'
def add_data(side, path=None):
    name_dir = "eth" if side==0 else "trx"
    sales = open_file(path)
    os.makedirs(f"{name_dir}", exist_ok=True)
    localpath = os.getcwd()
    fileName = rf"{localpath}/{name_dir}/Sales.csv"
    fileObj = Path(fileName)
    if fileObj.is_file() == False:
        with open(f"{name_dir}/Sales.csv", "w", newline="\n") as file:
            campos = ["Txhash","Blockno","UnixTimestamp","DateTime","From","To","Token_ID","Method"]
            writer = csv.DictWriter(file, fieldnames=campos)
            writer.writeheader()
    with open(f"{name_dir}/Sales.csv", "r+", newline="\n") as file:
        file.seek( len(file.read()))
        campos = ["Txhash","Blockno","UnixTimestamp","DateTime","From","To","Token_ID","Method"]
        writer = csv.DictWriter(file, fieldnames=campos)
        for i in sales:
            writer.writerow(i)