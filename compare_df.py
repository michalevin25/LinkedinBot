# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 22:29:01 2022

@author: micha
"""
import pandas as pd
# previous excel
df_prev = pd.read_excel('companies 2022-10-01.xlsx')
# 
df_curr = pd.read_excel('companies 2022-10-02.xlsx')


for index, row in df_prev.iterrows():
    prev_jobtitle = row['Job Title']
    prev_company  = row['Company name']
    a = df_curr[df_curr['Job Title'].eq(prev_jobtitle) == True]
    b = a[a['Company name'].eq(prev_company) == True]

    df_compared = df_curr.drop(b.index)



df_compared.to_excel('compared.xlsx')