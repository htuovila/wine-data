# this file is to combine downloaded data (csv files)
# to one big dataframe (and big file)

import csv
import os
import pandas as pd

path='data-files'

file_list=os.listdir(path)
print(file_list)

for file in file_list:
    if file!="older":
        print(path+"/"+file)
        data=pd.read_csv(path+"/"+file,dtype={'PRODUCT NUMBER': str})
        try:
            df_all=df_all.append(data,ignore_index=True)
            #print("dataframe shape: "+str(df_all.shape))
        except Exception as error:
            # case when we are on the first iteration
            print(error)
            df_all=data

print("dataframe size: "+str(df_all.shape))
df_all.to_csv("wine_data_all.csv")
print("end")


df_all.to_csv("combined_data_files.csv")
data_from_file=pd.read_csv("combined_data_files.csv")