# -*- coding: utf-8 -*-
"""
Created on Sat Jul 09 15:59:16 2016

@author: Josh Gartman
"""

import pandas
import unicodedata
from bs4 import BeautifulSoup

data_path = "../us-baby-names-release-2015-12-18-00-53-48\output\StateNames.csv"
table_path = "./Table7_"
table_years = [1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2020]

#the number of years from 1910 to 2016
NUM_YEARS = 107

#number of rows of data in the life tables
NUM_ROW = 120

#the number of columns in a row in the life tables
NUM_COLUMNS = 14


male = [[0 for j in range(NUM_ROW)] for i in range(len(table_years)) ]
female = [[0 for j in range(NUM_ROW)] for i in range(len(table_years)) ]

ext_male = [[0 for j in range(NUM_ROW)] for i in range(NUM_YEARS) ]
ext_female = [[0 for j in range(NUM_ROW)] for i in range(NUM_YEARS) ]


df = pandas.read_csv(data_path)

for i in range(len(table_years)):
    soup = BeautifulSoup(open(table_path + str(table_years[i]) + ".html"))
    
    #parse html to get the life table and ignore the first 18 elements which are part of the table
    #header
    life_table = soup.find_all("table")[1].find_all("div")[18:]
    
    for j in range(len(life_table)):
        index = j / NUM_COLUMNS
        if j % NUM_COLUMNS == 1:
            #data is currently in unicode format
            male[i][index] = float(unicodedata.normalize('NFKD',life_table[j].contents[0][1:8]).encode('ascii','ignore'))
        elif j % NUM_COLUMNS == 8:
            female[i][index] = float(unicodedata.normalize('NFKD',life_table[j].contents[0][1:8]).encode('ascii','ignore'))

#create tables for all years 1910-2016 using interpolation for years where
#the SSA hasn't actuallly produced tables
for i in range(NUM_YEARS):
    for j in range(NUM_ROW):
        index = i/10 
        diff_m = male[index + 1][j] - male[index][j]
        diff_f = female[index + 1][j] - female[index][j]
        ext_male[i][j] = male[index][j] + (diff_m/10.0 )* (i % 10)
        ext_female[i][j] = female[index][j] + (diff_f/10.0) * (i % 10)

#tables that give the percentage of people born in a given year that are still
#alive in 2016        
male_alive_percent = []
female_alive_percent = []

for i in range(NUM_YEARS):
    male_percent = 1.0
    female_percent = 1.0
    for j in range(i, NUM_YEARS):
        male_percent *= (1 - ext_male[j][j - i])
        female_percent *= (1 - ext_female[j][j - i])
    male_alive_percent.append(male_percent)
    female_alive_percent.append(female_percent)
    
    



        
        