#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:26:55 2019

@author: Heppa
"""

# load product numbers from file
import importProductNumbersFromFile
import wineScrapingFunctions

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

start_t=time.time()
counter=1
error_producing=[]
network_error=[]
for product_number in unique_product_numbers[0:10]:
    # generate www address
    link_start="https://www.alko.fi/en/tuotteet/" # + add product number
    
    # read page contents to soup object
    try:
        page = requests.get(link_start+str(product_number))
    except:
        network_error.append(product_number)
    soup = BeautifulSoup(page.content, 'html.parser')
    soups.append(soup)
    # translate soup object to a dataframe
    # some products cause errors
    # typically these are non-beverage products
    try:
        product_df=product_data_wrapper(soup)
    except:
        error_producing.append(product_number)
        
    if 'all_products' in locals():
        all_products=all_products.append(product_df)
    else:
        all_products=product_df
    counter=counter+1
    if counter%100==0:
        print(str(counter)+", "+str(time.time()-start_t))
    if counter%2==0:
        save_to_csv(all_products,counter)
        try: # if for some reason all_products is missing
            del all_products
        except:
            pass
end_t=time.time()
print("time elapsed: "+str(end_t-start_t))
print("time per page: "+str((end_t-start_t)/counter))
print("expected duration: "+str(((end_t-start_t)/counter)*len(unique_product_numbers)/60)+" mins")
all_products.head()

