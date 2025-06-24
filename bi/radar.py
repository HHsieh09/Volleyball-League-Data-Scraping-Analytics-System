import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_radar():
    df = pd.read_csv('ETL_files/Player_Stats.csv')
    print(df.columns)

    df['Attack'] = np.where(df['attack_total'] > 0, df['attack_point']/df['attack_total'], 0)
    df['Dig'] = np.where(df['dig_total'] > 0, df['dig_nice']/df['dig_total'], 0)
    df['Serve'] = np.where(df['serve_total'] > 0, df['serve_point'] / df['serve_total'], 0)
    df['Set'] = np.where(df['set_total'] > 0, df['set_nice'] / df['set_total'], 0)
    df['Receive'] = np.where(df['receive_total'] > 0, df['receive_nice'] / df['receive_total'], 0)
    df['Block'] = df['block_point']

    df = df[df['attack_total']+df['dig_total']+df['serve_total']+df['set_total']+df['receive_total']+df['block_point'] > 0]

    df['cup'] = df['match_cup_id'].str.split('_').str[1]

    indicators = ['Attack','Dig','Serve','Set','Receive','Block']

    df_avg = df.groupby(['cup','name'], as_index=False)[indicators].mean()

    df_avg[indicators] = df_avg[indicators] * 100

    scaler = MinMaxScaler(feature_range=(0,100))

    df_scaled = df_avg.copy()
    for col in indicators:
        scaler = MinMaxScaler(feature_range=(0, 100))
        df_scaled[col] = scaler.fit_transform(df_scaled[[col]])
        print(f"{col}: min={df_scaled[col].min():.2f}, max={df_scaled[col].max():.2f}")

    print(df_scaled)

    df_final = df_scaled.melt(id_vars=['cup','name'],
                            value_vars=indicators,
                            var_name='indicators',
                            value_name='score')

    print(df_final)

    df_final.to_csv('ETL_files/Radar_Data.csv', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    preprocess_radar()