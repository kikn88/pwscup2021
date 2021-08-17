# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import sys

if len(sys.argv) == 1:
    print(sys.argv[0], 'ex1.csv ex2.csv ...')
    sys.exit(0)
   # 行番号を束ね，標準出力に出力する．
   
ex = [pd.read_csv(x, header=None, index_col=0) for x in sys.argv[1:]]
sum(ex).to_csv(sys.stdout, header=None)
