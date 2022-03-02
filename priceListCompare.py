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
import time


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


#timer setup to track performance
tic_use_case_1 = time.perf_counter()

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

#remove obsolete items from obsolete tab

#add FDA approved column based on questionnaire




#save file to local hard drive
df_output.to_excel(r"C:\Users\milad\Dropbox\Documents\Development\Philips\Price List Comparison\price-list-comparison\output\US_MASTER_ANALYSIS.xlsx", na_rep = 'N/A', index=False)
toc_use_case_1 = time.perf_counter()
print(f'Qt Catalog Review Completed in {toc_use_case_1 - tic_use_case_1:0.4f} seconds')


#--------------------------------------------USE CASE 2---------------------------------------------------------------------
#Summary:Compare customer specific price lists to current market price to identify any issues with backend job done in legacy system
#Input:Current qt pricing AND all customer price lists 
#Output:All part numbers pricing delta, status (Okay, Price list higher on customer price list, part not on contract)

# New scenario: 
# if all price list in price books match, okay, but if one is different/higher apply a "potential issue"
# Add in logic to review against prior quarter price list 
#

tic_use_case_2_a = time.perf_counter()
PATH = r'files\2022 Q1 Customer Price Lists'
all_files = glob.glob(PATH + "/*.xlsx")

# for loop to create a large dataframe from all the customer price lists in folder
li = []
for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0)
    df['Price Book Name'] = os.path.basename(filename)
    li.append(df)



df_customer_price_lists = pd.concat(li, axis=0, ignore_index=True)
toc_use_case_2_a = time.perf_counter()
print(f'Mass data frame for customer price lists have been created in {toc_use_case_2_a - tic_use_case_2_a:0.4f} seconds')

tic_use_case_2_b = time.perf_counter()

df_customer_price_lists.rename(columns={'Code':'PART_NUM'}, inplace=TRUE)
df_customer_price_lists.rename(columns={'List Price':'Contract_Price_List'}, inplace=TRUE)

df_customer_output = pd.merge(df_curr_US_Master,df_customer_price_lists[['PART_NUM', 'Price Book Name', 'Contract_Price_List']], on='PART_NUM', how='left')


#add in new column 'delta' calculating difference between old list price and list price (current US Master price)
df_customer_output['DELTA'] = df_customer_output.apply(lambda row: row.Contract_Price_List - row.LIST_PRICE, axis=1)


#method for applying status based on customer price list compared to US Master price list
#If delta is greater than 0 set status to 'price is higher on customer price list'
#else if delta is less than 0 OR delta is equal to 0, set status to 'okay' since pricing can stay the same or be lower than market price
#otherwise, part number is not on contract price list and set status to 'part number not on contract price list'
def priceListCompare_df(df_customer_output):
    if(df_customer_output['DELTA'] > 0):
        return 'Price is higher on Customer Price List'
    elif((df_customer_output['DELTA'] < 0) | (df_customer_output['DELTA'] == 0)):
        return 'Okay'
    else:
        return 'part number not on contract price list'


#apply priceListCompare method to customer output file
df_customer_output['STATUS'] = df_customer_output.apply(priceListCompare_df, axis=1)

#export file
df_customer_output.to_excel(r"C:\Users\milad\Dropbox\Documents\Development\Philips\Price List Comparison\price-list-comparison\output\2022Q1_Customer_Price_List.xlsx", index=False)
toc_use_case_2_b = time.perf_counter()
print(f'Output Completed in {toc_use_case_2_b - tic_use_case_2_b:0.4f} seconds\nTotal Time for Price List Comparison = {toc_use_case_2_b - tic_use_case_2_a:0.4f} seconds \nTotal Runtime = {toc_use_case_2_b - tic_use_case_1:0.4f} seconds')





