# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import sys

def ccs(df):
    n = df.shape[0]
    age = pd.cut(df[1].apply(lambda x: min(max(19,x),80)), [19, 44, 64, 80])
    bmi = pd.cut(df[5].apply(lambda x: min(max(15,x),70)), [15, 18.5, 25, 30, 70])
    dep = df[6].apply(lambda x: 'dep_0' if x < 0.5 else 'dep_1')
    pir = df[7].apply(lambda x: 'pir_0' if x < 0.5 else 'pir_1')
    cc = [df.groupby([i,11])[0].count() for i in [0,age, 2,3,4, bmi, dep,pir,10]]
    ccs = pd.concat(cc)
    return pd.DataFrame({'cnt': ccs, 'rate': ccs/n})
    

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(sys.argv[0], ' input1.csv  [out.csv]')
        #sys.exit(0)
        # クロス集計．0-10列目の値を11列目(diabetes)について集計．

    df = pd.read_csv(sys.argv[1], header=None)
    out = sys.argv[2] if len(sys.argv) == 3 else sys.stdout

#     n = df.shape[0]
#     age = pd.cut(df[1], [19, 44, 64, 80])
#     bmi = pd.cut(df[5], [15, 18.5, 25, 30, 70])
#     cc = [df.groupby([i,11])[0].count() for i in [0,age, 2,3,4, bmi, 6,7,10]]
#     ccs = pd.concat(cc)
#     dfcc = pd.DataFrame({'cnt': ccs, 'rate': ccs/n})
    dfcc = ccs(df)
    dfcc.to_csv(out)
 