#!/usr/bin/python


from google_api import *
import time
import datetime
from utils import *
import numpy as np
import pandas as pd
from SubGridBuilder import *
import matplotlib.pyplot as plt


curr_dt = datetime.datetime.now()
curr_dt = curr_dt.replace(hour=0, minute=0, second=0, microsecond=0)

##### Get CSV from email

GMAIL_CREDENTIALS_PATH = 'credentials.json'
GMAIL_TOKEN_PATH = 'token.pickle'

search_query = "FIRMS Rapid Alert"
service = gmail.get_gmail_service(GMAIL_CREDENTIALS_PATH,
                                  GMAIL_TOKEN_PATH)
# query and retrieve the csv attachments - for fire grid building we only want the timestamp, lat, lon, confidence (for QA), and satellite
# cols to read in
cols = ['latitude','longitude','satellite','acq_date', 'acq_time','confidence']
csvs_and_excel = gmail.query_for_csv_or_xl_attachments(service, search_query, cols=cols)

print("{} Extracting csv from {} email(s) {}".format('-'*10, len(csvs_and_excel), '-'*10))

dfs = []
for item in csvs_and_excel:
	df = item['data']
	print('email: ' + item['emailsubject'])
	print('filename: ' + item['filename'])
	print("data sample: ")
	print("")
	print("{}".format('-'*20))
	print("")
	print(df.head())
	print("")
	print("{}".format('-'*20))
	dfs.append(df)

df = pd.concat(dfs, axis=0, ignore_index=True)


# ### Convert to DF
item = csvs_and_excel[0]
df = item['data']
print("{} Extracting csv from email {}".format('-'*10, '-'*10))
print("")
print('email: ' + item['emailsubject'])
print('filename: ' + item['filename'])
print("data sample: ")
print("")
print("{}".format('-'*20))
print("")
print(df.head())
print("")
print("{}".format('-'*20))

##### Process the DF
df = reduce_mem_usage(df)
# add timestamp column, drop unnecessary columns, add will_use feature (for QA filtering)
df = preprocess(df)

## CA coords
llcrnrlon= -125.
llcrnrlat=32.5
urcrnrlon= -113.75
urcrnrlat=42.

# # we only want the data from CA for this demo
# df = df[(df['longitude'] <= urcrnrlon) & (df['longitude'] >= llcrnrlon) & (df['latitude'] <= urcrnrlat)  & (df['latitude'] >= llcrnrlat)]


# # convert coordinates to grid
gridparams = SubGridBuilder((llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat), (0.625, 0.5), 3)

data = to_grid(df, gridparams.default_lat_border, gridparams.default_lon_border)

# sum fires on grid for every timestep
data['fire count'] = data.groupby(['lat_grid', 'lon_grid', 'timestamp'])['will_use'].transform('sum')
data.drop(['latitude', 'longitude', 'will_use'], axis=1, inplace=True)
data.drop_duplicates(inplace=True)

data['satellite'] = np.where(data['satellite'].isin(['T','Terra']), 1, 2)

#Satellite moving problem
# As the satellite goes it observes an area below, then a minute later observes an other. 
#Sometime our grids cells have data from these subsequent observations, 
# because part of the cell is observed during the first, the other part during the next observation. 
# So we have to sum these rare cases when the subsequent satellite observations cover the whole cell.

# build dataframes for the terra and aqua satellites to avoid sum their close observations
s1_data = data.loc[(data['satellite'] == 1)]
s2_data = data.loc[(data['satellite'] == 2)]

if len(s1_data) > 0:
    s1_data = process_distinct_satellites(s1_data)
if len(s2_data) > 0:
    s2_data = process_distinct_satellites(s2_data)    

# get back the whole dataset
if (len(s1_data) > 0) & (len(s2_data) > 0):
    data_pivot = s1_data.append(s2_data)
elif (len(s1_data) > 0):
    data_pivot = s1_data
elif (len(s2_data) > 0):
    data_pivot = s2_data

data_pivot.sort_values('timestamp', inplace=True)

# # if there are observations of the two satellites in the same 12 hour period we get the last
data_pivot_rs = data_pivot #.resample('12H').last()

# reset index
data_pivot_rs = reset_index(data_pivot_rs)

# unpivot dataframe
data_pivot_rs = data_pivot_rs.melt(id_vars=['timestamp'], value_name='fire count')

data_pivot_rs['lat'], data_pivot_rs['lon'] = zip(*data_pivot_rs['variable'])
data_pivot_rs.drop(['variable'], axis=1, inplace=True)

# # # # we want only a sample with fire count greater than 0 for the dashboard
sample = data_pivot_rs[data_pivot_rs['fire count'] > 0.]

# # # # create categories for the dash display
bins = [0,1,5,10,100]
labels = ['(-0.001, 1.0]', '(1.0, 5.0]', '(5.0, 10.0]', '(10.0, 100.0]']
binned = pd.cut(sample['fire count'], bins=bins,include_lowest=True, labels=labels)
sample['fire count category'] = binned

# # create timestep feature
sample.sort_values('timestamp', inplace=True)
sample.reset_index(inplace=True, drop=True)
timesteps = pd.to_datetime(sample['timestamp'])
start_day = curr_dt#sample['timestamp'].dt.day[0] # get the first day
start_time = 0.#sample['timestamp'].dt.hour[0] # get the first hour
 
time = pd.date_range(start=curr_dt, freq='12h', periods=5)



timesteps = pd.cut(df['timestamp'], time, labels=[12, 24, 36, 48], include_lowest=True, right=False)
sample['timestep'] = timesteps

sample.to_csv('nrt/{}_processed.csv'.format(datetime.datetime.now()), index=False)
