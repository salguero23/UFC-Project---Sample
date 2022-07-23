'''

This file will clean the rawData.csv file to format strings into floats
and remove unnecessary data entires. Will also clean the Raw - fighterMetrics.csv

'''

import pandas as pd
import numpy as np
import os
import re

path = os.getcwd()

# Call in our data
df = pd.read_csv(f'{path}\\Data\\rawdata.csv')
df_copy = df.copy() # Save a copy of our oringinal data
events = pd.read_csv(f'{path}\\Data\\events.csv')
events = events[['Date','Event','Location']]

# Merge data and convert date to time
df = pd.merge(df,events)
df['Date'] = pd.to_datetime(df['Date'])

# Remove percentage columns
columns_to_keep = [col for col in df.columns if '%' not in col]
df = df[columns_to_keep]



# Seperate landed and attempted values into their own features
columns_to_seperate = [col for col in df.columns if 'of' in str(df[col][0])]
columns_to_keep = [col for col in df.columns if 'of' not in str(df[col][0])]
df_of = df[columns_to_seperate]
df.drop(columns=columns_to_seperate,inplace=True)

for col in df_of:
    landed, attempted = [], []
    series = df_of[col].apply(lambda x: x.split('of'))

    for i in range(len(series)):
        landed.append(series.iloc[i][0])
        attempted.append(series.iloc[i][1])

    df_of[f'{col}_Landed'] = landed
    df_of[f'{col}_Attempted'] = attempted
    df_of[f'{col}_Landed'] = df_of[f'{col}_Landed'].astype('float64')
    df_of[f'{col}_Attempted'] = df_of[f'{col}_Attempted'].astype('float64')

    df_of.drop(columns=col,inplace=True)

df = pd.concat([df,df_of],axis=1)
df.fillna(0.0,inplace=True)


# Convert control features to float type
time_columns = ['R_Ctrl','B_Ctrl']
for col in time_columns:
    minutes, seconds = [], []
    series = df[col].apply(lambda x: x.split(':'))

    for i in range(len(series)):
        if series.iloc[i] != ['--']:
            minutes.append(series.iloc[i][0])
            seconds.append(series.iloc[i][1])
        else:
            minutes.append(0)
            seconds.append(0)
    
    minutes = np.array(minutes).astype('float64')
    seconds = np.array(seconds).astype('float64')
    seconds = np.round(seconds/60.0, 2)
    time = minutes + seconds

    df[col] = time


# Due to inconsistencies with the UFCs reporting we will drop some of the bias data
# df = df[:5400]


# Clean division data

# Define a function to remove the numbers from the division column
def remove_numbers(string):
    x = re.sub(pattern=r'\d',repl='',string=string)
    return x.strip()

df['Division'] = df['Division'].apply(lambda x: remove_numbers(x))
# Remove text data from divisions
words_to_remove = ['China','Brazil','Australia','vs.','UK','TUF Nations','Canada','Latin America']
for word in words_to_remove:
    df['Division'] = df['Division'].apply(lambda x: x.replace(word,'').strip())



# Save data to csv and print the top of the dataframe
df.to_csv(f'{path}\\Data\\cleanedData.csv',index=False)
df_ = df.copy()
print(df_.head())



# ---------------------------------------------------------------------------------------------------------------------
# Now we clean our fighter career statistics

# We first want to import our career stats data to clean
df = pd.read_csv(path + '\\Data\\Raw - fighterMetrics.csv')
df_copy = df.copy()
# Merge first and last name into a column called fighter
df['Fighter'] = df['First'] + ' ' + df['Last']
df.drop(columns=['First','Last','TD Avg..1'],inplace=True)

# Clean height, weight and reach data
# Define a function to convert height string into float and check for na
def convert_height(value):
    if value != '--':
        # Check if inches is in double digits
        if len(value) == 6:
            feet = float(value[0])
            l_inch = value[3]
            r_inch = value[4]
            inches = float(l_inch+r_inch) / 12.0

            height = np.round(feet + inches,2)

        else: # inches is single digit
            feet = float(value[0])
            inches = float(value[3]) / 12.0

            height = np.round(feet + inches,2)

    else: # if data is missing is value equal to NaN
        height = np.nan

    return height


# Define a function to convert weight into a float
def convert_weight(value):
    if value != '--':
        weight = float(value.split('lbs')[0].strip())
    else:
        weight = np.nan

    return weight


# Define a function to convert reach into a float
def convert_reach(value):
    if value != '--':
        reach = value[:4]
        reach = float(reach.split('.')[0])

    else:
        reach = np.nan

    return reach


df['Ht.'] = df['Ht.'].apply(lambda x: convert_height(x))
df['Wt.'] = df['Wt.'].apply(lambda x: convert_weight(x))
df['Reach'] = df['Reach'].apply(lambda x: convert_reach(x))


# All that is left is to clean the percentage data into a decimal
def clean_percents(value):
    percentage = float(value[:-1]) / 100.0

    return percentage


percent_columns = ['Str. Acc.','Str. Def','TD Acc.','TD Def.']
for column in percent_columns:
    df[column] = df[column].apply(lambda x: clean_percents(x))


sortedColumns = ['Fighter','Nickname','Ht.','Wt.','Reach','Stance','W','L','D','Belt','SLpM','Str. Acc.','SApM','Str. Def','TD Avg.',
                'TD Acc.','TD Def.','Sub. Avg.','Link']

df = df[sortedColumns]
# Rename percent columns and save data
df.rename(columns={'Str. Acc.':'Str Acc. (pct)','Str. Def':'Str Def. (pct)','TD Acc.':'TD Acc. (pct)','TD Def.':'TD Def. (pct)'},inplace=True)
df.to_csv(path + '\\Data\\Cleaned - fighterMetrics.csv',index=False)