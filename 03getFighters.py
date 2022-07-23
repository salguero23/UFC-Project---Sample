'''
Web scrape all of the fighter carrer stats
'''


import pandas as pd
from time import sleep
from tqdm import tqdm
import os
import fighterScraper as scraper

path = os.getcwd()
PAGES = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
df = pd.DataFrame()

for page in tqdm(PAGES):
    url = f'http://ufcstats.com/statistics/fighters?char={page}&page=all'
    
    try:
        soup = scraper.soupify(url)
        table = scraper.get_table(soup)
        temp_df = scraper.scrape_table(table)

        df = pd.concat([df,temp_df])

    except:
        print(f'Error at {url}')

    sleep(1)


# Now we iterate through each link to grab career stats
LINKS = df['Link'].values
career_df = pd.DataFrame()
career_error = pd.DataFrame(columns=['Error'])

for link in tqdm(LINKS):
    try:
        temp_df = scraper.scrape_career(link)
        career_df = pd.concat([career_df,temp_df])

    except:
        try: # try again
            temp_df = scraper.scrape_career(link)
            career_df = pd.concat([career_df,temp_df])
        except:
            print(f'An error occured at {link}')
    
    sleep(1)


# Merge data on link and then save to csv
data = pd.merge(df,career_df)
data.to_csv(f'{path}\\Data\\Raw - fighterMetrics.csv',index=False)