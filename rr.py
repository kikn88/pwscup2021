# Copyright 2020 Hiroaki Kikuchi 
import pandas as pd
import sys
import random
import numpy as np


def rr(x, q):
#     uniq = np.unique(x.values)
    uniq = x.value_counts().index.values
    y = [i if random.random() < q else random.choice(uniq) for i in x]
    return(y)


def rrdf(df, q, target):
    df2 = df.copy()
    for i in target:
        df2.iloc[:, i] = rr(df.iloc[:, i], q)
    return df2


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage : python [{}] [samplingfilename] [prob] [outputfilename] [target_columns]".format(
            sys.argv[0]))
        print("Example : python {} aaa.csv 0.9 bbb.csv 0_1_2_3_4_5_6_7_8".format(
            sys.argv[0]))
        exit(-1)

    df = pd.read_csv(sys.argv[1], header=None)
    q = float(sys.argv[2])
    target = list(set([int(i) for i in sys.argv[4].split("_")]))
    df2 = rrdf(df, q, target)
    df2.to_csv(sys.argv[3], header=False, index=False)
