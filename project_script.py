# -*- coding: utf-8 -*-
"""
Created on Sat Jul 09 15:59:16 2016

@author: Josh
"""

import pandas
import unicodedata
from bs4 import BeautifulSoup

data_path = "C:\Users\Josh\Desktop\CS\NU\CS7280\hw1\us-baby-names-release-2015-12-18-00-53-48\output\StateNames.csv"
table_path = "./Table7_"
table_years = [1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2020]

male = [[],[],[],[],[],[],[],[],[],[],[],[]]
female = [[],[],[],[],[],[],[],[],[],[],[],[]]

df = pandas.read_csv(data_path)

for i in range(len(table_years)):
    soup = BeautifulSoup(open(table_path + str(table_years[i]) + ".html"))
    
    #parse html to get the life table and ignore the first 18 elements which are part of the table
    #header
    life_table = soup.find_all("table")[1].find_all("div")[18:]
    print table_years[i]
    for j in range(len(life_table)):
        #special cases for missing data
            
        if j % 14 == 1:
            male[i].append( float(unicodedata.normalize('NFKD',life_table[j].contents[0][1:8]).encode('ascii','ignore')))
        elif j % 14 == 8:
            female[i].append( float(unicodedata.normalize('NFKD',life_table[j].contents[0][1:8]).encode('ascii','ignore')))
    

