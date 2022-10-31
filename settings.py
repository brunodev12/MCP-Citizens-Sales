def set_apis(polygon_api, moralis_api="test"):
    with open(".env","w") as f:
        text= f"POLYGONSCAN_APIKEY={polygon_api}\nMORALIS_APIKEY={moralis_api}"
        f.write(text)
