'''
Scaper tool for fighter career statistics

'''


import requests
from bs4 import BeautifulSoup
import pandas as pd


# Define a function that will establish the connection to our desired webpage
def soupify(URL):
    html = requests.get(URL)
    soup = BeautifulSoup(html.content, 'html.parser')

    return soup




# Define a function that will locate the table off of the html page
def get_table(soup):
    table = soup.find_all('table')[0]

    return table




# Define a function that will scrape the table we located
def scrape_table(table):

    # First, let us find our table headers and secure our data rows
    headers = [col.text.strip() for col in table.find_all('th')]
    headers.append('Link')
    DATA = table.find_all('tr')[2:]

    # Initialize variables
    firstName, lastName, nickName = [], [], []
    height, weight, reach, stance = [], [], [], []
    win, loss, draw, champ = [], [], [], []
    link = []

    # Iterate through each row
    for fighter in DATA:

        # Append data
        firstName.append(fighter.find_all('a')[0].text.strip())
        lastName.append(fighter.find_all('a')[1].text.strip())
        nickName.append(fighter.find_all('a')[2].text.strip())

        height.append(fighter.find_all('td')[3].text.strip())
        weight.append(fighter.find_all('td')[4].text.strip())
        reach.append(fighter.find_all('td')[5].text.strip())
        stance.append(fighter.find_all('td')[6].text.strip())

        win.append(fighter.find_all('td')[7].text.strip())
        loss.append(fighter.find_all('td')[8].text.strip())
        draw.append(fighter.find_all('td')[9].text.strip())
        champ.append(len(fighter.find_all('img')))

        link.append(fighter.find_all('a')[0]['href'])
    
    # Zip our data and return it as a pandas df
    ZIPPED_DATA = zip(firstName,lastName,nickName,height,weight,reach,stance,win,loss,draw,champ,link)
    df = pd.DataFrame(columns=headers,data=ZIPPED_DATA)

    return df


# Define a function to go to each profile and get career statistics
def scrape_career(link):
    soup = soupify(link)

    headers, data = [], []

    for _ in range(8,17):
        _ = _ if _ != 12 else _+1 

        temp = soup.find_all('li')[_].text.split('\n')
        headers.append(list(filter(lambda x: x != '',temp))[0].strip()[:-1])
        data.append(list(filter(lambda x: x != '',temp))[2].strip())

    headers.append('Link')
    data.append(link)
    df = pd.DataFrame(index=headers,data=data).T

    return df