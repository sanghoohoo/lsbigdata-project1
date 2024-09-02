# 원하는 변수를 사용해서 회귀모델을 만들고, 제출할것!
# 원하는 변수 2개
# 회귀모델을 통한 집값 예측

# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

## 필요한 데이터 불러오기
house_train=pd.read_csv("./data/houseprice/train.csv")
house_test=pd.read_csv("./data/houseprice/test.csv")
sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")

house_train.shape
house_test.shape

df=pd.concat([house_train, house_test],ignore_index=True)
df

df = pd.get_dummies(
    df,
    columns=["Neighborhood"],
    drop_first=True
    )


train_df = df.iloc[:1460,]
train_df

test_df = df.iloc[1460:,]
test_df

# validation 셋 (모의고사 셋) 만들기
np.random.seed(42)
val_index=np.random.choice(np.arange(1460), size=438, replace=False)

valid_df=train_df.loc[val_index] # 30%
train_df=train_df.drop(val_index) # 70%

train_df=train_df.query("GrLivArea <= 4500")

selected_columns= train_df\
    .filter(regex = '^GrLivArea$|^GarageArea$|^Neighborhood_').columns
train_x = train_df[selected_columns]
train_y = train_df["SalePrice"]

valid_x = valid_df[selected_columns]
valid_y = valid_df["SalePrice"]

model = LinearRegression()

model.fit(train_x, train_y)

y_hat=model.predict(valid_x)

np.sqrt(np.mean((valid_y - y_hat)**2))
