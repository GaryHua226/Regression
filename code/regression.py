import pandas as pd
import numpy
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
#MSE均方误差
from sklearn.metrics import mean_squared_error
#MAEX
from sklearn.metrics import mean_absolute_error
#R^2决定系数
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt

def regression():
    # 导入数据集合
    df = pd.read_excel('../data/data_for_regression.xlsx')
    print(df)
    X = df.iloc[:, 2:8].values  # 前4列
    Y = df.iloc[:, -1].values.reshape(-1, 1)

    Y = Y - X[:, -1].reshape(-1, 1)
    X = X[:, :-1]

    # print(X)
    # print(Y)

    # # 切分训练集和测试集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    #
    # 用线性回归模型进行训练
    lr_model = LinearRegression()
    lr_model.fit(X_train, Y_train)

    # 预测测试集合的结果
    Y_pred = lr_model.predict(X_test)
    # print(Y_pred)

    # # 回归评价，模型越好：r2→1；模型越差：r2→0
    print(r2_score(Y_test, Y_pred))
    print(mean_absolute_error(Y_test, Y_pred))
    print(mean_squared_error(Y_test, Y_pred))

if __name__ == '__main__':
    regression()