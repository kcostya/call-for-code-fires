import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
## util functions for grid building
def preprocess(df):
    # add timestamp column
    df['timestamp'] = pd.to_datetime(df['acq_date'].astype('str')+df['acq_time'].astype('str'), format='%Y-%m-%d%H%M', exact=True)

    # convert confidence to binary, use two digits percentages
    df['will_use'] = (df['confidence'] > 10) * 1

    # define columns we will not need and drop them inplace
    drop_cols = [x for x in df.columns if x not in ['latitude','longitude','satellite', 'timestamp', 'will_use']]

    df.drop(drop_cols, axis=1, inplace=True)
    return df       
        
def to_grid(df, lat_border, lon_border):
    df.loc[:,'lat_borders'] = pd.cut(df.loc[:,'latitude'], lat_border)
    df.loc[:,'lon_borders'] = pd.cut(df.loc[:,'longitude'], lon_border)
    df.dropna(inplace=True)
    df.reset_index(inplace=True, drop=True)
    df = df.groupby(['lat_borders', 'lon_borders']).apply( lambda x: x.reset_index(drop=True))
    df.reset_index(drop=True, inplace=True)
    df.loc[:,'lat_grid'] = df.loc[:,'lat_borders'].apply(lambda x: x.mid)
    df.loc[:,'lon_grid'] = df.loc[:,'lon_borders'].apply(lambda x : x.mid)
    df.drop(['lat_borders','lon_borders'], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def plot_fires(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, df, title, years=[2017, 2018]):
    lons = df.groupby('year')['longitude'].apply(list)
    lats = df.groupby('year')['latitude'].apply(list)

    plt.figure(1, figsize=(24,12))

    m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution='l', 
                projection='cass', lat_0 = 35, lon_0 = -118.)
    m.bluemarble()
    m.shadedrelief()
    for idx, year in enumerate(years):
        colors= ['#6f0404', '#d00000', '#891212','#ddff44','#e6d461','#eead3d','#f7833a','#ff5a36','#C0392B','#922B21']
        x, y = m(lons[year], lats[year])
        m.scatter(x,y, s=3, marker='D', color=colors[idx], alpha=0.6)
        
    m.drawstates(linewidth=0.5, color="k") 
    m.drawcountries(linewidth=0.5, color="k")  
    plt.title(title)
    plt.legend(years)
    plt.show()
    
# the default grid with annotation showing the fire count
# added aggfun parameter, somewhere we need count (fire count), other places mean (population density)
def map_with_heatmap(df, value, annot=False, cmap='tab20b', aggfunc=np.sum):
    map_df = df.pivot_table(index="lat_grid", columns="lon_grid", values=value, aggfunc=aggfunc)  
    f, ax = plt.subplots(figsize=(9, 9))
    sns.heatmap(map_df, annot=annot, cmap=cmap, annot_kws={"fontsize":8}, linewidths=.0, ax=ax)
    ax.invert_yaxis()
    
def reset_index(df):
    '''Returns DataFrame with index as columns'''
    index_df = df.index.to_frame(index=False)
    df = df.reset_index(level='timestamp', drop=True)
    #  In merge is important the order in which you pass the dataframes
    # if the index contains a Categorical. 
    # pd.merge(df, index_df, left_index=True, right_index=True) does not work
    return pd.merge(index_df, df, left_index=True, right_index=True)    


# reduce memory usage by converting to proper data types
def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))

    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else: df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

    return df