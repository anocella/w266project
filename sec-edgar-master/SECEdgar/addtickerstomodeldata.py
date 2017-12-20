# -*- coding: utf-8 -*-

import pandas

stockdata = dict()
tickers = list()
with open("D:/w266project/sp500_full.txt", "r") as tfile:
    for t in tfile:
        tickers.append(t.strip('\n'))
        
alldata = pandas.read_csv('D:/w266project/modeldata/' + tickers[0] + '.csv')
alldata['ticker'] = tickers[0]
for t in tickers[1:]:
    df = pandas.read_csv('D:/w266project/modeldata/' + t + '.csv')
    df['ticker'] = t
    alldata = alldata.append(df)

with open("D:/w266project/singledataset/all.csv", "w") as csvfile:
    alldata.to_csv(csvfile, index=False)