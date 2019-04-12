
# coding: utf-8

# In[4]:

link="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber=9&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"

import requests
page = requests.get(link)

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

print(soup.prettify())


# In[18]:

body=list(soup.children)[4]
list(body.children)

card=soup.find_all('div', class_="mini-card-wrap column")
print(card)


# In[20]:




# In[26]:

soup = BeautifulSoup(pages[1].content, 'html.parser')
print(soup)


# In[57]:

product_number=soup.find_all('span', class_="product-availability-symbol")
print(product_number[1])


# In[94]:




# In[108]:

# script to scrape product numbers

link_start="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber="
# input page number in between these two strings
link_end="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"
pages=[]
for i in range(1,10):
    link=link_start+str(i)+link_end
    page = requests.get(link)
    pages.append(page)
# end with pages object with list of pages

def extract_product_num_from_line(string):
    '''function to extract product name from html string'''
    result = re.search('data-availability="(.*)"></span>', string)
    return result.group(1)
extract_product_num_from_line(str(product_number[4]))

product_numbers=[]
for page in pages:
    soup = BeautifulSoup(page.content, 'html.parser')
    product_number_lines=soup.find_all('span', class_="product-availability-symbol")
    for line in product_number_lines:
        product_numbers.append(extract_product_num_from_line(str(line)))

unique_product_numbers=list(set(product_numbers))
len(unique)


# In[45]:




# In[100]:




# In[103]:

len(product_numbers)


# In[107]:




# In[ ]:



