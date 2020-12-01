import pandas as pd

def get_metrics():
    #读取财务数据，选取6月份的市场回报数据和每年1.1的财务数据
    df0=pd.read_excel('../data/result.xlsx')
    df14_6=pd.read_excel('../data/市场回报数据/2014-06.xlsx')
    df15_6=pd.read_excel('../data/市场回报数据/2015-06.xlsx')
    df16_6=pd.read_excel('../data/市场回报数据/2016-06.xlsx')
    df17_6=pd.read_excel('../data/市场回报数据/2017-06.xlsx')
    #print(df.iloc[0,2])

    #把日期修改为“年”
    for i in range(df14_6.shape[0]):
        #print(finance.iloc[i,1])
        df14_6.loc[i,0]=int(df14_6.iloc[i,0])
        df14_6.loc[i,'Trdmnt']='2014'

    for i in range(df15_6.shape[0]):
        #print(finance.iloc[i,1])
        df15_6.loc[i,0]=int(df15_6.iloc[i,0])
        df15_6.loc[i,'Trdmnt']='2015'

    for i in range(df16_6.shape[0]):
        #print(finance.iloc[i,1])
        df16_6.loc[i,0]=int(df16_6.iloc[i,0])
        df16_6.loc[i,'Trdmnt']='2016'

    for i in range(df17_6.shape[0]):
        #print(finance.iloc[i,1])
        df17_6.loc[i,0]=int(df17_6.iloc[i,0])
        df17_6.loc[i,'Trdmnt']='2017'

    #print(df14_6)
    df0.rename(columns={'Accper':'Trdmnt'},inplace=True) # 重命名列名
    # print(df0)
    #获取每一年末的财务数据，并将日期修改为年
    # finance=df0[df0.Trdmnt.str.contains('01-01')]

    # finance['Trdmnt'] = finance['Trdmnt'].map(lambda x: x.rstrip('-01-01'))
    finance=df0[df0.Trdmnt.str.contains('06-30')]
    #print(finance)
    finance['Trdmnt']=finance['Trdmnt'].map(lambda x:x[0:4])

    #finance['Trdmnt']=finance['Trdmnt'].map(lambda x:'2014')
    #print(finance)

    #将市场回报数据和财务数据以Stkcd和Trdmnt进行merge
    result14 = pd.merge(finance,df14_6, on=['Stkcd', 'Trdmnt'])
    result15 = pd.merge(finance,df15_6, on=['Stkcd', 'Trdmnt'])
    result16 = pd.merge(finance,df16_6, on=['Stkcd', 'Trdmnt'])
    result17 = pd.merge(finance,df17_6, on=['Stkcd', 'Trdmnt'])

    result1 = result14.append(result15)
    result2=result1.append(result16)
    result3=result2.append(result17)
    result4=result3.sort_values(by=['Stkcd','Trdmnt'])

    #1 Size
    result4['Size']=result4['Msmvosd']

    #2 账面市值比B/M
    result4['BM']=result4['total_equity']/result4['Msmvosd']

    #3 营运利润率OP
    result4['OP']=result4['operating_profit']/result4['total_equity']

    #4 投资风格
    result4['INV']=(result4['total_assets']-result4['total_assets'].shift())/result4['total_assets'].shift()

    #将2014年的INV修改为0，因为他没有办法和前一年对比，默认为0
    for i in range(result4.shape[0]):
        if str(result4.iloc[i,1])=='2014':
            result4.iloc[i,15]=0

    df = result4[['Stkcd','Size','BM','OP','INV','Trdmnt']]

    #按Stkcd进行分组用来检验是否有完整的四年数据，没有则将该股票数据剔除
    df_=df.groupby(["Stkcd"]).count().reset_index()
    df_['Count']=df_['Size']
    df_1=df_[['Stkcd','Count']]

    #print(df_1)

    result_ = pd.merge(df_1,df, on=['Stkcd'])
    print(result_)

    #把计数为0，1，2，3的数据去除
    final = result_[-result_.Count.isin([0,1,2,3])]
    final=final[['Stkcd','Size','BM','OP','INV','Trdmnt']]
    print(final)

    #print(df1)
    #final.to_excel('final1.xlsx',index = False)

    #数据切分，生成每一年的数据
    year_list=final['Trdmnt'].unique()
    for year in year_list:
        tmp=final[final['Trdmnt']==year]
        tmp.drop(['Trdmnt'], axis=1, inplace=True)
        Mretwd_df = pd.read_excel('../data/stock/'+year+'-06.xlsx')
        tmp = pd.merge(tmp, Mretwd_df, on='Stkcd')
        tmp.drop('Msmvosd', axis=1, inplace=True)
        tmp.to_excel('../data/metrics_6/'+year+'.xlsx',index=False)


if __name__ == '__main__':
    get_metrics()
