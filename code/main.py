#!/usr/bin/env python
# coding: utf-8

# # Assessment 2: Story telling

# ## Given the location data set, take any three tourist places in Kula Lumpur and tell us the story on tourism and visitors. State out the assumptions.

# ### I selected the following tourist places:
# 
# 1. Perdana Botanical Garden
# 2. Chinatown
# 3. Petronas towers
# 
# I chose these different types (natural, cultural, and modern) of tourist points to analyze how they differ from each other.
# 
# ### I identify 500m buffer from the central point of these areas as the study areas in this exercise.
# In this way, I can:
# 
# 1. keep the total area the same for all the points
# 2. overcome the ambiguous area boundaries for Petronas towers and Chinatown in a simple manner
# 
# ### I will analyze the tourist places by examining the following aspects:
# 
# 1. Spatio-temporal distribution of devices
# 2. Movement of each device: first&last timestamp, duration, and distance moved
# 
# This analysis should inform when people visit where for how long. And how much they move within the area.
# 
# ### I will conduct this exercise in the following steps:
# 
# 0. A brief exploration of the data
# 1. Create 500m buffers around the selected tourist points
# 2. Extract those points that intersect with the buffer
# 3. Group by each device id to get first&last timestamp, duration, and distance moved
# 4. Visualize the spatio-temporal distribution of devices

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point, LineString, shape
from geopandas.tools import sjoin
import contextily as ctx
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm
import geoplot


# ## 0. A brief exploration of the data
# - Check date range, the distribution of the points, the number of unique device id

# In[2]:


# import data
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
file_name=os.path.join(parentDirectory,'data','location_data.csv')
location_data=pd.read_csv(file_name)

# date range
location_data['timestamp']=pd.to_datetime(location_data['timestamp'],unit='s')
print(f"The range of the datetime of the data is from {location_data['timestamp'].min()} to {location_data['timestamp'].max()}")

# distribution of the points
location_data['geometry']=location_data.apply(lambda x: Point((float(x.longitude), float(x.latitude))), axis=1)
location_data_gdf=gpd.GeoDataFrame(location_data, geometry='geometry')
location_data_gdf=location_data_gdf.set_crs(epsg=4326)
location_data_gdf=location_data_gdf.to_crs("EPSG:4398")
fig, ax = plt.subplots(1, figsize=(10, 10))
location_data_gdf.plot(figsize=(10, 10), alpha=0.5, edgecolor='k',ax=ax)
ctx.add_basemap(ax, crs="EPSG:4398", url=ctx.providers.OpenStreetMap.Mapnik,zoom=10)
ax.set_axis_off()
ax.set_title("Spatial Distribution of Devices in the Dataset", fontdict={"fontsize": "25", "fontweight" : "3"})
fig.savefig(os.path.join(parentDirectory,'output','point_distribution.png'))


# In[3]:


# the number of unique device id
num_unique_device=len(location_data_gdf['device_id'].unique())
num_rows=len(location_data_gdf)
print(f"There are {num_unique_device} unique device ids among {num_rows} observations")


# From the exploration, we know that locations of 40,961 devices were retrieved in Kuala Lumpur area on the New Year's day in 2021.
# For the following analysis, we have to keep in mind that:
# 
# 1. Given the current COVID situation, it is highly likely that there are only few tourists from outside the city
# 2. If the assumption that I just made is true, this data only represents about 2% of the population (40,961 out of 1.8 million) in Kuala Lumpur.  
# 3. I will still assume that the sample devices are appropriately representing the larger population.
# 4. Since the data were retrieved on the New Year's day, people's movement might be different from the usual times.
# 5. Further statistical analysis is needed for any points made in this report because this report is just exploratory and descriptive.

# ## 1. Create 500m buffers around the selected tourist points

# In[4]:


# create 100m buffer from Kuala Lumpur airport
def create_point(df,crs):
    """
    This function is used to create a point geo dataframe
        Input:
            - df: a pandas dataframe that contains the location information
            - crs: a string of target crs
        Output:
            - gdf: a geodataframe of the given point
    """
    df['geometry']=df.apply(lambda x: Point((float(x.lon), float(x.lat))), axis=1)
    gdf=gpd.GeoDataFrame(df, geometry='geometry')
    gdf = gpd.GeoDataFrame(df)
    gdf=gdf.set_crs(epsg=4326)
    gdf=gdf.to_crs(crs)
    return gdf

def create_buffer(gdf,buffer_distance):
    """
    This function is used to create buffer around given geodataframe with a specified distance
        Input:
            - gdf: input geo dataframe
        Output: 
            - buffer_poly: a buffer around the input gdf with the specified distance
    """
    buffer_poly = gdf.copy()
    buffer_poly["geometry"]=gdf.geometry.buffer(buffer_distance)
    return buffer_poly

# location of the selected points
#df=pd.DataFrame(names=['name','lon','lat'])
location_dict=dict()
location_dict['perdona']=[101.6847, 3.1430]
location_dict['chinatown']=[101.6969, 3.1428]
location_dict['petronas']=[101.7120, 3.1579]
df=pd.DataFrame.from_dict(location_dict,orient='index',columns=['lon','lat']).    reset_index().rename(columns={'index':'name'})
crs="EPSG:4398"

# create buffer
distance=500
gdf=create_point(df,crs)
buffer=create_buffer(gdf,distance)
print(buffer.head())


# ## 2. Extract those points that intersect with the buffer

# In[5]:


# coduct spatial join to extract points that intersect with the 100m buffer
joined_buffer = gpd.sjoin(location_data_gdf, buffer, how="left", op='intersects')
print(joined_buffer.info())


# ## 3. Group by each device id to get first&last timestamp, duration, and distance moved

# Here, I cannot detect if the device leaves the point area and come back again.

# In[6]:


# first & last timestamp & duration by tourist points
time_visited_by_device=joined_buffer.groupby(['device_id','name']).agg(['min','max'])
time_visited_by_device.columns = ['{}_{}'.format(x[0], x[1]) for x in time_visited_by_device.columns]
time_visited_by_device=time_visited_by_device.reset_index()
time_visited_by_device=time_visited_by_device[['device_id','name','timestamp_min','timestamp_max']]
time_visited_by_device['duration']=time_visited_by_device['timestamp_max']-time_visited_by_device['timestamp_min']
print(time_visited_by_device)


# In[7]:


# plot first timestamp
sns.set_style(style="whitegrid")
time_visited_by_device['timestamp_min_hour']=time_visited_by_device['timestamp_min'].dt.hour
fist_visit_bplot = sns.violinplot(y='timestamp_min_hour', x='name', 
                 data=time_visited_by_device, 
                 width=0.5,
                 palette="colorblind")
fist_visit_bplot.axes.set_title("Timestamp of First Visits by Tourist Point",
                    fontsize=16)
fist_visit_bplot.figure.savefig(os.path.join(parentDirectory,'output','first_visit_timestamp.png'))


# Chinatown seems to have been visited by devices slightly earlier than the other two points.
# 
# This might be due to the type of activity there, such as street markets.

# In[8]:


# plot last timestamp
time_visited_by_device['timestamp_max_hour']=time_visited_by_device['timestamp_max'].dt.hour
last_visit_bplot = sns.violinplot(y='timestamp_max_hour', x='name', 
                 data=time_visited_by_device, 
                 width=0.5,
                 palette="colorblind")
last_visit_bplot.axes.set_title("Timestamp of Last Visits by Tourist Point",
                    fontsize=16)
last_visit_bplot.figure.savefig(os.path.join(parentDirectory,'output','last_visit_timestamp.png'))


# This result tells us two things:
# 
# 1. Petroas tower area has visitors leaving there later than the other two points.
# 2. People tended to visit these points in the morning and leave by the noon. 

# In[9]:


# plot duration
time_visited_by_device['duration_min']=time_visited_by_device['duration'].dt.total_seconds().div(60).astype(int)
duration_bplot = sns.boxplot(y='duration_min', x='name', 
                 data=time_visited_by_device, 
                 width=0.5,
                 palette="colorblind")
duration_bplot.axes.set_title("Duration of Stays by Tourist Point",
                    fontsize=16)
duration_bplot.figure.savefig(os.path.join(parentDirectory,'output','duration.png'))


# Petronas tower area has longer duration of stays than the other two points, where most devices left the areas within 1 hour.
# 
# This might be due to the kinds of activities people engage in the different points, which I will not analyse in this exercise but can be further analyzed by, for example, correlating with types of POIs.

# In[10]:


# calculate the length of movements by each device
result_df=pd.DataFrame()
movements_gdf=gpd.GeoDataFrame()
for index,row in tqdm.tqdm(time_visited_by_device.iterrows()):
    device_id=row[0]
    name=row[1]
    temp_gdf=joined_buffer.loc[(joined_buffer['name']==name)&(joined_buffer['device_id']==device_id)]
    try:
        movement=temp_gdf.groupby(['device_id', 'name'])['geometry'].apply(lambda x:LineString(x.tolist()))
        movement = gpd.GeoDataFrame(movement, geometry='geometry')
        movements_gdf=movements_gdf.append(movement)
    except ValueError: # when we cannot convert it to linestring
        continue
    try:
        length=movement['geometry'].length.tolist()[0]
    except IndexError: # when there is anything inside movement['geometry'].length
        continue
    temp_df = pd.DataFrame([[device_id,name,length]], columns=['device_id','name','length'])
    result_df=result_df.append(temp_df)
movements_gdf=movements_gdf.reset_index()
print(result_df)


# In[11]:


# plot distance travelled by each device
distance_bplot = sns.boxplot(y='length', x='name', 
                 order=['perdona','petronas','chinatown'],
                 data=result_df, 
                 width=0.5,
                 palette="colorblind")
distance_bplot.axes.set_title("Distance Travelled by Each Device (meters)",
                    fontsize=16)
distance_bplot.figure.savefig(os.path.join(parentDirectory,'output','distance.png'))


# This result shows general consistency with the duration (i.e., the longer the device stays, the longer the distance travelled by the device is)

# In[12]:


# plot the movement in perdona on a map
movements_perdona=movements_gdf.loc[movements_gdf['name']=='perdona']
fig, ax = plt.subplots(1, figsize=(10, 10))
movements_perdona.plot(figsize=(10, 10), alpha=0.2, color='blue',edgecolor='blue',ax=ax,markersize=5)
ctx.add_basemap(ax, crs="EPSG:4398", url=ctx.providers.OpenStreetMap.Mapnik)
ax.set_axis_off()
ax.set_title("Movements of devices in Perdona", fontdict={"fontsize": "25", "fontweight" : "3"})
fig.savefig(os.path.join(parentDirectory,'output','movement_perdona.png'))


# From this map, you can see that people tend to walk on the trail in the park.

# In[13]:


# plot the movement in petronas on a map
movements_petronas=movements_gdf.loc[movements_gdf['name']=='petronas']
fig, ax = plt.subplots(1, figsize=(10, 10))
movements_petronas.plot(figsize=(10, 10), alpha=0.1, color='blue',edgecolor='blue',ax=ax,markersize=1)
ctx.add_basemap(ax, crs="EPSG:4398", url=ctx.providers.OpenStreetMap.Mapnik)
ax.set_axis_off()
ax.set_title("Movements of devices in petronas", fontdict={"fontsize": "25", "fontweight" : "3"})
fig.savefig(os.path.join(parentDirectory,'output','movement_petronas.png'))


# From this map, you can see generally higher number of movements and concentration of movements around the petronas towers.

# In[14]:


# plot the movement in chinatown on a map
movements_chinatown=movements_gdf.loc[movements_gdf['name']=='chinatown']
fig, ax = plt.subplots(1, figsize=(10, 10))
movements_chinatown.plot(figsize=(10, 10), alpha=0.1, color='blue',edgecolor='blue',ax=ax,markersize=1)
ctx.add_basemap(ax, crs="EPSG:4398", url=ctx.providers.OpenStreetMap.Mapnik)
ax.set_axis_off()
ax.set_title("Movements of devices in chinatown", fontdict={"fontsize": "25", "fontweight" : "3"})
fig.savefig(os.path.join(parentDirectory,'output','movement_chinatown.png'))


# The map shows high concentration of movements along the major roads, rather than the main street in chinatown. 

# ## 4. Visualize the spatio-temporal distribution of devices

# In[15]:


# plot the cumulative total number of devices by hour
device_in_points=joined_buffer.dropna(subset=['name'])
device_in_points['timestamp_hour']=device_in_points['timestamp'].dt.hour
device_in_points_count=device_in_points.groupby(['name','timestamp_hour']).agg(['count'])
device_in_points_count.columns = ['{}_{}'.format(x[0], x[1]) for x in device_in_points_count.columns]
device_in_points_count=device_in_points_count.reset_index()
count_lplot=sns.lineplot(data=device_in_points_count, x="timestamp_hour", y="device_id_count", hue="name")
count_lplot.axes.set_title("Cumulative Number of Devices by Hour", fontsize=16)
count_lplot.figure.savefig(os.path.join(parentDirectory,'output','cumulative_devices.png'))


# - Chinatown peaks around 6 and has another smaller peak towards midnight. This might be due to its morning and night market.
# - Perdona has a similar pattern as Chinatown but has lower numbers of devices in general.
# - Petronas generally has higher numbers of devices. Its peak stays high from 6am to 11am. A little spike around 18 might be due to those who eat dinner around Petronas. Just like Chinatown, the number of devices increases towards the midnight.

# In[16]:


# plot spatial distribution of devices 
name_list=['perdona','petronas','chinatown']
for name in name_list:
    devices=device_in_points.loc[device_in_points['name']==name]
    nrow=4
    ncol=6
    fig, axes = plt.subplots(nrow, ncol,figsize=(50, 50))
    buffer_temp= buffer.loc[buffer['name']==name]
    xlim = ([buffer_temp.total_bounds[0],  buffer_temp.total_bounds[2]])
    ylim = ([buffer_temp.total_bounds[1],  buffer_temp.total_bounds[3]])
    # plot counter
    hour=0
    for r in range(nrow):
        for c in range(ncol):
            devices_temp=devices.loc[devices['timestamp_hour']==hour]
            devices_temp.plot(alpha=0.5, color='blue',ax=axes[r,c],markersize=50)
            axes[r,c].set_xlim(xlim)
            axes[r,c].set_ylim(ylim)
            ctx.add_basemap(axes[r,c], crs="EPSG:4398", url=ctx.providers.Stamen.TonerLite)
            axes[r,c].set_axis_off()
            axes[r,c].set_title(f"Devices at {hour}", fontdict={"fontsize": "50", "fontweight" : "1"})
            hour+=1
    fig.tight_layout()
    fig.suptitle(f"Spatial Distribution of Devices by Hour in {name.capitalize()}", fontsize=100)
    fig.savefig(os.path.join(parentDirectory,'output',f'device_{name}_hour.png'))


# From these maps, you can see some devices are in Perdona in the morning. But generally, there are not many of them.
# 
# For Petronas, you can see that there are higher numbers of devices around Petronas from 6 to 11. The drastic decrease of devices at 12 is quite interesting.
# 
# Chinatown also shows the similar pattern as Petronas: higher numbers of devices in the morning and sudden decrease at 12.

# In[18]:


location_data_gdf
location_data_gdf['timestamp_hour']=location_data_gdf['timestamp'].dt.hour
nrow=4
ncol=6
fig, axes = plt.subplots(nrow, ncol,figsize=(50, 50))
xlim = ([location_data_gdf.total_bounds[0],  location_data_gdf.total_bounds[2]])
ylim = ([location_data_gdf.total_bounds[1],  location_data_gdf.total_bounds[3]])
# plot counter
hour=0
for r in range(nrow):
    for c in range(ncol):
        devices_temp=location_data_gdf.loc[location_data_gdf['timestamp_hour']==hour]
        devices_temp.plot(alpha=0.2, color='blue',ax=axes[r,c],markersize=20)
        axes[r,c].set_xlim(xlim)
        axes[r,c].set_ylim(ylim)
        ctx.add_basemap(axes[r,c], crs="EPSG:4398", url=ctx.providers.Stamen.TonerLite)
        axes[r,c].set_axis_off()
        axes[r,c].set_title(f"Devices at {hour}", fontdict={"fontsize": "50", "fontweight" : "1"})
        hour+=1
fig.tight_layout(h_pad=100)
fig.suptitle("Spatial Distribution of Devices by Hour in Kuala Lumpur", fontsize=100)
fig.subplots_adjust(top=0.8)
fig.savefig(os.path.join(parentDirectory,'output','device_hour.png'))


# In[ ]:




