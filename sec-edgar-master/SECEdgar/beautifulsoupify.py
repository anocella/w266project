# -*- coding: utf-8 -*-

import glob
from bs4 import BeautifulSoup
from multiprocessing import Pool

def preprocess(data):
    a = BeautifulSoup(data,"lxml")
    b = BeautifulSoup(a.text,"lxml")
    return b.text.lower()

def doproc(file):
    #from bs4 import BeautifulSoup
    with open(file, 'r') as fhandle:
        with open(file[0:-4] + "_proc.txt", "w", encoding='utf-16') as pfile:
            pfile.write(BeautifulSoup(BeautifulSoup(fhandle, "lxml").text, "lxml").text.lower())
            #pfile.write(preprocess(fhandle))

def main():

    # User defined directory for files to be parsed            
    TARGET_FILES = r'D:\w266project\sec-edgar-master\SEC-Edgar-Data\A\*\2000*.txt'
    file_list = glob.glob(TARGET_FILES)
    return file_list

if __name__ == '__main__':
    file_list = main()
    file_list_set = set(file_list)
    print(file_list)
    new_file_list = []
    while file_list:
        for f in file_list:
            if f[0:-4] + '_proc.txt' in file_list_set:
                file_list.remove(f)
            else:
                if f[-8:] == 'proc.txt':
                    file_list.remove(f)
                else:
                    new_file_list.append(f)
                    file_list.remove(f)
    with Pool(processes=10) as pool:
        pool.map(doproc, new_file_list)