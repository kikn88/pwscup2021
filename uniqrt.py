# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import sys
#from quantify import quantify

def uniqrt(df, qi = [0,1,2,3,4,5,6,7, 10], q = 6):  # gh と metsを排除．量子化数 q
    df2 = df.copy()
    #df2[1] = quantify(df[1], q)      # age 
    #df2[5] = quantify(df[5], q)      # bmi 
    df2[1] = df[1].round(-1)
    df2[5] = df[5].round(-1)
    u = (df2[qi].value_counts() == 1).sum()
    #return u / df.shape[0]
    return u

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage : ', sys.argv[0], 'input.csv')
        sys.exit(0)
        # 一意な値となる行数の割合
    n = 4190        # dia9 (dia6: 3419)

    df = pd.read_csv(sys.argv[1], header=None)
    u = uniqrt(df)
    print( u, u/df.shape[0], u/n)
