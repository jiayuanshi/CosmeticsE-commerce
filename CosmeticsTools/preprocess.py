import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure

def missing_value_check(df):
    for col in df.columns:
        pct_missing = np.mean(df[col].isnull())
        print('{} - {}%'.format(col, pct_missing))
        
def drop_useless_columns(df, col_name):
    df.drop(col_name, axis=1, inplace=True)    
        
def datatype_check(df):
    print (df.dtypes)

def add_event_date(df):
    df['event_date'] = df['event_time'].str[:10]
    
def add_event_weekday(df):
    df['weekday'] =  pd.to_datetime(df['event_date']).dt.weekday
    
def drop_duplicates(df):
    df.drop_duplicates()