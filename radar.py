import pandas as pd
import numpy as np

df = pd.read_csv('ETL_files/Player_Stats.csv')
print(df.columns)

df['Attack'] = df.where(df['attack_total']> 0, df['attack_point']/df['attack_total'],np.nan)


rate_indicators = ['Attack','Dig','Receive','Serve','Set']
num_indicators = ['Block']

