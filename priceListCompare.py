from datetime import date
from doctest import master
import pandas as pd
import numpy as np
from pathlib import Path 
from openpyxl import load_workbook, Workbook 
import xlwings as xw


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


#CREATE DF FOR PRIOR QT US MASTER
prior_US_Master = 'files/2021_Q4_US_Master.xlsx'
df_old_US_Master = pd.read_excel(prior_US_Master)

#ARRAY VARIABLE TO STORE DATA FROM SOURCE FILE
append_data = []


#IDENTIFY THE DATA TO BE ADDED TO ARRAY
df_old_US_Master = df_old_US_Master[['PART_NUM','DESCRIPTION', 'TYPE', 'MAG', 'MAG_CODE',	'AG',	'AG_CODE',	'BUSINESS_UNIT', 'BUSINESS', 'BS_CODE', 'BU_CODE', 'LIST_PRICE']]

#Append data to df
append_data.append(df_old_US_Master)
# print(append_data)

#LOOK FOR PART NUMBERS THAT MATCH TO PRIOR MASTER AND PULL IN LIST PRICE 

#APPEND TO DATA

#CALCULATE DELTA AND APPEND AS NEW COLUMN TO DF AS 'DELTA'


#CONCAT DATA AND PASTE INTO NEW MASTER FILE 
append_data = pd.concat(append_data)
append_data.to_excel(r"C:\Users\milad\Dropbox\Documents\Development\Philips\Price List Comparison\price-list-comparison\output\US_MASTER_ANALYSIS.xlsx", index=False)


# print(df_old_US_Master)


#CREATE DF FOR CURRENT QT US MASTER
# curr_US_Master = 'files/2021_Q4_US_Master.xlsx'
# wb = load_workbook(curr_US_Master)
# ws = wb.active

# column_a = ws['A']
# print(column_a)

# for cell in column_a:
#     print(cell.value)
# df_curr_US_Master = pd.read_excel(curr_US_Master)

# wb = load_workbook(filename=curr_US_Master)



#CREATE THE NEW WORKBOOK
# master_wb = xw.Book()

# for cells in curr_US_Master:
#     wb = xw.Book(curr_US_Master)
#     for sheet in wb.sheets:
#         sheet.api.copy(After=master_wb.sheets[0].api)
#         wb.close()

# master_wb.sheets[0].delete()
# master_wb.save(f'US_MASTER_ANALYSIS.xlsx')
# if len(master_wb.app.books) == 1:
#     master_wb.app.quit()
# else:
#     master_wb.close()

# master_ws = master_wb.active
# master_ws.title = 'US_MASTER_ANALYSIS'



# values_excel_files = {}
# for curr_US_Master in curr_US_Master:
#     report_date = curr_US_Master.stem.replace("_Report", "")
#     wb = load_workbook(filename=curr_US_Master)
#     rng = wb["Sheet1"]["B2":"B19"]
#     rng_values = []
#     for cells in rng:
#         for cell in cells:
#             rng_values.append(cell.value)
#     values_excel_files[report_date] = rng_values
# print(values_excel_files)
#COPY PART NUMBERS FROM CURRENT US MASTER INTO NEW FILE
#PART NUMBER | DESCRIPTION | HIERARCHYY (MAG, AG, BU) | OLD PRICE LIST | NEW PRICE LIST | DELTA | STATUS 


#IF PART NUMBER NOT FOUND, SET AS NEW STAUS AND PULL IN DATA FROM CURRENT US MASTER INTO SHEET

#IF PART NUMBER IS FOUND, POPULATE OLD PRICE, NEW PRICE LIST
#CALCULATE DELTA
#SET STATUS BASED ON DEFINITION



#


#


#

# print(df_old_US_Master)

#

#--------------------------------------------USE CASE 2---------------------------------------------------------------------
#Summary:
#Input:
#Output:

#CREATE DF FOR ALL CUSTOMER PRICE BOOKS


#COMPARE OLD MASTER TO CURR MASTER

#SAVE RESULTS TO A NEW EXCEL FILE 


