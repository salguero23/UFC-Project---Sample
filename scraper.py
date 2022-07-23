'''

Functions to use whe webscraping the tables for each UFC fight.

'''

import requests
from bs4 import BeautifulSoup
import pandas as pd


def soupify(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    return soup

def get_table(soup):
    tables = soup.find_all('table')
    totals = tables[0]
    signifigant = tables[2]

    return totals, signifigant

# Define function to scrape aggregate table
def scrape_table(table):

    headers = table.find_all('th')
    columns = []

    for item in headers:
        columns.append(item.text.strip())

    Rcolumns, Bcolumns = [], []
    for col in columns:
        Rcolumns.append('R_' + col)
        Bcolumns.append('B_' + col)

    data = table.find_all('td')
    red, blue = dict(), dict()
    for idx, col in enumerate(Rcolumns):
        red[col] = data[idx].find_all('p')[0].text.strip()
    for idx, col in enumerate(Bcolumns):
        blue[col] = data[idx].find_all('p')[1].text.strip()
    
    red.update(blue)
    data = red
    df = pd.DataFrame(data,index=[0])

    return df


# Define function to merge and clean columns for two dataframes
def merge_df(df1,df2):

    df = pd.merge(df1,df2)
    df.drop(columns=['R_Sig. str', 'B_Sig. str'],inplace=True)

    a_list = []
    b_list = []
    for col in df.columns:
        if col[0] == 'R':
            a_list.append(col)
        else:
            b_list.append(col)

    columns = a_list + b_list
    df = df[columns]

    return df



# Define function that will scrape who won the fight, if the fight ended in a draw or no contest
def winner(soup):
    div = soup.find_all('div',attrs={'class': 'b-fight-details__person'})
    result = div[0].find('i').text.strip()

    if result == 'W':
        return 'Red'
    elif result == 'L':
        return 'Blue'
    elif result == 'D':
        return 'Draw'
    else:
        return 'No Contest'



# Define function that will scape how and when the fight ended
def fight_result(soup):
    p = soup.find('p',attrs={'class':'b-fight-details__text'})
    i = p.find_all('i')
    results = dict()

    results['Method'] = i[2].text.strip()
    results['Round'] = i[3].text.strip()[-2:].strip()
    results['Time'] = i[5].text.strip()[-6:].strip()

    return results



# Define function that will determine what division the bout was fought at
def get_division(soup):
    words_to_replace = ['UFC','Title','Bout', 'Interim','Tournament','Ultimate Fighter']

    i = soup.find_all('i',attrs={'class':'b-fight-details__fight-title'})
    division = i[0].text.strip()
    for word in words_to_replace:
        division = division.replace(word,'')
    division = division.strip()

    return division



def title_bout(soup):
    i = soup.find_all('i',attrs={'class':'b-fight-details__fight-title'})
    division = i[0].text.strip()   

    if 'Title' in division:
        return 1
    else:
        return 0



# Scrape the event the fight was fought at
def get_event(soup):
    event = soup.find_all('h2')[0].text.strip()

    return event



# Use functions to append to dataframe
def finalize_df(df,soup):
    df['Winner'] = winner(soup)
    df['Division'] = get_division(soup)
    df['Title_Bout'] = title_bout(soup)
    df['Event'] = get_event(soup)

    df['Method'] = fight_result(soup)['Method']
    df['Round'] = fight_result(soup)['Round']
    df['Time'] = fight_result(soup)['Time']

    return df