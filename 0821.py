from palmerpenguins import load_penguins
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import patsy

df = load_penguins()
penguins=df.dropna()

# Patsy를 사용하여 수식으로 상호작용 항 생성
# 0 + 는 절편을 제거함
# 종속변수 ~ 독립변수 + 독립변수
model=LinearRegression()
formula = 'bill_depth_mm ~ 0 + bill_length_mm * body_mass_g * flipper_length_mm * species'
y, x = patsy.dmatrices(formula, penguins, return_type='dataframe')

x=x.iloc[:,1:]

model.fit(x, y)

model.coef_
model.intercept_