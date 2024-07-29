house_train = pd.read_csv("data/houseprice/train.csv")
df = house_train.sort_values('SalePrice').head(10)

house_train = house_train[["Id", "BldgType", "Neighborhood", "RoofStyle", "SalePrice"]]

# 연도별 평균 
house_mean = house_train.groupby(["BldgType", "Neighborhood", "RoofStyle"], as_index = False) \
                        .agg(mean = ('SalePrice', 'mean'))
house_test = pd.read_csv("data/houseprice/test.csv")
house_test = house_test[["Id", "BldgType", "Neighborhood", "RoofStyle"]]

house_test = pd.merge(house_test, house_mean, how ='left',
                      on = ["BldgType", "Neighborhood", "RoofStyle"])
house_test = house_test.rename(columns = {'mean' : 'SalePrice'})

house_test.isna().sum()  # na 값 세기 
house_test.loc[house_test['SalePrice'].isna()] # na값 보기 

 # na 값 채우기 
price_mean = house_train["SalePrice"].mean()
house_test['SalePrice'] = house_test['SalePrice'].fillna(price_mean) 

#SalePrice 바꿔치기 및 저장 
sub_df['SalePrice'] = house_test['SalePrice']
sub_df.to_csv("data/houseprice/sample_submission3.csv", index = False)
