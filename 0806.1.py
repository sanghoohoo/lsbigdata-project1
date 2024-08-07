import json
geo = json.load(open('data/SIG.geojson', encoding='UTF-8'))
geo['features'][0]['properties']
geo['features'][0]['geometry']

import pandas as pd
df_pop = pd.read_csv('data/Population_SIG.csv')
df_pop.head()
df_pop.info()
df_pop['code'] = df_pop['code'].astype(str)

import folium
m = folium.Map(location = [35.95, 127.7], zoom_start = 8)
m.save('maps/map1.html')

map_sig = folium.Map(location = [35.95, 127.7], zoom_start = 8, tiles = 'cartodbpositron')
map_sig.save('maps/map2.html')

folium.Choropleth(
    geo_data =geo,
    data = df_pop,
    columns = ('code','pop'),
    key_on = 'feature.properties.SIG_CD')\
    .add_to(map_sig)
map_sig
map_sig.save('maps/map3.html')

bins = list(df_pop['pop'].quantile([0,0.2,0.4,0.6,0.8,1]))
bins

map_sig = folium.Map(location = [35.95,127.7],
                     zoom_start = 8,
                     tiles = 'cartodbpositron')
    
folium.Choropleth(
    geo_data=geo,
    data=df_pop,
    columns=('code', 'pop'),
    key_on='feature.properties.SIG_CD',
    fill_color='YlGnBu',
    fill_opacity=1,
    line_opacity=0.5,
    bins=bins
).add_to(map_sig)
    
map_sig.save('maps/map4.html')
