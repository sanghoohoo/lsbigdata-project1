import pandas as pd
import numpy as np
import seaborn as sns

raw_welfare = pd.read_spss('data/Koweps_hpwc14_2019_beta2.sav')
welfare=raw_welfare.copy()
welfare.shape
welfare.info()
welfare.describe()

welfare = welfare.rename(
    columns = {'h14_g3' : 'sex',
               'h14_g4' : 'birth',
               'h14_g10' : 'marriage_type',
               'h14_g11' : 'religion',
               'p1402_8aq1' : 'income',
               'h14_eco9' : 'code_job',
               'h14_reg7' : 'code_religion',}
)

welfare = welfare[['sex','birth', 'marriage_type', 'religion',
                   'income', 'code_job', 'code_religion']]
                   
welfare.shape
