# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License
"""

import requests 
from bs4 import BeautifulSoup
zip_links = []
res = requests.get("https://download.lineageos.org/marlin")
soup = BeautifulSoup(res.content, features="lxml")
table = soup.find('table')
table_rows = table.find_all('tr')
for tr in table_rows:
    td = tr.find_all('td')
    if len(td) == 5:
        link_row = [i.a for i in td]
        data_row = [i.string for i in td]
        print(data_row)
        print(link_row[2])

del data_row, link_row
for tr in table_rows:
    td = tr.find_all('td')
    if len(td) == 5:
        for i in range(0,len(td)):
            print ("%d ====== %s",i,td[i].a)
        #link_row = [i.a for i in td]
        #data_row = [i.string for i in td]
        #print(data_row)
        #print(link_row[2])