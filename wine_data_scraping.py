
# coding: utf-8

# In[1]:

import requests
page = requests.get("https://www.alko.fi/tuotteet/909527")
page.content

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')


print(soup.prettify())


# In[2]:

taste_description=soup.find_all('div', class_="taste-description")
bag=taste_description[0].get_text()


product_name=soup.find_all('h1', class_="product-name")
name=product_name[0].get_text()

volume=soup.find_all('span', class_="volume")
volume=volume[0].get_text()


# In[3]:

import re
bag=re.sub("\n","",bag)
list_of_tags=re.split(",",bag)
list_of_tags2=[]
for element in list_of_tags:
    list_of_tags2.append((element.lstrip()).rstrip().lower())
print(list_of_tags2)


# In[113]:

def getTasteProfile(soup):
    '''extract the taste profile and name from html'''
    #taste profile
    taste_description=soup.find_all('div', class_="taste-description")
    bag=taste_description[0].get_text()
    #extract name
    product_name=soup.find_all('h1', class_="product-name")
    name=product_name[0].get_text()
    #extraxt product volume (packaging size)
    volume=soup.find_all('span', class_="volume")
    volume=volume[0].get_text()
    volume=re.sub("\xa0l","",volume)
    # some volume fields contain text
    #volume=float(volume)
    
    bag=re.sub("\n","",bag)
    
    list_of_tags=re.split(",",bag)
    list_of_tags2=[]
    for element in list_of_tags:
        list_of_tags2.append((element.lstrip()).rstrip().lower())
    return list_of_tags2, name, volume


# In[5]:

getTasteProfile(soup)


# In[129]:

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# Oton ensimmäinen "commit" 3.3.2019

def getTuotetiedot(soup):

	label_raw = soup.find_all("div", {"class": "column tiny-6 small-b1 h8 fact-label"})
	value_raw = soup.find_all("div", {"class": "column tiny-6 small-h6 fact-data"})

	label = [tag.text for tag in label_raw]
	value = [tag.text.strip() for tag in value_raw]
    
	df = pd.DataFrame({"LABEL": label, "VALUE": value})

	return df

def getTags(soup):

	try:
		wine_tags_raw = soup.find("div", {"class": "product-tags-wrap pdp-wine-tags"}).find_all("div", {"class": "tooltip-heading"})
		wine_tags = [tag.text.strip() for tag in wine_tags_raw]
	except:
		wine_tags = []

	try:
		region_tags_raw = soup.find("div", {"class": "product-tags-wrap pdp-region-tags"}).find_all("div", {"class": "tooltip-heading"})
		region_tags = [tag.text.strip() for tag in region_tags_raw]
	except:
		pass

	try:
		product_tags_raw = soup.find("div", {"class": "product-tags-wrap pdp-region-tags"}).find_all("a", {"class": "tag-not-clickable"})
		product_tags = [tag.text.strip() for tag in product_tags_raw]
	except:
		pass

	#region = region_tags + product_tags

	return wine_tags, region_tags[0],region_tags[1:], product_tags

def getIcons(soup):
    
    try:
        icons_raw = soup.find("ul", {"class": "food-pairings"}).find_all("a", {"class": "trackable-filter-item pdp-symbol-link"})
    except:
        pass
    icons = []

    for tag in icons_raw:
        s = str(tag)
        t = re.search('filterValue":"(.+?)"', s).group(1)
        icons.append(t)    
    return icons


# In[99]:

def getProductCategory(soup):
    try:
        wine_tags_raw = soup.find("a", {"class": "product-category trackable-filter-item"}).get_text()
    except:
        wine_tags_raw = []
    return wine_tags_raw.strip()

def getProductCharacteristics(soup):
    try:
        characteristics_raw = soup.find("div", {"class": "taste-type-text"}).get_text()
    except:
        characteristics_raw = []
    return characteristics_raw.strip()

getProductCharacteristics(soup)


# In[99]:

# script to scrape product numbers

link_start="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber="
# input page number in between these two strings
link_end="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"
pages=[]
for i in range(1,100):
    link=link_start+str(i)+link_end
    try:
        page = requests.get(link)
        pages.append(page)
    except:
        # ignore the error
        break
        
# end with pages object with list of pages

def extract_product_num_from_line(string):
    '''function to extract product name from html string'''
    result = re.search('data-availability="(.*)"></span>', string)
    return result.group(1)

product_numbers=[]
for page in pages:
    soup = BeautifulSoup(page.content, 'html.parser')
    product_number_lines=soup.find_all('span', class_="product-availability-symbol")
    for line in product_number_lines:
        product_numbers.append(extract_product_num_from_line(str(line)))

unique_product_numbers=list(set(product_numbers))
len(unique_product_numbers)


# In[100]:

file = open('product_numbers.txt','w') 
for num in unique_product_numbers:
    file.write(str(num)+",") 
file.close() 


# In[174]:

# wrapper function for all data
def product_data_wrapper(soup):
    # get all data to variables
    tasteprofile=getTasteProfile(soup)
    icons=getIcons(soup)
    tags=getTags(soup)
    productinfo=getTuotetiedot(soup)

    productinfo_T=(productinfo.T).reset_index(drop=True)

    # create new dataframe (initialization)
    product_df=productinfo_T
    headers = product_df.iloc[0]
    product_df  = pd.DataFrame(product_df.values[1:], columns=headers)

    # add the rest to the new dataframe
    taste_profile, name, volume=getTasteProfile(soup)
    product_df["TASTE PROFILE"]=str(','.join(map(str, taste_profile)))
    product_df["NAME"]=str(name)
    product_df["VOLUME"]=str(volume)
    icons=getIcons(soup)
    product_df["ICONS"]=str(','.join(map(str, icons)))
    grape, country, region1, region2=getTags(soup)
    #product_df["TAGS"]=str(getTags(soup))
    product_df["COUNTRY"]=str(country)
    try:
        product_df["GRAPE"]=str(','.join(map(str, grape)))
    except:
        pass
    try:
        product_df["REGION1"]=str(region1[0])
    except:
        pass
    try:
        product_df["REGION2"]=str(region2[0])
    except:
        pass
    product_df["CHARACTERISTICS"]=str(getProductCharacteristics(soup))
    product_df["CATEGORY"]=str(getProductCategory(soup))
    return product_df

###################
# test the function
prod_num_test=909527
link_start="https://www.alko.fi/en/tuotteet/" # + add product number
# read page contents to soup object
page = requests.get(link_start+str(prod_num_test))
soup = BeautifulSoup(page.content, 'html.parser')
print(product_data_wrapper(soup))


# In[172]:



for i in range(0,10):
    product_df=product_data_wrapper(soup)
    if 'all_products' in locals():
        all_products=all_products.append(product_df)
    else:
        all_products=product_df

print(all_products)


# In[44]:

# load product numbers from file
import csv
del unique_product_numbers
if 'unique_product_numbers' in locals():
    1+1
else:
    with open('product_numbers.txt') as csvfile:
        unique_product_numbers=csvfile.read()
unique_product_numbers=re.split(',',unique_product_numbers)
len(unique_product_numbers)


# In[185]:

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
for product_number in unique_product_numbers:
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
end_t=time.time()
print("time elapsed: "+str(end_t-start_t))
print("time per page: "+str((end_t-start_t)/counter))
print("expected duration: "+str(((end_t-start_t)/counter)*len(unique_product_numbers)/60)+" mins")
all_products.head()


# In[186]:

error_producing


# In[187]:

len(all_products)


# In[ ]:



