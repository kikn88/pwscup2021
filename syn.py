# Created by Satoshi Hasegawa, modified by H. Kikuchi
import pandas as pd
import numpy as np
import synthetic as st
import sys
import hashlib

import warnings
warnings.simplefilter('ignore', FutureWarning)

n = 4190

if len(sys.argv) < 4:
    print(sys.argv[0], 'B.csv B2.csv seed')
    sys.exit(0)
    # Bから基本統計量を維持したデータB2をseedによる乱数で合成する．


dfB = pd.read_csv(sys.argv[1], header=None)
seed = int(sys.argv[3])
np.random.seed(seed)

df = dfB[[0,1,2,3,4,5,6,7,10,11]]
df.columns = range(df.shape[1])

sdg = st.SyntheticDataGenerator(df=df, scale=False, logcol=[], int_kde=True)
ssf = sdg.generator(n * 2)
ssf.drop_duplicates(inplace=True)
df2 = ssf.sample(n=n, random_state=seed)
df2[[10,11]] = 0
df3 = df2[[0,1,2,3,4,5,6,7,10,11,8,9]]
df3.columns = range(df3.shape[1])
df3[1] = df3[1].round(0)
df3[5] = df3[5].round(1)

# SHA1ハッシュ値によるチェックサム
print(hashlib.sha1(df3.to_string(header=False,index=False).encode()).hexdigest())

df3.to_csv(sys.argv[2], header=False, index=False)
