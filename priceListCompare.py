import pandas as pd
import numpy as np


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


#CREATE DF FOR CURRENT QT US MASTER
curr_US_Master = 'files/2021_Q4_US_Master.xlsx'
df_curr_US_Master = pd.read_excel(curr_US_Master)

#COPY PART NUMBERS FROM CURRENT US MASTER INTO NEW FILE
#PART NUMBER | DESCRIPTION | HIERARCHYY (MAG, AG, BU) | OLD PRICE LIST | NEW PRICE LIST | DELTA | STATUS 


#IF PART NUMBER NOT FOUND, SET AS NEW STAUS AND PULL IN DATA FROM CURRENT US MASTER INTO SHEET

#IF PART NUMBER IS FOUND, POPULATE OLD PRICE, NEW PRICE LIST
#CALCULATE DELTA
#SET STATUS BASED ON DEFINITION



#


#


#

print(df_old_US_Master)

#

#--------------------------------------------USE CASE 2---------------------------------------------------------------------
#Summary:
#Input:
#Output:

#CREATE DF FOR ALL CUSTOMER PRICE BOOKS


#COMPARE OLD MASTER TO CURR MASTER

#SAVE RESULTS TO A NEW EXCEL FILE 


