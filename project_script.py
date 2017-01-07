# -*- coding: utf-8 -*-
"""
Created on Sat Jul 09 15:59:16 2016

@author: Josh Gartman
"""

import pandas
import unicodedata
from bs4 import BeautifulSoup
import math
import pickle

data_path = "../us-baby-names-release-2015-12-18-00-53-48/output/StateNames.csv"
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
df_f = df[df["Gender"] == "F"]
df_m = df[df["Gender"] == "M"]
                  
#comment out below if data_struct_f and data_struct_m not perviously constructed
                
index_struct_m = pickle.load(open( "df_m_save.p", "r" ))
index_struct_f = pickle.load(open( "df_f_save.p", "r" ))

#uncomment below if data_struct_f and data_struct_m not perviously constructed
 

#data_struct_m = [[None for j in range(51)] for i in range(105)]
#data_struct_f = [[None for j in range(51)] for i in range(105)]             
#prev_year = 1910
#cur_year_index = 0
#prev_state = "AK"
#cur_state_index = 0
#begin_index = 0
#end_index = 0
##create tables that will make get_pop_name function more efficient
#for i in range(len(df_f)):
#    if df_f.iloc[i].Year != prev_year and df_f.iloc[i].State == prev_state:
#        end_index = i
#        data_struct_f[cur_year_index][cur_state_index] = (begin_index, end_index)
#        begin_index = i
#        prev_year = df_f.iloc[i].Year
#        cur_year_index += 1
#    if df_f.iloc[i].Year != prev_year and df_f.iloc[i].State != prev_state:
#        end_index = i
#        data_struct_f[cur_year_index][cur_state_index] = (begin_index, end_index)
#        begin_index = i
#        prev_state = df_f.iloc[i].State
#        prev_year = 1910
#        cur_year_index = 0
#        cur_state_index += 1
#        
#prev_year = 1910
#cur_year_index = 0
#prev_state = "AK"
#cur_state_index = 0
#begin_index = 0
#end_index = 0
##create tables that will make get_pop_name function more efficient
#for i in range(len(df_m)):
#    if df_m.iloc[i].Year != prev_year and df_m.iloc[i].State == prev_state:
#        end_index = i
#        data_struct_m[cur_year_index][cur_state_index] = (begin_index, end_index)
#        begin_index = i
#        prev_year = df_m.iloc[i].Year
#        cur_year_index += 1
#    if df_m.iloc[i].Year != prev_year and df_m.iloc[i].State != prev_state:
#        end_index = i
#        data_struct_m[cur_year_index][cur_state_index] = (begin_index, end_index)
#        begin_index = i
#        prev_state = df_m.iloc[i].State
#        prev_year = 1910
#        cur_year_index = 0
#        cur_state_index += 1
#
#pickle.dump(data_struct_f, open( "df_f_save.p", "wb" ) )
#pickle.dump(data_struct_m, open( "df_m_save.p", "wb" ) )

state_list = df.State.unique()

for i in range(len(table_years)):
    soup = BeautifulSoup(open(table_path + str(table_years[i]) + ".html"))
    
    #parse html to get the life table and ignore the first 18 elements which are 
    #part of the table header
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
    
#the lookup tables map states to names to total living persons with that name
#from that state
#lookup_table_m = dict.fromkeys(df.State.unique())
#lookup_table_f = dict.fromkeys(df.State.unique())
#
##get unique female and male names
#male_names_dict = dict.fromkeys(df[df["Gender"] == "M"].Name.unique(),0)
#female_names_dict = dict.fromkeys(df[df["Gender"] == "F"].Name.unique(),0)
#
#for state in lookup_table_m.keys():
#    lookup_table_m[state] = male_names_dict.copy()
#    lookup_table_f[state] = female_names_dict.copy()

#populate lookup tables
#for state in lookup_table_m.keys():
 #   for name in lookup_table_m[state].keys():
     
state_list = df["State"].unique()
s = dict.fromkeys(state_list)

name_list_f = df_f["Name"].unique()
name_list_m = df_m["Name"].unique()


for i in range(len(s)):
    s[state_list[i]] = i
    
def get_pop_name(name, gender, state, data_struct):
    state_i = s[state]
    assert(gender == "M" or gender == "F")
    assert(state in state_list)
    if(gender == "M"):
        name_data = df_m
        percent_alive_table = male_alive_percent
    else:
        name_data = df_f
        percent_alive_table = female_alive_percent
    result = 0
    for i in range(104):
        indices = data_struct[i][state_i]
        year_state_table = name_data[indices[0]:indices[1]]
        if name in year_state_table.Name.get_values():
            result += year_state_table[year_state_table["Name"] == name].Count.get_values()[0]*percent_alive_table[i]
    return math.floor(result)

f = [[get_pop_name(name, "F", state, index_struct_f) for state in state_list] for name in name_list_f]
      
df_final_f = pandas.DataFrame(f)
df_final_f.columns = state_list
df_final_f.index = name_list_f
writer_f = pandas.ExcelWriter('processed_data_f.xlsx', engine='xlsxwriter')
df_final_f.to_excel(writer_f)
writer_f.save()

del f
del df_final_f

m = [[get_pop_name(name, "M", state, index_struct_m) for state in state_list] for name in name_list_m]      

df_final_m = pandas.DataFrame(m)
df_final_m.columns = state_list
df_final_m.index = name_list_m
writer_m = pandas.ExcelWriter('processed_data_m.xlsx', engine='xlsxwriter')
df_final_m.to_excel(writer_m)
writer_m.save()