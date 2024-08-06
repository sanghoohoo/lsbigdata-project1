import numpy as np
import pandas as pd
df = pd.read_csv("data/houseprice/houseprice-with-lonlat.csv")

df['Exterior_1st'].describe()
import json
geo = json.load(open('data/houseprice/us-states.json', encoding='UTF-8'))

import folium
m = folium.Map(location = [42.054035,-93.619754], zoom_start = 5)
m.save('house_maps/map1.html')
