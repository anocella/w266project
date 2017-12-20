# -*- coding: utf-8 -*-

import requests
import pickle

apiKey = "zh6f-9LQ6ZVbxx65djNV"
startDate = "19900101"
endDate = "20180101"

stockdata = dict()
tickers = list()
with open("D:/w266project/sp500_full.txt", "r") as tfile:
    for t in tfile:
        tickers.append(t.strip('\n'))
        
for t in tickers:
    stockdata[t] = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?"
                                 + "date.gte=" + startDate + "&date.lt=" + endDate
                                 + "&api_key=" + apiKey + "&ticker=" + t).json()

with open("D:/w266project/stockdata/stockdata.pkl", "wb") as pklfile:
    pickle.dump(stockdata, pklfile)