# Story telling
## Given the location data set, take any three tourist places in Kula Lumpur and tell us the story on tourism and 




ors. State out the assumptions.


# 1.	Introduction
For this exercise, I selected the following tourist places:
1.	Perdana Botanical Garden,
2.	Chinatown,
3.	Petronas towers.
I chose these different types (natural, cultural, and modern) of tourist points to analyze how they differ from each other. I identified 500m buffers from the central point of these areas as the study areas in this exercise. 
This is because, in this manner, I can keep the total area the same for all the points and overcome the ambiguous area boundaries, such as Petronas towers and Chinatown, in a simple manner. I analyzed the tourist places by examining the following aspects:
1.	Spatio-temporal distribution of devices
2.	Movement of each device: first & last timestamp, duration, and distance moved
At the end of the analysis, this analysis should inform when people visit where for how long and how much they move within the area.
For the methodology, I conducted this exercise in the following steps:
0.	A brief exploration of the data
1.	Create 500m buffers around the selected tourist points
2.	Extract those points that intersect with the buffer
3.	Group by each device id to get first&last timestamp, duration, and distance moved
4.	Visualize the spatio-temporal distribution of devices

# 2.	Initial data exploration
Before conducting analysis, I checked date range, the number of unique device id, and the distribution of the points. The range of the datetime of the data is from 2021-01-01 00:00:00 to 2021-01-01 23:59:59. So it is the New Year’s day this year in 2021. The number of unique device id is 40,961 among about 1,180,000 observations. Thus, roughly, more than 25 observations per device id are recorded. The map below shows the spatial distribution of all the points recorded in the data, from which you can see that they were recorded in Kuala Lumpur.

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/point_distribution.png)

For the following analysis, we have to keep in mind that:
1.	Given the current COVID situation, it is highly likely that there are only few tourists from outside the city
2.	If the assumption that I just made is true, this data only represents about 2% of the population (40,961 out of 1.8 million) in Kuala Lumpur.  
3.	I still assumed that the sample devices are appropriately representing the larger population.
4.	Since the data were retrieved on the New Year's day, people's movement might be different from the usual times.
5.	Further statistical analysis is needed for any points made in this report because this report is just exploratory and descriptive.

# 3.	Visit time, duration, and distance travelled by devices
To understand when people enter the selected areas, I visualized the first timestamps recorded by unique device ids. The figure below shows that, generally speaking, the first visits are concentrated in the morning. Also, Chinatown has been visited by devices slightly earlier than the other two points. This might be due to the type of activity there, such as street markets.  

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/first_visit_timestamp.png)

I also visualized the last timestamps to see when visitors left the selected areas. This result tells us two things:
1.	The Petronas area has visitors leaving there later than the other two points.
2.	People tended to visit these points in the morning and leave by the noon. 

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/last_visit_timestamp.png)

From the first and last timestamp, I calculated the duration of stays by unique devices as well. The graph below shows that Petronas tower area has longer duration of stays than the other two points, where most devices left the areas within 1 hour. This might be due to the kinds of activities people engage in the different points, which I will not analyze in this exercise but can be further analyzed by, for example, correlating with types of POIs. 

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/duration.png)

I also calculated the spatial length of movements by devices within the selected areas. The result below shows general consistency with the duration (i.e., the longer the device stays, the longer the distance travelled by the device is). 

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/distance.png)

I further visualized the movements of devices in each selected area on a map. The map of Perdona area below shows that people tend to walk on the trail in the park.

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/movement_perdona.png)

In the map of Petronas below, you can see generally higher number of movements and concentration of movements around the Petronas towers. 

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/movement_petronas.png)

The map of Chinatown shows a high concentration of movements along the major roads, rather than the main street in Chinatown. 

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/movement_chinatown.png)

# 4.	Spatio-temporal distribution of devices
For this section, I focused more on the changes of devices’ locations over time. The first analysis is on the cumulative total number of devices by hour. The plot below tells the following points:
1.	Chinatown peaks around 6 and has another smaller peak towards midnight. This might be due to its morning and night market.
2.	Perdona has a similar pattern as Chinatown but has lower numbers of devices in general.
3.	Petronas generally has higher numbers of devices. Its peak stays high from 6am to 11am. A little spike around 18 might be due to those who eat dinner around Petronas. Just like Chinatown, the number of devices increases towards the midnight.

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/cumulative_devices.png)

I also mapped the locations of devices aggregated by hour for each of the selected areas. For Perdona, see some devices are there in the morning. But generally, there are not many of them.
 
![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/device_perdona_hour.png)

For Petronas, you can see that there are higher numbers of devices around Petronas from 6 to 11. The drastic decrease of devices at 12 is quite interesting.
 
![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/device_petronas_hour.png)

Chinatown also shows the similar pattern as Petronas: higher numbers of devices in the morning and sudden decrease at 12.

![image](https://github.com/koito19960406/GPS_analysis/blob/main/output/device_chinatown_hour.png)

To check if these observations are influenced by the trend of devices in Kuala Lumpur as a whole, I also visualized locations of devices by hour. In the map below, you can see more devices in the morning compared to the afternoon.

![](https://github.com/koito19960406/GPS_analysis/blob/main/output/device_hour.png =100x20)

# 5.	Conclusion
The analysis so far highlighted the following characteristics of the selected areas:
1.	Concentration of devices in the morning: throughout the areas, I was able to observe higher numbers of devices in the morning and lower in the afternoon. 
2.	Concentration of devices in urbanized areas: compared to the Perdona Botanic Garden, Petronas twin towers’ area and Chinatown had higher number of devices.
3.	Concentration of devices along the major roads: This was observed especially in Chinatown. Less devices were recorded in the main market street. 
From these observations and the overall changes of locations of devices in Kuala Lumpur, I hypothesize the following:
1.	More people are Kuala Lumpur in the morning, which influences the fluctuation of number of devices in the selected areas, that 
2.	People tend to prefer urbanized attractions rather than natural ones in Kuala Lumpur
3.	People tend to prefer vehicles as a mode of transport over walking in Kuala Lumpur. 
