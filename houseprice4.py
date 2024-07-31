import seaborn as sns
house_train = pd.read_csv("data/houseprice/train.csv")
house_train['MSSubClass'].value_counts()
#        20	1-STORY 1946 & NEWER ALL STYLES
#        30	1-STORY 1945 & OLDER
#        40	1-STORY W/FINISHED ATTIC ALL AGES
#        45	1-1/2 STORY - UNFINISHED ALL AGES
#        50	1-1/2 STORY FINISHED ALL AGES
#        60	2-STORY 1946 & NEWER
#        70	2-STORY 1945 & OLDER
#        75	2-1/2 STORY ALL AGES
#        80	SPLIT OR MULTI-LEVEL
#        85	SPLIT FOYER
#        90	DUPLEX - ALL STYLES AND AGES
#       120	1-STORY PUD (Planned Unit Development) - 1946 & NEWER
#       150	1-1/2 STORY PUD - ALL AGES
#       160	2-STORY PUD - 1946 & NEWER
#       180	PUD - MULTILEVEL - INCL SPLIT LEV/FOYER
#       190	2 FAMILY CONVERSION - ALL STYLES AND AGES
sns.barplot(data=house_train, x='MSSubClass', y='SalePrice')
plt.show()
plt.clf()

house_train['MSZoning'].value_counts()
#       A	Agriculture
#       C	Commercial
#       FV	Floating Village Residential
#       I	Industrial
#       RH	Residential High Density
#       RL	Residential Low Density
#       RP	Residential Low Density Park 
#       RM	Residential Medium Density
sns.barplot(data=house_train, x='MSZoning', y='SalePrice')
plt.show()
plt.clf()

house_train['LotShape'].value_counts()
#       Reg	Regular	
#       IR1	Slightly irregular
#       IR2	Moderately Irregular
#       IR3	Irregular
sns.barplot(data=house_train, x='LotShape', y='SalePrice')
plt.show()
plt.clf()
