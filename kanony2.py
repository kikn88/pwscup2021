# Copyright 2020 Hiroaki Kikuchi 
import pandas as pd
import sys


def kanony(df, qi=[1, 2], k=1):
    return df.groupby(qi).filter(lambda x: x[0].count() >= k)
    
def kanony2(df, qi=[1, 2], k=1):
    return df.groupby(qi).filter(lambda x: x[0].count() < k).index

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage : ', sys.argv[0], 'input.csv  k  columns [ex.csv]')
        sys.exit(0)
        # 列columnsを準識別子とみなしてk-匿名化する．削除する行をex.csvへ出力
        
    df = pd.read_csv(sys.argv[1], header=None)
    k = int(sys.argv[2])
    qi = list(set([int(i) for i in sys.argv[3].split("_")]))
    out = sys.argv[4] if len(sys.argv) == 5 else sys.stdout

    df2 = kanony2(df, qi=qi, k=k).to_series()
    df2.to_csv(out, header=False, index=False)
