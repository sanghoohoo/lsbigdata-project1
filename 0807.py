import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

geo_seoul = json.load(open('data/SIG_Seoul.geojson', encoding='UTF-8'))
geo_seoul

type(geo_seoul)
len(geo_seoul)
geo_seoul.keys()
geo_seoul['features'][0]['properties']
coordinate_list = geo_seoul['features'][0]['geometry']['coordinates']
len(coordinate_list[0])
len(coordinate_list[0][0])
coordinate_array = np.array(coordinate_list[0][0])
x = coordinate_array[:,0]
y = coordinate_array[:,1]
plt.plot(x,y)
plt.show()
plt.clf()


def draw_seoul(num):
    gu_name = geo_seoul['features'][num]['properties']['SIG_KOR_NM']
    coordinate_list = geo_seoul['features'][num]['geometry']['coordinates']
    coordinate_array = np.array(coordinate_list[0][0])
    x = coordinate_array[:,0]
    y = coordinate_array[:,1]
    plt.rcParams.update({'font.family': 'Malgun Gothic'})
    plt.plot(x,y)
    plt.title(gu_name)
    plt.show()
    plt.clf()
    return None

draw_seoul(5)



# 서울시 전체 지도 그리기
#plt.plot(x, y, hue = 'gu_name')

#
for i in range(25):
coordinate_list_all = geo_seoul['features'][i]['geometry']['coordinates']
coordinate_array = np.array(coordinate_list_all[0][0])
gu_name = geo_seoul['features'][i]['properties']['SIG_KOR_NM']

pd.DataFrame({'gu_name' : gu_name,
              'x' : coordinate_array[:,0],
              'y' : coordinate_array[:,1]})


df = pd.DataFrame(columns=['SIG_KOR_NM', 'x', 'y'])
for i in range(25):
  df.loc[i] = [geo_seoul["features"][i]["properties"]["SIG_KOR_NM"], 
                geo_seoul["features"][i]["geometry"]["coordinates"][0][0][0][0],
                geo_seoul["features"][i]["geometry"]["coordinates"][0][0][0][1]]
                
#
data = []
# geo_seoul의 모든 구에 대해 반복
for i in range(len(geo_seoul['features'])):
    # 좌표 및 구 이름 추출
    coordinate_list_all = geo_seoul['features'][i]['geometry']['coordinates']
    coordinate_array = np.array(coordinate_list_all[0][0])
    gu_name = geo_seoul['features'][i]['properties']['SIG_KOR_NM']
    
    # 좌표와 구 이름을 데이터 리스트에 추가
    for coord in coordinate_array:
        data.append({'gu_name': gu_name, 'x': coord[0], 'y': coord[1]})
        
df = pd.DataFrame(data)
df

sns.lineplot(data=df, x=x, y=y)
plt.show()
plt.clf()


#
x=[]
y=[]
gu=[]
for i in range(len(geo_seoul['features'])):
    # 좌표 및 구 이름 추출
    coordinate_list_all = geo_seoul['features'][i]['geometry']['coordinates']
    coordinate_array = np.array(coordinate_list_all[0][0])
    gu_name = geo_seoul['features'][i]['properties']['SIG_KOR_NM']
    
    # 좌표와 구 이름을 데이터 리스트에 추가
    for coord in coordinate_array:
        gu.append(gu_name)
        x.append(coord[0])
        y.append(coord[1])
x
y
gu

df2=pd.DataFrame({'gu' : gu, 'x' : x, 'y' : y})
df2


#
def make_seouldf(num):
    gu_name=geo_seoul["features"][num]["properties"]["SIG_KOR_NM"]
    coordinate_list=geo_seoul["features"][num]["geometry"]["coordinates"]
    coordinate_array=np.array(coordinate_list[0][0])
    x=coordinate_array[:,0]
    y=coordinate_array[:,1]

    return pd.DataFrame({"gu_name":gu_name, "x": x, "y": y})

make_seouldf(1)

result=pd.DataFrame({})
for i in range(25):
    result=pd.concat([result, make_seouldf(i)], ignore_index=True)    
result=result.assign(isgangnam = np.where(result['gu_name']=='강남구', '강남', '안강남'))

sns.scatterplot(data=result, x='x', y='y', hue='gu_name', s=2, legend=False,
                palette='inferno')

sns.scatterplot(data=result, x='x', y='y', hue='isgangnam', s=2, legend=False,
                palette={'강남': 'red', '안강남': 'gray'})

plt.show()
plt.clf()



## textbook 11-1
geo_seoul['features'][0]['properties']
df_pop = pd.read_csv('data/Population_SIG.csv')
df_seoulpop = df_pop.iloc[1:26]
df_seoulpop['code']=df_seoulpop['code'].astype(str)

import folium
map_sig=folium.Map(location = [37.55180997129064, 126.97315486480478],
                             zoom_start = 12, tiles='cartodbpositron')
map_sig.save('maps/mymap1.html')

folium.Choropleth(
    geo_data = geo_seoul,
    data = df_seoulpop,
    columns = ('code','pop'),
    key_on = 'feature.properties.SIG_CD')\
    .add_to(map_sig)
map_sig.save('maps/mymap2.html')

bins = list(df_seoulpop['pop'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))

map_sig = folium.Map(location = [37.55180997129064, 126.97315486480478],
                     zoom_start = 12,
                     tiles='cartodbpositron')
folium.Choropleth(
    geo_data = geo_seoul,
    data = df_seoulpop,
    columns = ('code','pop'),
    key_on = 'feature.properties.SIG_CD',
    fill_color = 'viridis',
    bins = bins)\
    .add_to(map_sig)
map_sig.save('maps/mymap3.html')

# 점찍는법
make_seouldf(0).iloc[:,1:3].mean()
folium.CircleMarker([37.583744,126.983800], popup = '종로구').add_to(map_sig)
map_sig.save('maps/mymap4.html')
