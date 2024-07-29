import pandas as pd
import numpy as np

train=pd.read_csv("./data/houseprice/train.csv")
house_train=train[["Id", "YearBuilt", "SalePrice"]]
house_train.info()

# 연도별 평균
house_mean=house_train.groupby("YearBuilt", as_index=False) \
                      .agg(mean_year = ("SalePrice", "mean"))
house_mean                      

test=pd.read_csv("./data/houseprice/test.csv")
house_test=test[["Id", "YearBuilt"]]
house_test

house_test=pd.merge(house_test, house_mean, 
                    how="left", on="YearBuilt")
house_test=house_test.rename(
    columns={"mean_year": "SalePrice"}
    )
house_test

house_test["SalePrice"].isna().sum()

# 비어있는 테스트 세트 집들 확인
house_test.loc[house_test["SalePrice"].isna()]

# 집값 채우기
house_mean=house_train["SalePrice"].mean()
house_test["SalePrice"]=house_test["SalePrice"].fillna(house_mean)

# sub 데이터 불러오기
sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")
sub_df

# SalePrice 바꿔치기
sub_df["SalePrice"] = house_test["SalePrice"]
sub_df

#sub_df.to_csv("./data/houseprice/sample_submission2.csv", index=False)
train['LotArea']
train['BldgType']

##
house_mean2=train.groupby(["LotArea", "BldgType"],as_index=False) \
                      .agg(mean = ("SalePrice", "mean"))
house_mean2

house_test2=test[["LotArea", "BldgType"]]

house_test2=pd.merge(house_test2, house_mean2, 
                    how="left", on=["LotArea", "BldgType"])

house_test2=house_test2.rename(
    columns={"mean": "SalePrice"}
    )
    
house_test2["SalePrice"].isna().sum()
house_test2["SalePrice"]=house_test2["SalePrice"].fillna(house_test["SalePrice"])
sub_df["SalePrice"] = house_test2["SalePrice"]
sub_df

sub_df.to_csv("./data/houseprice/sample_submission3.csv", index=False)
