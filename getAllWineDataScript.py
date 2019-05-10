#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:26:55 2019

@author: Heppa
"""

# load product numbers from file
import importProductNumbersFromFile
import wineScrapingFunctions
import requests

from bs4 import BeautifulSoup

#%% Get product numbers
unique_product_numbers=importProductNumbersFromFile.getProductNumbers()
# In[185]:

#####################################################
#%% save to file function

def save_to_csv(all_products,number):
    all_products.to_csv(path_or_buf="data-files/"+"csv_test"+str(number)+".csv")
    
#####################################################
#%%

import time

# loop through product pages and load the data
soups=[]
try:
    del all_products
except:
    pass


#%%
# Define log writing function
import logging
logging.basicConfig(filename="wine_logging.log", level=logging.DEBUG)

start_t=time.time()
counter=1
error_producing=[]
network_error=[]
logging.info("started")
for product_number in unique_product_numbers:
    product_number=product_number.strip()
    # generate www address
    link_start="https://www.alko.fi/en/tuotteet/" # + add product number
    
    # read page contents to soup object
    try:
        page = requests.get(link_start+str(product_number))
    except:
        network_error.append(product_number)
    soup = BeautifulSoup(page.content, 'html.parser')
    # the next line probably causes memory issues - too long of a string
    # soups.append(soup)
    # translate soup object to a dataframe
    # some products cause errors
    # typically these are non-beverage products
    try:
        product_df=wineScrapingFunctions.product_data_wrapper(soup)
    except:
        logging.warning("failed product number "+str(product_number))
        error_producing.append(product_number)
        
    if 'all_products' in locals():
        all_products=all_products.append(product_df)
    else:
        all_products=product_df
    counter=counter+1
    if counter%100==0:        
        print(str(counter)+", "+str(time.time()-start_t))
    if (counter%500==0) | (product_number==unique_product_numbers[-1]):
        save_to_csv(all_products,counter)
        try: # if for some reason all_products is missing
            del all_products
        except:
            pass
end_t=time.time()
logging.info("end")

logging.info("time elapsed: " + str(end_t-start_t))
logging.info("time per page: "+str((end_t-start_t)/counter))
logging.info("expected duration: "+str(((end_t-start_t)/counter)*len(unique_product_numbers)/60)+" mins")

