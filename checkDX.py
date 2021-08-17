# wrote by Hiroaki Kikuchi, 2021

import pandas as pd
import numpy as np
import sys
#from quantify import quantify
    
def checkvalues(df, i, vals):
    if set(df[i].values).issubset(vals):
        print(i, 'OK')
    else:
        print(i, 'Invalid')

def checkrange(df, i, vmin, vmax):
    print(i, 'OK' if df[i].min() >= vmin and df[i].max() <= vmax else 'Invalid')

if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print('Usage : ', sys.argv[0], 'B.csd D.csv X.csv')
        sys.exit(0)
        # 加工フェーズの提出物(匿名化データD, 排除行データX)の形式チェック

    dfB = pd.read_csv(sys.argv[1], header=None)
    dfD = pd.read_csv(sys.argv[2], header=None)
    dfX = pd.read_csv(sys.argv[3], header=None)
    n = dfB.shape[0]
    
    print('D: num',  'OK' if dfD.dtypes[[1,5,6,7,11]].isin([np.dtype(int), np.dtype(float)]).all() else 'invalid')
    print('D: obj', 'OK' if dfD.dtypes[[0,2,3,4,10]].isin([np.dtype(object)]).all() else 'invalid')

    checkrange(dfD, 1, 13, 85)
    checkrange(dfD, 5, 13, 75)
    checkrange(dfD, 6, 0, 1)
    checkrange(dfD, 7, 0, 1)
    checkrange(dfD, 11, 0, 1)

    checkvalues(dfD, 0, {'Female', 'Male'})
    checkvalues(dfD, 2, {'Black', 'Hispanic', 'Mexican', 'Other', 'White'})
    checkvalues(dfD, 3, {'11th', '9th', 'College', 'Graduate', 'HighSchool', 'Missing', np.nan})
    checkvalues(dfD, 4, {'Divorced', 'Married', 'Never', 'Parther', 'Separated', 'Widowed'})
    checkvalues(dfD, 10, {'Q1', 'Q2', 'Q3', 'Q4'})
    print(dfD.shape, 'OK' if dfD.shape[0] > n/2 and dfD.shape[1] == 12 else 'Invalid')
  
    print('X: int', 'OK' if dfX[0].dtypes == int else 'Invalid')
    print('X: unique', 'OK' if (dfX[0].value_counts() == 1).all() else 'Invalid')
    print(dfX.shape, 'OK' if dfX.shape[1] == 1 and dfD.shape[0] + dfX.shape[0] == n else 'Invalid')