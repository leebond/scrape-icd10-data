# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:14:29 2019

@author: david
"""

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


### download chrome driver from https://chromedriver.chromium.org/ 
driver = webdriver.Chrome('C:/Users/david/Documents/chromedriver/chromedriver.exe')
http = "https://www.icd10data.com/ICD10CM/Codes"
driver.get(http)

df = pd.DataFrame(columns=['icd10parent', 'icd10parentdesc', 'icd10children1', 'icd10children1desc',\
                           'icd10children2', 'icd10children2desc'])

def saveData(df, parent, parentdesc, child1, child1desc, child2, child2desc):
    df = df.append({'icd10parent': parent, 'icd10parentdesc': parentdesc, \
                      'icd10children1': child1, 'icd10children1desc': child1desc, \
                      'icd10children2': child2, 'icd10children2desc': child2desc}, ignore_index = True)
    return df

def getICD10desc(icd10desc_all, icd10code):
    res = re.search(icd10code, icd10desc_all).end()
    return icd10desc_all[(res+1):]

parentlistXpath = '/html/body/div[3]/div/div[1]/div/ul/li[*]/a'
parentlist = driver.find_elements_by_xpath(parentlistXpath)

for i in range(len(parentlist)):
    driver.implicitly_wait(2)
#    print(len(parentlist), i+1)
    parentXpath = '/html/body/div[3]/div/div[1]/div/ul/li['+str(i+1)+']/a'
    parent = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, parentXpath))).text
    parentdesc = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, parentXpath[:-2]))).text
    driver.get(http+'/'+parent)
    parentdesc = getICD10desc(parentdesc, parent)
#    print(parentdesc)
    child1listXpath = '/html/body/div[3]/div/div[1]/div/ul/li[*]/a'
    child1list = driver.find_elements_by_xpath(child1listXpath)
    for j in range(len(child1list)):
        driver.implicitly_wait(2)
#        print(len(child1list), j+1)
        child1Xpath = '/html/body/div[3]/div/div[1]/div/ul/li['+str(j+1)+']/a'
        child1 = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, child1Xpath)))
        driver.execute_script("arguments[0].scrollIntoView();", child1)
        child1 = child1.text
        child1desc = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, child1Xpath[:-2]))).text
        driver.get(http+'/'+parent+'/'+child1)
        child1desc = getICD10desc(child1desc, child1)
#        print(child1desc)
        child2listXpath = '/html/body/div[3]/div/div[1]/div/ul/li[*]/a'
        child2list = driver.find_elements_by_xpath(child2listXpath)
        for k in range(len(child2list)):
            driver.implicitly_wait(2)
#            print(len(child2list), k+1)
            child2Xpath = '/html/body/div[3]/div/div[1]/div/ul/li['+str(k+1)+']/a'
            child2 = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, child2Xpath)))
            driver.execute_script("arguments[0].scrollIntoView();", child2)
            child2 = child2.text
            child2desc = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, child2Xpath[:-2]))).text
            child2desc = getICD10desc(child2desc, child2)
#            print(parentdesc, child1desc, child2desc)
            df = saveData(df, parent, parentdesc, child1, child1desc, child2, child2desc)
            
        print(df.shape)
        driver.get(http+'/'+parent)
        ## back to child1 list
    driver.get(http)
    ## back to parent list
    

driver.close()
df.to_csv("ICD10hierarchy.csv", index = False)
print(df.shape)