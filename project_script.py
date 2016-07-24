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

male = [[0 for j in range(120)] for i in range(12) ]
female = [[0 for j in range(120)] for i in range(12) ]

ext_male = [[0 for j in range(120)] for i in range(107) ]
ext_female = [[0 for j in range(120)] for i in range(107) ]


df = pandas.read_csv(data_path)

for i in range(len(table_years)):
    soup = BeautifulSoup(open(table_path + str(table_years[i]) + ".html"))
    
    #parse html to get the life table and ignore the first 18 elements which are part of the table
    #header
    life_table = soup.find_all("table")[1].find_all("div")[18:]
    
    for j in range(len(life_table)):
        index = j / 14
        if j % 14 == 1:
            male[i][index] = float(unicodedata.normalize('NFKD',life_table[j].contents[0][1:8]).encode('ascii','ignore'))
        elif j % 14 == 8:
            female[i][index] = float(unicodedata.normalize('NFKD',life_table[j].contents[0][1:8]).encode('ascii','ignore'))

#create tables for all years 1910-2016 using interpolation for years where
#the SSA hasn't actuallly produced tables
for i in range(len(ext_male)):
    for j in range(len(male[0])):
        index = i/10 
        diff_m = male[index + 1][j] - male[index][j]
        diff_f = female[index + 1][j] - female[index][j]
        ext_male[i][j] = male[index][j] + (diff_m/10.0 )* (i % 10)
        ext_female[i][j] = female[index][j] + (diff_f/10.0) * (i % 10)
        


        
        