'''

This file will use the csv file generated from getEvents.py to return the
links to each fight on the UFC stats pages. getEvents.py must be ran prior to
ensure the latest fights are accounted for.

'''


import pandas as pd
import requests
import time
from tqdm import tqdm
import os
from bs4 import BeautifulSoup

path = os.getcwd()
events = pd.read_csv(f'{path}\\Data\\events.csv')
links = list(events['Link'])
link_lst = []

for idx, link in enumerate(tqdm(links)):
    fileName = events.iloc[idx]['Event']
    html = requests.get(link)
    soup = BeautifulSoup(html.content)

    table = soup.find('table')
    rows = table.find_all('tr')
    
    for row in rows[1:]:
        data = row.find('td')
        a = data.find('a')
        link_lst.append(a['href'])

    time.sleep(3)

series = pd.Series(link_lst)

series.to_csv(f'{path}\\Data\\fights.csv',index=False)