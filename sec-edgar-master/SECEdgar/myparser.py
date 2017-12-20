# -*- coding: utf-8 -*-

import os
import glob
import sys
from html.parser import HTMLParser
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import re
import csv

with open(r'D:\w266project\wordsEn.txt') as f:
    englishWords = list()
    for w in f:
        englishWords.append(w.strip('\n').lower())
    englishWords = set(englishWords)
    
with open(r'D:\w266project\wordsNeg.txt') as f:
    negativeWords = list()
    for w in f:
        negativeWords.append(w.strip('\n').lower())
    negativeWords = set(negativeWords)
    
with open(r'D:\w266project\wordsPos.txt') as f:
    positiveWords = list()
    for w in f:
        positiveWords.append(w.strip('\n').lower())
    positiveWords = set(positiveWords)

with open(r'D:\w266project\wordsLit.txt') as f:
    litigiousWords = list()
    for w in f:
        litigiousWords.append(w.strip('\n').lower())
    litigiousWords = set(litigiousWords)

sys.path.append('D:\w266project\sec-edgar-master\SECEdgar')  # Modify to identify path for custom modules

def html_part(filepath):
    """
    Generator returning only the HTML lines from an
    SEC Edgar SGML multi-part file.
    """
    start, stop = '<html>\n', '</html>\n'
    filepath = os.path.expanduser(filepath)
    with open(filepath) as f:
        # find start indicator, yield it
        for line in f:
            if line == start:
                yield line
                break
        # yield lines until stop indicator found, yield and stop
        for line in f:
            yield line
            if line == stop:
                raise StopIteration

#remove html formatting
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def checkForWord(match):
    match = match.group()
    if match in englishWords and len(match) >= 3:
        return match
    else:
        return ""

def preprocess(data):
    #try:
        #data = strip_tags(data)
    #except Exception as e:
    #    print(e)
    #data = data.upper()
    #a = BeautifulSoup(data,"lxml")
    #b = BeautifulSoup(a.text,"lxml")
    # Remove a bunch of special characters
    #c = re.sub(r"[!@#$%\^&*\.\,\;\'\"\(\)\{\}\[\]`]", r"", b.text).lower() #r"[!@#$%\^&*`]"
    # Strip out common ends of conjugations
    #c = re.sub(r"s\b|ly\b|y\b|ied\b|ed\b", r"", c)
    # 3+ digit numbers are 100 now
    #c = re.sub(r"\b[0-9]{3,}\b", r"100", c)
    data = re.sub(r"\b\w+\b", checkForWord, data)
    data = re.sub(r"[0-9]", "", data)
    #return c
    return data

#Bring in files. Vectorize and perform cosine similarity
def createdata(ticker):
    # User defined directory for files to be parsed       
    lookback = 4
    basePath = 'D:\\w266project\\sec-edgar-master\\SEC-Edgar-Data\\'
    TARGET_FILES = basePath + ticker + r'\\*\\*_proc.txt'
    file_list = glob.glob(TARGET_FILES)
    filesToRemove = []
    for f in range(len(file_list)-1):
        _, tail1 = os.path.split(file_list[f])
        _, tail2 = os.path.split(file_list[f+1])
        if tail1[0:10] == tail2[0:10]:
            print(file_list[f],file_list[f+1])
            filesToRemove.append(file_list[f+1])
    [file_list.remove(f) for f in filesToRemove]

    tfidf = TfidfVectorizer(input='filename', strip_accents='unicode', analyzer='word', preprocessor=preprocess, stop_words='english', norm='l1', encoding='utf-16', ngram_range=(1,3))
    count = CountVectorizer(input='filename', strip_accents='unicode', analyzer='word', preprocessor=preprocess, stop_words='english', encoding='utf-16', ngram_range=(1,3))
    countUnary = CountVectorizer(input='filename', strip_accents='unicode', analyzer='word', preprocessor=preprocess, stop_words='english', encoding='utf-16', ngram_range=(1,1))
    term_matrix_tfidf = tfidf.fit_transform(file_list)
    term_matrix_count = count.fit_transform(file_list)
    term_matrix_countUnary = countUnary.fit_transform(file_list)
    datarows = []
    for doc1 in range(lookback, len(file_list) - 1):
        _, tailCurr = os.path.split(file_list[doc1])
        _, tailPrev = os.path.split(file_list[doc1 - 1])
        _, tailNext = os.path.split(file_list[doc1 + 1])
        fileDate = tailCurr[0:10]
        prevFileDate = tailPrev[0:10]
        nextFileDate = tailNext[0:10]
        similaritiesTfidf = [y.sum() for y in [np.dot(term_matrix_tfidf[doc1].todense(), term_matrix_tfidf[doc2].todense().T) /
                             (np.linalg.norm(term_matrix_tfidf[doc1].todense()) *
                              np.linalg.norm(term_matrix_tfidf[doc2].todense()))
                             for doc2 in [x for x in range(doc1-lookback, doc1)]]]
        similaritiesCount = [y.sum() for y in [np.dot(term_matrix_count[doc1].todense(), term_matrix_count[doc2].todense().T) /
                             (np.linalg.norm(term_matrix_count[doc1].todense()) *
                              np.linalg.norm(term_matrix_count[doc2].todense()))
                             for doc2 in [x for x in range(doc1-lookback, doc1)]]]
        fnames = countUnary.get_feature_names()
        posWordCount = []
        negWordCount = []
        litWordCount = []
        allWordCount = []
        for t in range(doc1-lookback, doc1+1):
            thisTM = term_matrix_countUnary[t].todense()
            posWordCount.append(sum([thisTM.item(fnames.index(w)) for w in positiveWords if w in fnames]))
            negWordCount.append(sum([thisTM.item(fnames.index(w)) for w in negativeWords if w in fnames]))
            litWordCount.append(sum([thisTM.item(fnames.index(w)) for w in litigiousWords if w in fnames]))
            allWordCount.append(thisTM.sum())
        datarows.append([fileDate, prevFileDate, nextFileDate] + [x for x in similaritiesTfidf] +
                            [x for x in similaritiesCount] + [x for x in posWordCount] + 
                            [x for x in negWordCount] + [x for x in litWordCount] + [x for x in allWordCount])
    with open("D:\w266project\modeldata\{}.csv".format(ticker), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['filedate', 'prevfiledate', 'nextfiledate'] +
                        ['simtfidf' + str(x) for x in range(1,lookback+1)[::-1]] +
                        ['simcount' + str(x) for x in range(1,lookback+1)[::-1]] +
                        ['countpos' + str(x) for x in range(lookback+1)[::-1]] +
                        ['countneg' + str(x) for x in range(lookback+1)[::-1]] +
                        ['countlit' + str(x) for x in range(lookback+1)[::-1]] +
                        ['countall' + str(x) for x in range(lookback+1)[::-1]])
        for r in datarows:
            writer.writerow(r)