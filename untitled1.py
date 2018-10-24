# -*- coding: utf-8 -*-
"""
Copyright 2018, Prasad Tengse
This Project is Licensed under MIT License
"""
import requests
import re
from bs4 import BeautifulSoup
LOS_REL_TYPE = []
LOS_VERSION = []
LOS_URL = []
LOS_SIZE = []
LOS_DATE = []
los_download_page = requests.get("https://download.lineageos.org/marlin")
soup = BeautifulSoup(los_download_page.content, features="lxml")
table = soup.find('table')
for tr in table.find_all('tr'):
    td = tr.find_all('td')
    if len(td) == 5: # Making sure not to grab header
        LOS_REL_TYPE.append(td[0].string)
        LOS_VERSION.append(td[1].string)
        LOS_URL.append((td[2].a).get('href'))
        LOS_SIZE.append(td[3].string)
        LOS_DATE.append(td[4].string)
print(LOS_URL)