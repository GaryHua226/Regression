import pandas as pd
import os

def get_stockmnth():
    path = '../ff5f_data/stockmnth/'
    stockmnth_df = pd.DataFrame()
    for root, dirs, files in os.walk(path):
        for file in files:
            df = pd.read_excel(path+file)
            stockmnth_df = pd.concat([stockmnth_df, df])
            
    stockmnth_df = stockmnth_df[stockmnth_df.Markettype.isin(['1','4'])] # 筛选A股数据
    stockmnth_df = stockmnth_df[['Stkcd', 'Trdmnt', 'Msmvosd', 'Mretwd']]
    stockmnth_df[['Msmvosd','Mretwd']]= stockmnth_df[['Msmvosd','Mretwd']].values.astype(float)
    stockmnth_df[['Stkcd']]= stockmnth_df[['Stkcd']].values.astype(str)
    # print(stockmnth_df)

    stockmnth_df['Stkcd'] = stockmnth_df['Stkcd'].map(lambda x: (6-len(x))*'0' + x)

    month_list = stockmnth_df['Trdmnt'].unique()
    # print(month_list)

    for month in month_list:
        df = stockmnth_df[stockmnth_df['Trdmnt'] == month]
        df.to_excel('../data/stock/'+month+'.xlsx', index=False)
    
def get_mktmnth_and_rf():
    mktmnth_path = '../ff5f_data/mktmnth/'
    mktmnth_df = pd.DataFrame()
    for root, dirs, files in os.walk(mktmnth_path):
        for file in files:
            df = pd.read_excel(mktmnth_path+file)
            mktmnth_df = pd.concat([mktmnth_df, df])
    mktmnth_df = mktmnth_df[mktmnth_df.Markettype == 5] # 筛选A股数据
    mktmnth_df = mktmnth_df[['Trdmnt','Cmretwdos']]
    # print(mktmnth_df)

    rf_path = '../ff5f_data/rf/'
    rf_df = pd.DataFrame()
    for root, dirs, files in os.walk(rf_path):
        for file in files:
            df = pd.read_excel(rf_path+file)
            rf_df = pd.concat([rf_df, df])
    rf_df['month'] = rf_df['Clsdt'].map(lambda x:x[:-3])
    rf_df = rf_df[['month', 'Nrrmtdt']]
    rf_df = rf_df.groupby('month').mean()
    # print(rf_df)

    merge_df = pd.merge(mktmnth_df, rf_df, left_on='Trdmnt', right_on='month')
    # print(merge_df)
    merge_df.to_excel('../data/market/market.xlsx', index=False)

if __name__ == '__main__':
    # get_stockmnth()
    get_mktmnth_and_rf()