
def get_groups(df):
    '''
    df的字段为证券代码Stkcd、市值Size、账面市值比BM、营运利润率OP、投资风格INV
    '''

    # 数据类型转换为float
    df[['Size','BM','OP','INV']]= df[['Size','BM','OP','INV']].values.astype(float)
    
    # 划分大小市值公司
    df['Size_label'] = df['Size'].map(lambda x: 'B' if x >= df['Size'].median() else 'S')
   
    # 划分高、中、低账面市值比公司
    BM_border_down, BM_border_up = df['BM'].quantile([0.3, 0.7])
    df['BM_label'] = df['BM'].map(lambda x: 'H' if x >= BM_border_up else('L' if x <= BM_border_down  else 'N'))
    
    # 划分高、中、低营运利润率
    OP_border_down, OP_border_up = df['OP'].quantile([0.3, 0.7])
    df['OP_label'] = df['OP'].map(lambda x: 'R' if x >= OP_border_up else('W' if x <= OP_border_down  else 'N'))

    # 划分投资风格
    INV_border_down, INV_border_up = df['INV'].quantile([0.3, 0.7])
    df['INV_label'] = df['INV'].map(lambda x: 'A' if x >= INV_border_up else('C' if x <= INV_border_down  else 'N'))

    # 划分6个组合
    df_SL = df.query('(Size_label=="S") & (BM_label=="L")')
    df_SN_BM = df.query('(Size_label=="S") & (BM_label=="N")')
    df_SH = df.query('(Size_label=="S") & (BM_label=="H")')
    df_BL = df.query('(Size_label=="B") & (BM_label=="L")')
    df_BN_BM = df.query('(Size_label=="B") & (BM_label=="N")')
    df_BH = df.query('(Size_label=="B") & (BM_label=="H")')

    # 划分12个组合
    df_SR = df.query('(Size_label=="S") & (OP_label=="R")')
    df_SN_OP = df.query('(Size_label=="S") & (OP_label=="N")')
    df_SW = df.query('(Size_label=="S") & (OP_label=="W")')
    df_BR = df.query('(Size_label=="B") & (OP_label=="R")')
    df_BN_OP = df.query('(Size_label=="B") & (OP_label=="N")')
    df_BW = df.query('(Size_label=="B") & (OP_label=="W")')

    df_SC = df.query('(Size_label=="S") & (INV_label=="C")')
    df_SN_INV = df.query('(Size_label=="S") & (INV_label=="N")')
    df_SA = df.query('(Size_label=="S") & (INV_label=="A")')
    df_BC = df.query('(Size_label=="B") & (INV_label=="C")')
    df_BN_INV = df.query('(Size_label=="B") & (INV_label=="N")')
    df_BA = df.query('(Size_label=="B") & (INV_label=="A")')

    return df_SL, df_SN_BM, df_SH, df_BL, df_BN_BM, df_BH, df_SR, df_SN_OP, df_SW,\
        df_BR, df_BN_OP, df_BW, df_SC, df_SN_INV, df_SA, df_BC,df_BN_INV, df_BA 

    

def get_factors(df_SL, df_SN_BM, df_SH, df_BL, df_BN_BM, df_BH, df_SR, df_SN_OP, df_SW,\
        df_BR, df_BN_OP, df_BW, df_SC, df_SN_INV, df_SA, df_BC,df_BN_INV, df_BA ):
    # # 计算各组收益率
    # R_SL = (df_SL['pct_chg'] * df_SL['circ_mv'] / 100).sum() / df_SL['circ_mv'].sum()
    # R_SM = (df_SM['pct_chg'] * df_SM['circ_mv'] / 100).sum() / df_SM['circ_mv'].sum()
    # R_SH = (df_SH['pct_chg'] * df_SH['circ_mv'] / 100).sum() / df_SH['circ_mv'].sum()
    # R_BL = (df_BL['pct_chg'] * df_BL['circ_mv'] / 100).sum() / df_BL['circ_mv'].sum()
    # R_BM = (df_BM['pct_chg'] * df_BM['circ_mv'] / 100).sum() / df_BM['circ_mv'].sum()
    # R_BH = (df_BH['pct_chg'] * df_BH['circ_mv'] / 100).sum() / df_BH['circ_mv'].sum()

    # 计算SMB
    SMB_BM = (R_SH + R_SN_BM +R_SL -R_BH - R_BN_BM - R_BL) / 3
    SMB_OP = (R_SR + R_SN_OP +R_SW -R_BR - R_BN_OP - R_BW) / 3
    SMB_INV = (R_SC + R_SN_INV +R_SA -R_BC - R_BN_INV - R_BA) / 3
    SMB = (SMB_BM + SMB_OP + SMB_INV) / 3

    # 计算HML
    HML = (R_SH + R_BH -R_SL - R_BL) / 2

    # 计算RMW
    RMW = (R_SR + R_BR -R_SW - R_BW) / 2

    # 计算CMA
    CMA = (R_SC + R_BC -R_SA - R_BA) / 2
    
    return SMB, HML, RMW, CMA