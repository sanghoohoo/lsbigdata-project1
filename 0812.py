import pandas as pd
import numpy as np
import plotly.express as px
from palmerpenguins import load_penguins

penguins = load_penguins()
penguins.head()

fig = px.scatter(
    penguins,
    x="bill_length_mm",
    y="bill_depth_mm",
    color="species",
    # trendline = 'ols',
)


fig.update_layout(
    title={'text':"<span style='color:blue;font-weight:bold'>팔머펭귄</span>",
    'x':0.5}
)

fig.show()