# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import numpy as np
import sys

def lap(x, eps):
    return (x + np.random.default_rng().laplace(0, 1/eps, x.shape[0])).astype(int) 
    # intへのキャストは不要かも．sensitivity = 1とする．

def lapdf(dfin, cols, epss):
    df = dfin.copy()
    for i in range(len(cols)):
        df.iloc[:,cols[i]] = lap(df.iloc[:,cols[i]], epss[i])
    return df    

if __name__ == "__main__":
    if len(sys.argv) <= 4:
        print(sys.argv[0], ' input.csv  cols  epsilons  [d.csv]')
        #sys.exit(0)
        # 差分プライバシーに基づいて行colsにεのラプラスノイズを付加する．

    df = pd.read_csv(sys.argv[1], header=None)
    cols = [int(c) for c in sys.argv[2].split('_')]
    epss = [float(e) for e in sys.argv[3].split('_')]
    out = sys.argv[4] if len(sys.argv) == 5 else sys.stdout
    for i in range(len(cols)):
        df.iloc[:,cols[i]] = lap(df.iloc[:,cols[i]], epss[i])
    df.to_csv(out, index = None, header = None)
