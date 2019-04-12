
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
import csv

link_start="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber="
# input page number in between these two strings
link_end="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"
pages=[]
for i in range(1,10):
    link=link_start+str(i)+link_end
    page = requests.get(link)
    pages.append(page)
# end with pages object with list of pages
    
def loadAllProductLinks():
    link_start="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber="
    link_end="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"
    page_num=500 #try too big to see how the response looks
    link=link_start+str(page_num)+link_end
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.prettify())

def extract_product_num_from_line(string):
    '''function to extract product name from html string'''
    result = re.search('data-availability="(.*)"></span>', string)
    return result.group(1)
# test
# extract_product_num_from_line(str(product_number[4]))

def getAllProductNumbers():
    product_numbers=[]
    for page in pages:
        soup = BeautifulSoup(page.content, 'html.parser')
        product_number_lines=soup.find_all('span', class_="product-availability-symbol")
        for line in product_number_lines:
            product_numbers.append(extract_product_num_from_line(str(line)))
    
    unique_product_numbers=list(set(product_numbers))
    return unique_product_numbers

if __name__=="__main__":
    unique_product_numbers=getAllProductNumbers()
    print("product number count: "+str(len(unique_product_numbers)))
