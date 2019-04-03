
# coding: utf-8

# In[1]:

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




def extract_product_num_from_line(string):
    '''function to extract product name from html string'''
    result = re.search('data-availability="(.*)"></span>', string)
    return result.group(1)


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
    
if __name__=="__main__":
    print("test starts")
    prod_num_test=909527
    link_start="https://www.alko.fi/en/tuotteet/" # + add product number
    # read page contents to soup object
    page = requests.get(link_start+str(prod_num_test))
    soup = BeautifulSoup(page.content, 'html.parser')
    print(product_data_wrapper(soup))
    print("test ended")
