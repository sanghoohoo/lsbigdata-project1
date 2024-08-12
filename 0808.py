import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

df_covid19_100 = pd.read_csv('data/plotly/df_covid19_100.csv')
df_covid19_100
df_covid19_100.info()

# import os
# os.getcwd()
# 주석 ctrl + /

margins_P = {'l':25, 'r':25, 't':50, 'b':25}
fig = go.Figure(
    data = [{
        'type':'scatter',
        'mode':'markers',
        'x':df_covid19_100.loc[df_covid19_100['iso_code']=='KOR','date'],
        'y':df_covid19_100.loc[df_covid19_100['iso_code']=='KOR','new_cases'],
        'marker':{'color':'red'}
    },
        {
        'type':'scatter',
        'mode':'lines',
        'x':df_covid19_100.loc[df_covid19_100['iso_code']=='KOR','date'],
        'y':df_covid19_100.loc[df_covid19_100['iso_code']=='KOR','new_cases'],
        'line':{'color':'blue','dash':'dash'},
        }],
    layout = {
            'title':'코로나19 발생 현황',
            'xaxis':{'title':'날짜','showgrid':False},
            'yaxis':{'title':'확진자수'},
            'margin':margins_P
            }
)
fig.show()


#프레임속성========
# 애니메이션 프레임 생성
frames = []
dates = df_covid19_100.loc[df_covid19_100["iso_code"] == "KOR", "date"].unique()

for date in dates:
    frame_data = {
        "data": [
            {
                "type": "scatter",
                "mode": "markers",
                "x": df_covid19_100.loc[(df_covid19_100["iso_code"] == "KOR") & (df_covid19_100["date"] <= date), "date"],
                "y": df_covid19_100.loc[(df_covid19_100["iso_code"] == "KOR") & (df_covid19_100["date"] <= date), "new_cases"],
                "marker": {"color": "red"}
            },
            {
                "type": "scatter",
                "mode": "lines",
                "x": df_covid19_100.loc[(df_covid19_100["iso_code"] == "KOR") & (df_covid19_100["date"] <= date), "date"],
                "y": df_covid19_100.loc[(df_covid19_100["iso_code"] == "KOR") & (df_covid19_100["date"] <= date), "new_cases"],
                "line": {"color": "blue", "dash": "dash"}
            }
        ],
        "name": str(date)
    }
    frames.append(frame_data)

x_range = ['2022-10-03', '2023-01-11']
y_range = [8900, 88172]


# 애니메이션을 위한 레이아웃 설정
margins_P = {"l": 25, "r": 25, "t": 50, "b": 50}
layout = {
    "title": "코로나 19 발생현황",
    "xaxis": {"title": "날짜", "showgrid": False, "range": x_range},
    "yaxis": {"title": "확진자수", "range": y_range},
    "margin": margins_P,
    "updatemenus": [{
        "type": "buttons",
        "showactive": False,
        "buttons": [{
            "label": "Play",
            "method": "animate",
            "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
        }, {
            "label": "Pause",
            "method": "animate",
            "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
        }]
    }]
}

# Figure 생성
fig = go.Figure(
    data=[
        {
            "type": "scatter",
            "mode": "markers",
            "x": df_covid19_100.loc[df_covid19_100["iso_code"] == "KOR", "date"],
            "y": df_covid19_100.loc[df_covid19_100["iso_code"] == "KOR", "new_cases"],
            "marker": {"color": "red"}
        },
        {
            "type": "scatter",
            "mode": "lines",
            "x": df_covid19_100.loc[df_covid19_100["iso_code"] == "KOR", "date"],
            "y": df_covid19_100.loc[df_covid19_100["iso_code"] == "KOR", "new_cases"],
            "line": {"color": "blue", "dash": "dash"}
        }
    ],
    layout=layout,
    frames=frames
)

fig.show()

##
import pandas as pd
import numpy as np
import plotly.express as px
from palmerpenguins import load_penguins

# 데이터 로드
penguins = load_penguins()
penguins.head()

# Scatter plot 생성
fig = px.scatter(
    penguins,
    x="bill_length_mm",
    y="bill_depth_mm",
    color="species",
    trendline = 'ols',
    size_max=10  # 점의 최대 크기 설정
)

# 레이아웃 업데이트
fig.update_layout(
    title=dict(text="팔머펭귄 종별 부리 길이 vs. 깊이", font=dict(size=24, color="white")),
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="white"),
    xaxis=dict(
        title=dict(text="부리 길이 (mm)", font=dict(size=18, color="white")), 
        tickfont=dict(size=14, color="white"),
        gridcolor='rgba(255, 255, 255, 0.2)'  # 그리드 색깔 조정
    ),
    yaxis=dict(
        title=dict(text="부리 깊이 (mm)", font=dict(size=18, color="white")), 
        tickfont=dict(size=14, color="white"),
        gridcolor='rgba(255, 255, 255, 0.2)'  # 그리드 색깔 조정
    ),
    legend_title=dict(text='펭귄 종', font=dict(size=18, color='white')),
    legend=dict(font=dict(size=14, color="white")),
)

# 점 크기 업데이트
fig.update_traces(marker=dict(size=12), opacity=0.7)


##
from sklearn.linear_model import LinearRegression

model = LinearRegression()
penguins = penguins.dropna()
x = penguins[['bill_length_mm']]
y = penguins['bill_depth_mm']

model.fit(x,y)
linear_fit = model.predict(x)

fig.add_trace(go.Scatter(
    mode = 'lines',
    x = penguins['bill_length_mm'],
    y = linear_fit,
    name = '선형회귀직선',
    line = dict(dash = 'dot')
))

fig.show()

# 범주형 변수로 회귀분석 진행하기
# 범주형 변수인 'species'를 더미 변수로 변환
penguins_dummies = pd.get_dummies(penguins, 
                                  columns=['species'],
                                  drop_first=False)
penguins_dummies.columns
penguins_dummies.iloc[:,-3:]


# x와 y 설정
x = penguins_dummies[["bill_length_mm", "species_Chinstrap", "species_Gentoo"]]
y = penguins_dummies["bill_depth_mm"]

# 모델 학습
model = LinearRegression()
model.fit(x,y)

model.coef_
model.intercept_

# y = 0.2 * bill_length -1.93 * species_Chinstrap -5.1 * species_Gentoo + 10.56
# penguins
# species    island  bill_length_mm  ...  body_mass_g     sex  year
# Adelie     Torgersen            39.5  ...       3800.0  female  2007
# Chinstrap  Torgersen            40.5  ...       3800.0  female  2007
# Gentoo     Torgersen            40.5  ...       3800.0  female  2007
# x1, x2, x3
# 39.5, 0, 0
# 40.5, 1, 0
# y = 0.2 * bill_length -1.93 * species_Chinstrap -5.1 * species_Gentoo + 10.56
0.2 * 40.5 -1.93 * True -5.1* False + 10.56

x
regline_y=model.predict(x)

import matplotlib.pyplot as plt
import seaborn as sns

sns.scatterplot(x=x['bill_length_mm'], y=regline_y)
