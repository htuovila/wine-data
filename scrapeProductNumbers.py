#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:45:49 2019

@author: Heppa
"""


import requests
from bs4 import BeautifulSoup
import re
import csv
import datetime
import math

#####################################
# script to scrape product numbers

def extractProductNumFromLine(string):
    '''function to extract product name from html string'''
    result = re.search('data-availability="(.*)"></span>', string)
    return result.group(1)

def extractProductNumber(page):
    soup=BeautifulSoup(page.content,'html.parser')
    product_number_lines=soup.find_all('span', class_="product-availability-symbol")
    product_numbers=list()
    for line in product_number_lines:
        result=extractProductNumFromLine(str(line))
        product_numbers.append(result)
    return product_numbers

link1="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12"
link2="&SortingAttribute=startOfSale-desc&PageNumber="
link3="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%"
link4="3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"

#link_start="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber="
# input page number in between these two strings
#link_end="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"
pages=[]
product_numbers=list()

def getProductNumbersFromPage(product_numbers,link):
    page = requests.get(link)
    initial_prod_nums=extractProductNumber(page)
    page.close    
    try:
        product_numbers.extend(initial_prod_nums)
    except:
        product_numbers=initial_prod_nums        
    product_numbers=list(set(list(product_numbers)))
    return product_numbers

    
# search_attributes=["startOfSale-desc","startOfSale-asc","priceWithPant-desc","priceWithPant-asc"]
# latter one with no redundancies
search_attributes=["startOfSale-desc","startOfSale-asc"]

# number of items atm
def getNumberOfItems():
    link="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber=9&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"
    page = requests.get(link)
    soup=BeautifulSoup(page.content,'html.parser')
    number=soup.find('span', class_="color-primary")
    number=int(number.get_text().replace(u'\xa0', u''))
    return number

try:
    num_of_products=getNumberOfItems()
except:
    num_of_products=9000
# num of pages
num_of_pages=math.ceil((num_of_products/12)/2)+1

page_num=str(num_of_pages)
for attribute in search_attributes:
    # parse link url
    link2_start="&SortingAttribute="
    link2_end="&PageNumber="
    link2=link2_start+attribute+link2_end
    link=link1+link2+page_num+link3+link4

    product_numbers=getProductNumbersFromPage(product_numbers,link)
    
    print("iteration: "+attribute+", unique product numbers: "+
          str(len(product_numbers))+
          ", "+str(round(100*len(product_numbers)/8752))+" %")

len(product_numbers)    


if 1==0:
    soup=BeautifulSoup(page.content,'html.parser')
    product_number_lines=soup.find_all('span', class_="product-availability-symbol")
    extractProductNumFromLine(str(product_number_lines[0]))
    temp=extractProductNumber(page)

now = datetime.datetime.now()
now=str(now.strftime("%Y-%m-%d"))
with open('data-files/product_numbers_'+now+'.csv', 'w+') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(product_numbers)
writeFile.close()
    