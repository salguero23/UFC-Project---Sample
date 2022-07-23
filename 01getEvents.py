'''

This file will return the link to each UFC EVENT.

'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

path = os.getcwd()
url = 'http://ufcstats.com/statistics/events/completed?page=all'
html = requests.get(url)
soup = BeautifulSoup(html.content)

columns = ['Date','Event','Location', 'Link']

table = soup.find('table')
links = table.find_all('a')
dates = table.find_all('span')
rows = table.find_all('tr')


date_lst, event_lst, loc_lst, link_lst =  [], [], [], []


for link in links[1:]:
    event_lst.append(link.text.strip())
    link_lst.append(link['href'])
    # print(link.text.strip() + ': ' + link['href'])
for date in dates[1:]:
    date_lst.append(date.text.strip())
for row in rows[3:]:
    loc_lst.append(row.find_all('td')[1].text.strip())

df = pd.DataFrame()
df['Date'] = date_lst
df['Event'] = event_lst
df['Location'] = loc_lst
df['Link'] = link_lst

df.to_csv(f'{path}\\Data\\events.csv',index=False)
print(df)