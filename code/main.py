from group import *

if __name__ == '__main__':
    df = pd.read_excel('test.xlsx')

    factor = Factors(df)
    factor.get_groups()
    factor.get_factors()
    print(factor.df)