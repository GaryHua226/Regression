import pandas as pd

class Factors:
    def __init__(self):
        self.df = pd.DataFrame()
        self.Mretwd_df = pd.DataFrame()

        # 划分6个组合
        self.df_SL = pd.DataFrame()
        self.df_SN_BM = pd.DataFrame()
        self.df_BH = pd.DataFrame()
        self.df_BL = pd.DataFrame()
        self.df_BN_BM = pd.DataFrame()
        self.df_BH = pd.DataFrame()

        # 划分12个组合
        self.df_SR = pd.DataFrame()
        self.df_SN_OP = pd.DataFrame()
        self.df_SW = pd.DataFrame()
        self.df_BR = pd.DataFrame()
        self.df_BN_OP = pd.DataFrame()
        self.df_BW = pd.DataFrame()

        self.df_SC = pd.DataFrame()
        self.df_SN_INV = pd.DataFrame()
        self.df_SA = pd.DataFrame()
        self.df_BC = pd.DataFrame()
        self.df_BN_INV = pd.DataFrame()
        self.df_BA = pd.DataFrame()

        self.SMB = 0
        self.HML = 0
        self.RMW = 0
        self.CMA = 0

    def update_df(self, df):
        self.df = df
        self.df[['Size','BM','OP','INV','Mretwd']]= df[['Size','BM','OP','INV','Mretwd']].values.astype(float)


    def update_df_Mretwd(self, year, month):
        self.df.drop(['Mretwd', 'Trdmnt'], axis=1, inplace=True)
        Mretwd_df = pd.read_excel('../data/stock/'+year+'-'+month+'.xlsx')
        Mretwd_df['Stkcd'] = Mretwd_df['Stkcd'].astype(str)
        Mretwd_df['Stkcd'] = Mretwd_df['Stkcd'].map(lambda x: (6-len(x))*'0' + x)
        self.df = pd.merge(self.df, Mretwd_df, on='Stkcd')
        self.df.drop('Msmvosd', axis=1, inplace=True)

    def get_groups(self):
        '''
        df的字段为证券代码Stkcd、市值Size、账面市值比BM、营运利润率OP、投资风格INV、考虑现金红利再投资的月个股回报率Mretwd
        '''
        
        # 划分大小市值公司
        self.df['Size_label'] = self.df['Size'].map(lambda x: 'B' if x >= self.df['Size'].median() else 'S')
    
        # 划分高、中、低账面市值比公司
        BM_border_down, BM_border_up = self.df['BM'].quantile([0.3, 0.7])
        self.df['BM_label'] = self.df['BM'].map(lambda x: 'H' if x >= BM_border_up else('L' if x <= BM_border_down  else 'N'))
        
        # 划分高、中、低营运利润率
        OP_border_down, OP_border_up = self.df['OP'].quantile([0.3, 0.7])
        self.df['OP_label'] = self.df['OP'].map(lambda x: 'R' if x >= OP_border_up else('W' if x <= OP_border_down  else 'N'))

        # 划分投资风格
        INV_border_down, INV_border_up = self.df['INV'].quantile([0.3, 0.7])
        self.df['INV_label'] = self.df['INV'].map(lambda x: 'A' if x >= INV_border_up else('C' if x <= INV_border_down  else 'N'))

        # 划分6个组合
        self.df_SL = self.df.query('(Size_label=="S") & (BM_label=="L")')
        self.df_SN_BM = self.df.query('(Size_label=="S") & (BM_label=="N")')
        self.df_SH = self.df.query('(Size_label=="S") & (BM_label=="H")')
        self.df_BL = self.df.query('(Size_label=="B") & (BM_label=="L")')
        self.df_BN_BM = self.df.query('(Size_label=="B") & (BM_label=="N")')
        self.df_BH = self.df.query('(Size_label=="B") & (BM_label=="H")')

        # 划分12个组合
        self.df_SR = self.df.query('(Size_label=="S") & (OP_label=="R")')
        self.df_SN_OP = self.df.query('(Size_label=="S") & (OP_label=="N")')
        self.df_SW = self.df.query('(Size_label=="S") & (OP_label=="W")')
        self.df_BR = self.df.query('(Size_label=="B") & (OP_label=="R")')
        self.df_BN_OP = self.df.query('(Size_label=="B") & (OP_label=="N")')
        self.df_BW = self.df.query('(Size_label=="B") & (OP_label=="W")')

        self.df_SC = self.df.query('(Size_label=="S") & (INV_label=="C")')
        self.df_SN_INV = self.df.query('(Size_label=="S") & (INV_label=="N")')
        self.df_SA = self.df.query('(Size_label=="S") & (INV_label=="A")')
        self.df_BC = self.df.query('(Size_label=="B") & (INV_label=="C")')
        self.df_BN_INV = self.df.query('(Size_label=="B") & (INV_label=="N")')
        self.df_BA = self.df.query('(Size_label=="B") & (INV_label=="A")')
    
    def get_factors(self):
        # # 计算各组流通市值加权收益率
        R_SL = (self.df_SL['Mretwd'] * (self.df_SL['Size'] / self.df_SL['Size'].sum()) ).sum()
        R_SN_BM = (self.df_SN_BM['Mretwd'] * (self.df_SN_BM['Size'] / self.df_SN_BM['Size'].sum()) ).sum()
        R_SH = (self.df_SH['Mretwd'] * (self.df_SH['Size'] / self.df_SH['Size'].sum()) ).sum()
        R_BL = (self.df_BL['Mretwd'] * (self.df_BL['Size'] / self.df_BL['Size'].sum()) ).sum()
        R_BN_BM = (self.df_BN_BM['Mretwd'] * (self.df_BN_BM['Size'] / self.df_BN_BM['Size'].sum()) ).sum()
        R_BH = (self.df_BH['Mretwd'] * (self.df_BH['Size'] / self.df_BH['Size'].sum()) ).sum()

        R_SR = (self.df_SR['Mretwd'] * (self.df_SR['Size'] / self.df_SR['Size'].sum()) ).sum()
        R_SN_OP = (self.df_SN_OP['Mretwd'] * (self.df_SN_OP['Size'] / self.df_SN_OP['Size'].sum()) ).sum()
        R_SW = (self.df_SW['Mretwd'] * (self.df_SW['Size'] / self.df_SW['Size'].sum()) ).sum()
        R_BR = (self.df_BR['Mretwd'] * (self.df_BR['Size'] / self.df_BR['Size'].sum()) ).sum()
        R_BN_OP = (self.df_BN_OP['Mretwd'] * (self.df_BN_OP['Size'] / self.df_BN_OP['Size'].sum()) ).sum()
        R_BW = (self.df_BW['Mretwd'] * (self.df_BW['Size'] / self.df_BW['Size'].sum()) ).sum()

        R_SC = (self.df_SC['Mretwd'] * (self.df_SC['Size'] / self.df_SC['Size'].sum()) ).sum()
        R_SN_INV = (self.df_SN_INV['Mretwd'] * (self.df_SN_INV['Size'] / self.df_SN_INV['Size'].sum()) ).sum()
        R_SA = (self.df_SA['Mretwd'] * (self.df_SA['Size'] / self.df_SA['Size'].sum()) ).sum()
        R_BC = (self.df_BC['Mretwd'] * (self.df_BC['Size'] / self.df_BC['Size'].sum()) ).sum()
        R_BN_INV = (self.df_BN_INV['Mretwd'] * (self.df_BN_INV['Size'] / self.df_BN_INV['Size'].sum()) ).sum()
        R_BA = (self.df_BA['Mretwd'] * (self.df_BA['Size'] / self.df_BA['Size'].sum()) ).sum()

        # 计算SMB、HML、RMW、CMA
        self.SMB_BM = (R_SH + R_SN_BM +R_SL -R_BH - R_BN_BM - R_BL) / 3
        self.SMB_OP = (R_SR + R_SN_OP +R_SW -R_BR - R_BN_OP - R_BW) / 3
        self.SMB_INV = (R_SC + R_SN_INV +R_SA -R_BC - R_BN_INV - R_BA) / 3
        self.SMB = (self.SMB_BM + self.SMB_OP + self.SMB_INV) / 3

        self.HML = (R_SH + R_BH -R_SL - R_BL) / 2

        self.RMW = (R_SR + R_BR -R_SW - R_BW) / 2

        self.CMA = (R_SC + R_BC -R_SA - R_BA) / 2

if __name__ == '__main__':
    df = pd.read_excel('test.xlsx')

    factor = Factors(df)
    factor.get_groups()
    factor.get_factors()
    print(factor.df)