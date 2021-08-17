# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 4:
        print(sys.argv[0], ' diabetes10.csv col theta [ex.csv]')
        #sys.exit(0)
        # bottom coding - 列col でしきい値 theta より小さい行を出力する．列は 1_5 の様にベクトルで与えても良い．

    df = pd.read_csv(sys.argv[1], header=None)
    cols = sys.argv[2].split('_')
    thetas = sys.argv[3].split('_')
    out = sys.argv[4] if len(sys.argv) == 5 else sys.stdout
    ex = df[0] == None
    for i in range(len(cols)):
        x = df.loc[:, int(cols[i])]
        ex |= x < int(thetas[i])
    ex = ex[ex].index.to_series()
    ex.to_csv(out, index = None, header = None) 
