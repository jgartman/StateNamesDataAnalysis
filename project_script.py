# -*- coding: utf-8 -*-
"""
Created on Sat Jul 09 15:59:16 2016

@author: Josh
"""

import pandas
import unicodedata
from bs4 import BeautifulSoup

file_path = "C:\Users\Josh\Desktop\CS\NU\CS7280\hw1\us-baby-names-release-2015-12-18-00-53-48\output\StateNames.csv"

df = pandas.read_csv(file_path)

soup = BeautifulSoup(open("C:\Users\Josh\Desktop\CS\data_project\Table7_1920.html"))

#parse html to get the life table and ignore the first 18 elements which are part of the table
#header
lt = soup.find_all("table")[1].find_all("div")[18:]

#characters are in unicode format, convert to ascii
unicodedata.normalize('NFKD', lt[66].contents[0][1:6]).encode('ascii','ignore')

male = []

female = []

for i in range(len(lt)):
    if i % 14 == 1:
        male.append( float(unicodedata.normalize('NFKD',lt[i].contents[0][1:8]).encode('ascii','ignore')))
    elif i % 14 == 8:
        female.append( float(unicodedata.normalize('NFKD',lt[i].contents[0][1:8]).encode('ascii','ignore')))
        



