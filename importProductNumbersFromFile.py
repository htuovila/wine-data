#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:35:56 2019

@author: Heppa
"""

import os
import re
import datetime

def getProductNumbers():
    path=os.path.dirname(os.path.abspath(__file__))
    
    print(path)
    
    # id unique product numbers exist
    try:
        del unique_product_numbers
    except:
        pass
    
    if 'unique_product_numbers' in locals():
        1+1
    else:
        now = datetime.datetime.now()
        now=str(now.strftime("%Y-%m-%d"))
        filename='data-files/product_numbers_'+now+'.csv'
        with open(filename) as csvfile:
            unique_product_numbers=csvfile.read()
    unique_product_numbers=re.split(',',unique_product_numbers)
    print("unique product numbers: "+str(len(unique_product_numbers)))
    return unique_product_numbers

if __name__=="__main__":
    temp=getProductNumbers()
    print(len(temp))
