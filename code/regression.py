import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error # MSE均方误差
from sklearn.metrics import mean_absolute_error # MAEX
from sklearn.metrics import r2_score # R^2决定系数
from sklearn import preprocessing

import matplotlib.pyplot as plt

def regression(df):
    # print(df)

    # 用14、15、16年数据回归，用17年数据验证
    train_df = pd.DataFrame()
    df_14 = df[df.Trdmnt.str.contains('2014')]
    df_15 = df[df.Trdmnt.str.contains('2015')]
    df_16 = df[df.Trdmnt.str.contains('2016')]
    df_17 = df[df.Trdmnt.str.contains('2017')]
    train_df = pd.concat([train_df, df_14, df_15, df_16])
    test_df = df_17
    
    X_train = train_df.iloc[:, 2:-1].values.astype(float)
    Y_train = (train_df['Mretwd']-train_df['Nrrmtdt']).values.reshape(-1, 1).astype(float)
    X_test = test_df.iloc[:, 2:-1].values.astype(float)
    Y_test = (test_df['Mretwd']-test_df['Nrrmtdt']).values.reshape(-1, 1).astype(float)
    # print(X_train)
    # print(Y_train)

    # 数据min-max归一化
    minMaxScaler = preprocessing.MinMaxScaler()
 
    scaler = preprocessing.MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    Y_train = scaler.fit_transform(Y_train)
    X_test = scaler.fit_transform(X_test)
    Y_test = scaler.fit_transform(Y_test)
    # print(X_train)
    # print(Y_train)
    
    # 用线性回归模型进行训练
    lr_model = LinearRegression()
    lr_model.fit(X_train, Y_train)

    # 预测测试集合的结果
    Y_pred_train = lr_model.predict(X_train)
    Y_pred = lr_model.predict(X_test)
    # Y_pred = scaler.inverse_transform(Y_pred)
    print(Y_test)
    print(Y_pred)

    # # 回归评价，模型越好：r2→1；模型越差：r2→0
    print('train_R^2: ', r2_score(Y_train, Y_pred_train))
    print('R^2: ', r2_score(Y_test, Y_pred))
    print('MSE: ', mean_absolute_error(Y_test, Y_pred))
    print('MAEX: ', mean_squared_error(Y_test, Y_pred))

    plot(Y_test, Y_pred)

def plot(Y_test, Y_pred):
    # 画图
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(Y_test, color='red', label='Y_test')
    ax.plot(Y_pred, color='blue', label='Y_pred')
    plt.title('Y_test and Y_pred')
    plt.legend(loc=0,ncol=1)
    # plt.savefig('result.png')
    plt.show()

if __name__ == '__main__':
    df = pd.read_excel('../data/data_for_regression.xlsx')
    regression(df)