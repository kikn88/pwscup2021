# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import numpy as np
import sys
#from quantify import quantify

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print('Usage : ', sys.argv[0], 'B.csv E.csv')
        sys.exit(0)
        # 攻撃フェーズの提出物(推定行番号データE)の形式チェック

    dfB = pd.read_csv(sys.argv[1], header=None)
    dfE = pd.read_csv(sys.argv[2], header=None)
    n = dfB.shape[0]

    print(dfE.shape, 'OK' if dfE.shape[0] ==  100 and dfE.shape[1] == 3 else 'Invalid')
    print('E: int',  'OK' if dfE.dtypes.isin([np.dtype('int32'), np.dtype('int64')]).all() else 'invalid')

    print('E: max', 'OK' if (dfE.max() < n).all() else 'Invalid')
    print('E: min', 'OK' if (dfE.min() >= -1).all() else 'Invalid')
    