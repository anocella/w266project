# -*- coding:utf-8 -*-
# This script will download all the 10-K, 10-Q and 8-K
# provided that of company symbol and its cik code.

import requests
import os
import errno
from bs4 import BeautifulSoup
from config import DEFAULT_DATA_PATH
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class SecCrawler():

    def __init__(self):
        self.hello = "Welcome to Sec Cralwer!"
        print("Path of the directory where data will be saved: " + DEFAULT_DATA_PATH)

    def make_directory(self, company_code, cik, priorto, filing_type):
        # Making the directory to save comapny filings
        path = os.path.join(DEFAULT_DATA_PATH, company_code, cik, filing_type)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

    def save_in_directory(self, company_code, cik, priorto, doc_list,
        doc_name_list, filing_type, doc_date_list):
        # Save every text document into its respective folder
        for j in range(len(doc_list)):
            base_url = doc_list[j]
            r = requests.get(base_url, verify=False)
            data = r.text
            # deleting filing_type from directory structure so they're all in the same CIK folder
            path = os.path.join(DEFAULT_DATA_PATH, company_code, cik,
                doc_date_list[j] + "_" + doc_name_list[j])
            

            with open(path, "ab") as f:
                f.write(data.encode('ascii', 'ignore'))

    def filing_10Q(self, company_code, cik, priorto, count):

        self.make_directory(company_code, cik, priorto, '10-Q')

        # generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=10-Q&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
        print ("started 10-Q " + str(company_code))
        r = requests.get(base_url, verify=False)
        data = r.text

        # get doc list data
        doc_list, doc_name_list, doc_date_list = self.create_document_list(data)

        try:
            self.save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, '10-Q', doc_date_list)
        except Exception as e:
            print (str(e))

        print ("Successfully downloaded all the files")


    def filing_10K(self, company_code, cik, priorto, count):

        self.make_directory(company_code,cik, priorto, '10-K')

        # generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=10-K&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
        print ("started 10-K " + str(company_code))

        r = requests.get(base_url, verify=False)
        data = r.text

        # get doc list data
        doc_list, doc_name_list, doc_date_list = self.create_document_list(data)

        try:
            self.save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, '10-K', doc_date_list)
        except Exception as e:
            print (str(e))

        print ("Successfully downloaded all the files")

    def filing_8K(self, company_code, cik, priorto, count):
        try:
            self.make_directory(company_code,cik, priorto, '8-K')
        except Exception as e:
            print (str(e))

        # generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=8-K&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)

        print ("started 8-K" + str(company_code))
        r = requests.get(base_url, verify=False)
        data = r.text

        # get doc list data
        doc_list, doc_name_list, doc_date_list = self.create_document_list(data)

        try:
            self.save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, '8-K', doc_date_list)
        except Exception as e:
            print (str(e))

        print ("Successfully downloaded all the files")

    def filing_13F(self, company_code, cik, priorto, count):
        try:
            self.make_directory(company_code, cik, priorto, '13-F')
        except Exception as e:
            print (str(e))

        # generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=13F&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
        print ("started 10-Q "+ str(company_code))
        r = requests.get(base_url, verify=False)
        data = r.text

        doc_list, doc_name_list = self.create_document_list(data)

        try:
            self.save_in_directory(company_code, cik, priorto, doc_list,
                doc_name_list, '13-F')
        except Exception as e:
            print (str(e))

        print ("Successfully downloaded all the files")

    def filing_SD(self, company_code, cik, priorto, count):

        self.make_directory(company_code, cik, priorto, 'SD')

        # generate the url to crawl
        base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=sd&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
        print ("started SD " + str(company_code))
        r = requests.get(base_url, verify=False)
        data = r.text

        # get doc list data
        doc_list, doc_name_list, doc_date_list = self.create_document_list(data)

        try:
            self.save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, 'SD', doc_date_list)
        except Exception as e:
            print (str(e))

        print ("Successfully downloaded all the files")

    def create_document_list(self, data):
        # parse fetched data using beatifulsoup
        soup = BeautifulSoup(data, "html5lib")
        # store the link in the list
        link_list = list()

        # If the link is .htm convert it to .html
        for link in soup.find_all('filinghref'):
            url = link.string
            if link.string.split(".")[len(link.string.split("."))-1] == "htm":
                url += "l"
            link_list.append(url)
        link_list_final = link_list
        
        doc_date_list = list()
        for fd in soup.find_all('datefiled'):
            doc_date_list.append(fd.string)
            

        print ("Number of files to download {0}".format(len(link_list_final)))
        print ("Starting download....")

        # List of url to the text documents
        doc_list = list()
        # List of document names
        doc_name_list = list()

        # Get all the doc
        for k in range(len(link_list_final)):
            required_url = link_list_final[k].replace('-index.html', '')
            txtdoc = required_url + ".txt"
            docname = txtdoc.split("/")[-1]
            doc_list.append(txtdoc)
            doc_name_list.append(docname)
        return doc_list, doc_name_list, doc_date_list