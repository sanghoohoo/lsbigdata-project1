import pandas as pd
import numpy as np
gsheet_url = "https://docs.google.com/spreadsheets/d/1RC8K0nzfpR3anLXpgtb8VDjEXtZ922N5N0LcSY5KMx8/gviz/tq?tqx=out:csv&sheet=Sheet2"
names = pd.read_csv(gsheet_url)
names.head()

names=names.iloc[:,:2]
names=names.drop(columns='ID')
names

#names.sample(n=2)
np.random.choice(names['이름'],2,replace=False)
