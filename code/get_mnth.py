import pandas as pd
import os

if __name__ == '__main__':
    path = '../ff5f_data/stockmnth/'
    stockmnth_df = pd.DataFrame()
    for root, dirs, files in os.walk(path):
        for file in files:
            df = pd.read_excel(path+file)
            stockmnth_df = pd.concat([stockmnth_df, df])
            
    stockmnth_df = stockmnth_df[stockmnth_df.Markettype.isin(['1','4'])] # 筛选A股数据
    stockmnth_df = stockmnth_df[['Stkcd', 'Trdmnt', 'Msmvosd', 'Mretwd']]
    stockmnth_df[['Msmvosd','Mretwd']]= stockmnth_df[['Msmvosd','Mretwd']].values.astype(float)
    # stockmnth_df = stockmnth_df.groupby(df['Trdmnt'])
    print(stockmnth_df)