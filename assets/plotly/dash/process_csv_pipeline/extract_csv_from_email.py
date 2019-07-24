#!/usr/bin/python


from google_api import *
import time
import datetime
from utils import *
import numpy as np
import pandas as pd
from SubGridBuilder import *
import matplotlib.pyplot as plt

print("{} Extracting csv from email {}".format('-'*10, '-'*10))
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

# ### Convert to DF
item = csvs_and_excel[0]
df = item['data']
print('email: ' + item['emailsubject'])
print('filename: ' + item['filename'])
print("data sample: ")

print(df.head())
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

df = to_grid(df, gridparams.default_lat_border, gridparams.default_lon_border)

# # sum fires on grid for every timestep
df['fire count'] = df.groupby(['lat_grid', 'lon_grid', 'timestamp'])['will_use'].transform('sum')

df.drop(['latitude', 'longitude', 'will_use'], axis=1, inplace=True)

df.drop_duplicates(inplace=True)

# sort by fire_count to find cells with most intense fire
df.sort_values('fire count', inplace=True)

if df['satellite'].nunique() > 1:
	# build dataframes for the terra and aqua satellites to avoid sum their close observations
	s1_df = df.loc[(df['satellite'].isin(['A', 'Aqua']))]
	s2_df = df.loc[(df['satellite'].isin(['T', 'Terra']))]

	# sort by timestamp
	s1_df.sort_values('timestamp', inplace=True)
	s2_df.sort_values('timestamp', inplace=True)

	# pivot on fire_count
	s1_pivot = s1_df.pivot_table(values='fire count', index='timestamp', columns=['lat_grid', 'lon_grid'])
	s2_pivot = s2_df.pivot_table(values='fire count', index='timestamp', columns=['lat_grid', 'lon_grid'])

	# fill NaN with zero
	s1_pivot.fillna(0, inplace=True)
	s1_pivot.sort_index(inplace=True)

	s2_pivot.fillna(0, inplace=True)
	s2_pivot.sort_index(inplace=True)

	## reset index
	s1_pivot = reset_index(s1_pivot)
	s2_pivot = reset_index(s2_pivot)

	# calculate the time differences of rows
	s1_pivot['time_diff'] = s1_pivot['timestamp'].diff()
	s2_pivot['time_diff'] = s2_pivot['timestamp'].diff()

	# if time_diff is small enough for the same satellite
	# we consider it the same observation over different parts of our grid cell, 
	# so give them same date, upon this same date later we can group our data
	s1_pivot.loc[s1_pivot['time_diff'] <= pd.Timedelta('0 days 00:05:00'), 'timestamp'] = s1_pivot['timestamp'].shift()
	s2_pivot.loc[s1_pivot['time_diff'] <= pd.Timedelta('0 days 00:05:00'), 'timestamp'] = s2_pivot['timestamp'].shift()

	# and we gopub by the timestamp, where the close ones are in the same group
	s1_pivot = s1_pivot.groupby(['timestamp']).sum()
	s2_pivot = s2_pivot.groupby(['timestamp']).sum()

	# get back the whole dataset
	data_pivot = s1_pivot.append(s2_pivot)

else:

	df.sort_values('timestamp', inplace=True)
	# pivot on firecount
	df_pivot = df.pivot_table(values='fire count', index='timestamp', columns=['lat_grid', 'lon_grid'])
	# fill NaN with zero
	df_pivot.fillna(0, inplace=True)
	df_pivot.sort_index(inplace=True)
	# reset index
	data_pivot = df_pivot.groupby('timestamp').sum()

# # resort by timestamp
data_pivot.sort_values('timestamp', inplace=True)

# # if there are observations of the two satellites in the same 12 hour period they are averaged
data_pivot_rs = data_pivot.resample('12H').mean()

# # simple linear interpolation for filling th gaps
data_pivot_rs = data_pivot_rs.interpolate(method='linear')
data_pivot_rs = reset_index(data_pivot_rs)
# # # reset timestamp column to new resampled time
# data_pivot_rs['timestamp'] = data_pivot_rs.index

# # # unpivot dataframe
data_pivot_rs = data_pivot_rs.melt(id_vars=['timestamp'], value_name='fire count')
data_pivot_rs[['lat', 'lon']] = pd.DataFrame(data_pivot_rs['variable'].tolist(), index=data_pivot_rs.index)
data_pivot_rs.drop('variable', inplace=True, axis=1)

# # # we want only a sample with fire count greater than 0 for the dashboard
sample = data_pivot_rs[data_pivot_rs['fire count'] > 0.]

# # # create categories for the dash display
bins = [0,1,5,10,100]
labels = ['(-0.001, 1.0]', '(1.0, 5.0]', '(5.0, 10.0]', '(10.0, 100.0]']
binned = pd.cut(sample['fire count'], bins=bins,include_lowest=True, labels=labels)
sample['fire count category'] = binned

# create timestep feature
sample.sort_values('timestamp', inplace=True)
sample.reset_index(inplace=True, drop=True)
timesteps = pd.to_datetime(sample['timestamp'])
start_day = sample['timestamp'].dt.day[0] # get the first day
start_time = sample['timestamp'].dt.hour[0] # get the first hour
timestep = 12
second_time = 0 if start_time == 12 else 12
timestep_conversion = {start_day:{start_time:timestep, second_time: timestep*3}, start_day+1:{second_time: timestep*2, start_time:timestep*4}}
sample['timestep'] = sample['timestamp'].apply(lambda x: timestep_conversion[x.day][x.hour])

sample.to_csv('nrt/{}_processed.csv'.format(datetime.datetime.now()), index=False)
