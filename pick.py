# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import sys

seed = 100

def pick(df, x):
    dfC = df.drop(x)
    dfC[12] = range(dfC.shape[0])   # 行番号振り直し
    df1 = df.loc[x,:].sample(n = 50, random_state = seed)	# 負例から50
    df2 = dfC.sample(n = 50, random_state = seed)	# 正例から50
    df3 = pd.concat([df1,df2.iloc[:,0:12]])   
    df3[12] = df2[12]   # Cの相対行番号
    df3.loc[df1.index,12] = -1
    df3[12] = df3[12].astype(int)
    return df3.iloc[:,0:12], df3.iloc[:,12]     # DataFrame と Series を返すのに注意．
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(sys.argv[0], 'B.csv Ex.csv C.csv Ea.csv')
        sys.exit(0)
       # BからEx(排除行）から50行，~Ex(保留行)から50行ランダムサンプリング
       # 出力： サンプリングされた100行 C.csv，答えの行番号 Ea.csv
     
    df = pd.read_csv(sys.argv[1], header=None)
    ex = pd.read_csv(sys.argv[2], header=None, index_col=0)
    dfc, ea = pick(df, ex.index)
    
    dfc.sort_index().to_csv(sys.argv[3], header=None, index = None)
    ea.sort_index().to_csv(sys.argv[4], header=None, index = None)

'''
dfC = df.drop(ex.index)
dfC[12] = range(dfC.shape[0])   # 行番号振り直し
df1 = df.loc[ex.index,:].sample(n = 50, random_state = seed)	# 負例から50
df2 = dfC.sample(n = 50, random_state = seed)	# 正例から50
df3 = pd.concat([df1,df2.iloc[:,0:12]])

df3.sort_index().to_csv(sys.argv[3], header=None, index = None)

df3[12] = df2[12]   # Cの相対行番号
df3.loc[df1.index,12] = -1 
df3[12] = df3[12].astype(int)
# df3.loc[df1.index,12] = -1 * df1.index # 負の行番号
df3[12].sort_index().to_csv(sys.argv[4], header=None, index = None)
'''
