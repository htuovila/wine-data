#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:45:49 2019

@author: Heppa
"""

link="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber=9&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"

import requests
from bs4 import BeautifulSoup
import re
import csv
import datetime

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
link2="&SortingAttribute=&PageNumber="
link3="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%"
link4="3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"

link_start="https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber="
# input page number in between these two strings
link_end="&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3D6Q7AqG5uhTIAAAFVOmkI2BYA%26OnlineFlag%3D1"
pages=[]
product_numbers=list()
start_iteration=600
# change 1 and 2 to bigger numbers once finished
for i in range(50,100):
    # parse full link string with page number in the middle
    link=link1+link2+str(i)+link3+link4
    page = requests.get(link)
    initial_prod_nums=extractProductNumber(page)
    page.close    
    try:
        product_numbers.extend(initial_prod_nums)
    except:
        product_numbers=initial_prod_nums
        
    product_numbers=list(set(list(product_numbers)))
    print("iteration: "+str(i)+", unique product numbers: "+
          str(len(product_numbers))+
          ", "+str(round(100*len(product_numbers)/8752))+" %")
#    pages.append(page)
# end with pages object with list of pages


len(product_numbers)    


if 1==0:
    soup=BeautifulSoup(page.content,'html.parser')
    product_number_lines=soup.find_all('span', class_="product-availability-symbol")
    extractProductNumFromLine(str(product_number_lines[0]))
    temp=extractProductNumber(page)

now = datetime.datetime.now()
now=str(now.strftime("%Y-%m-%d"))
with open('wine-data/data-files/product_numbers_'+now+'.csv', 'w+') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(product_numbers)
writeFile.close()
    