# -*- coding: utf-8 -*-

import os
import glob
import sys
from HTMLParser import HTMLParser
from sklearn.feature_extraction.text import TfidfVectorizer as TfidfVectorizer
import numpy as np


sys.path.append('C:\w266project\sec-edgar-master\SECEdgar')  # Modify to identify path for custom modules

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

def preprocess(data):
    try:
        data = strip_tags(data)
    except Exception as e:
        print(e)
    data = data.upper()
    return data

#Bring in files. Vecortrize and perform cosine simularity
def main():

    # User defined directory for files to be parsed            
    TARGET_FILES = r'C:\w266project\sec-edgar-master\SEC-Edgar-Data\NTAP\0001002047\10-Q\*.*'
    file_list = glob.glob(TARGET_FILES)

    tfidf = TfidfVectorizer(input='filename', strip_accents='unicode', analyzer='word', preprocessor=preprocess, stop_words='english', norm='l1')
    term_matrix = tfidf.fit_transform(file_list)
    for doc1 in range(term_matrix.shape[0]):
        for doc2 in range(term_matrix.shape[0]):
            similarity = np.dot(term_matrix[doc1].todense(), term_matrix[doc2].todense().T) / (np.linalg.norm(term_matrix[doc1].todense()) * np.linalg.norm(term_matrix[doc2].todense()))
            print('Filename 1: ' + str(file_list[doc1]))
            print('Filename 2: ' + str(file_list[doc2]))
            print('Similarity: ' + str(similarity))




if __name__ == '__main__':
    main()