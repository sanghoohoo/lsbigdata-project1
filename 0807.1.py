import numpy as np
import pandas as pd
df =pd.read_csv('data/houseprice/houseprice-with-lonlat.csv')
df
df=df.iloc[:,-2:]
df['Longitude'].mean()
df['Latitude'].mean()
import folium
map_ames=folium.Map(location = [42.03448223395904, -93.64289689856655],
                             zoom_start = 12, tiles='cartodbpositron')
##
from folium.plugins import MarkerCluster
    
house_df = pd.read_csv("data/houseprice/houseprice-with-lonlat.csv")

house_df = house_df[["Longitude", "Latitude"]]

center_x=house_df["Longitude"].mean()
center_y=house_df["Latitude"].mean()


map_sig=folium.Map(location = [42.034, -93.642],
                  zoom_start = 12,
                  tiles="cartodbpositron")

marker_cluster = MarkerCluster().add_to(map_sig)

for i in range(len(house_df)):
    folium.Marker(
        location=[house_df.iloc[i,1], house_df.iloc[i,0]],
        popup="houses,,"
    ).add_to(marker_cluster)

map_sig.save('maps/mymap5.html')

