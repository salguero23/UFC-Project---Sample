'''

This file will webscrape each fight in the UFC and store into a file known as rawData.csv.
fighLinks.py must be ran before running this file to ensure to have the latest fights in the UFC.

'''


import pandas as pd
from tqdm import tqdm
import scraper as sc
import time
import os

path = os.getcwd()
fights = pd.read_csv(f'{path}\\Data\\fights.csv')
links = fights.values.reshape(len(fights),)
error_links = []

df = pd.DataFrame()
for link in tqdm(links):
    try:
        soup = sc.soupify(link)
        totals, signifigants = sc.get_table(soup=soup)
        totals_df, sig_df = sc.scrape_table(totals), sc.scrape_table(signifigants)

        data = sc.merge_df(totals_df,sig_df)
        data = sc.finalize_df(df=data,soup=soup)

        df = pd.concat([df,data])
        time.sleep(1.5)
    
    except:
        error_links.append(link)
        print(f'An error occured for {link}')

error_links_df = pd.Series(error_links)
error_links_df.to_csv('D:/OneDrive/Documents/UFC/Data/errors.csv',index=False)

df.to_csv(f'{path}\\Data\\rawData.csv',index=False)