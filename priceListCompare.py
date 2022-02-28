from datetime import date
from doctest import master
from operator import index
from pickle import TRUE
from turtle import pos
import pandas as pd
import numpy as np
from pathlib import Path 
from openpyxl import load_workbook, Workbook 
import xlwings as xw
import glob
import os


#-------------------------------------------PSEUDOCODE-------------------------------------------

#COMPARE 2021 Q4 PRICE LIST TO 2022 Q1 SHOWING PRICE INCREASE, DECREASE, AND NO CHANGE FOR MATCHING PRODUCTS
#IF NO MATCH FOUND, SET AS NEW PRODUCT
#EXAMPLE:
#PART NUMBER    STATUS       PRICE BOOK               US MASTER PRICE      CUSTOMER PRICE     
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150


##COMPARE ALL GPO PRICE LISTS TO CURRENT US MASTER PRICE LIST SHOWING ONLY PRICE HIGHER IN GPO PRICE LIST IF GPO PRICE LIST IS HIGHER THAN US MASTER
#SHOW ONLY ITEMS THAT HAVE HIGHER PRICE LIST AND THE CORRESPONDING GPO PRICE BOOK IT WAS FOUND ON
#EXAMPLE:
#PART NUMBER    STATUS       PRICE BOOK               US MASTER PRICE      CUSTOMER PRICE     
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150
#  XXXXX        HIGHER    VIZIENT 2016 PRICE LIST          $100                 $150



#--------------------------------------------USE CASE 1---------------------------------------------------------------------
#Summary:Compare prior qt us master pricing to current qt
#Input:Prior qt pricing & current qt pricing
#Output:All part numbers pricing delta, status (no change, price list increase, price list decreased, new, deleted).

#Definition of status:
#   No Change: no pricing changes compared to last qt
#   Price List Increase: Price list is higher compared to last qt
#   Price list decrease: Price list is lower compared to last qt
#   New: Part number not found compared to last qt
#   Deleted: Part number was found in obsolete file 

# should see delta on NUSM307

#CREATE DF FOR PRIOR QT US MASTER
curr_US_Master = 'files/2022_Q1_US_Master.xlsx'
df_curr_US_Master = pd.read_excel(curr_US_Master)
df_curr_US_Master = df_curr_US_Master[['PART_NUM','DESCRIPTION', 'TYPE', 'MAG', 'MAG_CODE',	'AG',	'AG_CODE',	'BUSINESS_UNIT', 'BUSINESS', 'BS_CODE', 'BU_CODE', 'LIST_PRICE']]
# print(df_curr_US_Master)


old_US_Master = 'files/2021_Q4_US_MASTER.xlsx'
df_old_US_Master = pd.read_excel(old_US_Master)
df_old_US_Master = df_old_US_Master[['PART_NUM','DESCRIPTION', 'TYPE', 'MAG', 'MAG_CODE',	'AG',	'AG_CODE',	'BUSINESS_UNIT', 'BUSINESS', 'BS_CODE', 'BU_CODE', 'LIST_PRICE', 'Comments', 'Discountable']]

df_old_US_Master.rename(columns={'LIST_PRICE':'OLD_LIST_PRICE'}, inplace=TRUE)
# print(df_old_US_Master)

#Merge old list price and comments to current US Master. This works like a vlookup pulling in based on PART_NUM and pulling in the OLD_LIST_PRICE
df_output = pd.merge(df_curr_US_Master, df_old_US_Master[['PART_NUM', 'OLD_LIST_PRICE', 'Comments', 'Discountable']], on='PART_NUM', how = 'left' )


#add in new column 'delta' calculating difference between old list price and list price (current US Master price)
df_output['DELTA'] = df_output.apply(lambda row: row.OLD_LIST_PRICE - row.LIST_PRICE, axis=1)


#add in new 'status' column. Applying 'no change' if delta is 0, 'price increased' if list price increased, 'price decreased' if delta is a negative, and 'new' if nan
def status_df(df_output):
    if(df_output['DELTA'] > 0):
        return 'price list increased'
    elif(df_output['DELTA'] < 0):
        return 'price list decreased'
    elif(df_output['DELTA'] == 0):
        return 'no change'


df_output['STATUS'] = df_output.apply(status_df, axis=1)

#apply 'new' status if old pricing is N/A
df_output['STATUS'] = df_output['STATUS'].fillna('new')


#save file to local hard drive
df_output.to_excel(r"C:\Users\milad\Dropbox\Documents\Development\Philips\Price List Comparison\price-list-comparison\output\US_MASTER_ANALYSIS.xlsx", na_rep = 'N/A', index=False)
print('Qt Catalog Review Completed')


#--------------------------------------------USE CASE 2---------------------------------------------------------------------
#Summary:
#Input:
#Output:

PATH = r'files\2021 Q4 Customer Price Lists'
all_files = glob.glob(PATH + "/*.xlsx")

# for loop to create a large dataframe from all the customer price lists in folder
li = []
for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0)
    li.append(df)



df_customer_price_lists = pd.concat(li, axis=0, ignore_index=True)
print('Mass data frame for customer price lists have been created')

df_customer_price_lists.rename(columns={'Product Number':'PART_NUM'}, inplace=TRUE)
df_customer_price_lists.rename(columns={'Contract Price List':'Contract_Price_List'}, inplace=TRUE)

df_customer_output = pd.merge(df_curr_US_Master,df_customer_price_lists[['PART_NUM', 'Price List Label', 'Contract_Price_List']], on='PART_NUM', how='left')


#add in new column 'delta' calculating difference between old list price and list price (current US Master price)
df_customer_output['DELTA'] = df_customer_output.apply(lambda row: row.Contract_Price_List - row.LIST_PRICE, axis=1)


#add in new 'status' column. Applying 'no change' if delta is 0, 'price increased' if list price increased, 'price decreased' if delta is a negative, and 'new' if nan
def priceListCompare_df(df_customer_output):
    if(df_customer_output['DELTA'] > 0):
        return 'Price is higher on Customer Price List'
    elif((df_customer_output['DELTA'] < 0) | (df_customer_output['DELTA'] == 0)):
        return 'Okay'
    else:
        return 'part number not on contract price list'



df_customer_output['STATUS'] = df_customer_output.apply(priceListCompare_df, axis=1)

#apply 'new' status if old pricing is N/A
# df_customer_output['STATUS'] = df_customer_output['STATUS'].fillna('new')



df_customer_output.to_excel(r"C:\Users\milad\Dropbox\Documents\Development\Philips\Price List Comparison\price-list-comparison\output\2021Q4_Customer_Price_List.xlsx", index=False)
print('Output is ready')

#need to pull all price list from siebel to identify how df should be created from that



#ADD COLUMNS FOR PRICE LIST OF EACH CUSTOMER PRICE BOOK 

#DELTA BETWEEN EACH PRICE LIST - US MASTER 
#IF CUSTOMER PRICE LIST IS HIGHER THAN US MASTER SHOW AS INCORRECT PRICING


#COMPARE CUSTOMER PRICE LISTS TO OLD CUSTOMER PRICE LIST 


#COMPARE OLD MASTER TO CURR MASTER

#SAVE RESULTS TO A NEW EXCEL FILE 


