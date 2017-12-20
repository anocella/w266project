# -*- coding: utf-8 -*-

from multiprocessing import Pool
import myparser

if __name__ == '__main__':
    with open(r'D:\w266project\sp500.txt') as f:
        tickers = list()
        for t in f:
            tickers.append(t.strip('\n'))
    print(tickers)
    with Pool(processes=11) as pool:
        pool.map(myparser.createdata, tickers)