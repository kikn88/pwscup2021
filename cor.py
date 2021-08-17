# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import sys
import numpy as np
import category_encoders as ce

def get_cor(mat, names):
    with np.errstate(invalid='ignore'):
        cor = np.corrcoef(mat.T)
        # cor = cor * (np.ones(cor.shape) - np.tril(np.ones(cor.shape))) 
        # ceで符号化の順番が変動するので，対角成分を残しておく．
        cor = cor * (np.ones(cor.shape) - np.diag(np.ones(cor.shape[0])))
    return pd.DataFrame(cor, columns = names, index = names)    

def OneHot(df):
    categories = df.dtypes[df.dtypes == 'object'].index
    enc = ce.OneHotEncoder(cols=categories, drop_invariant=False, use_cat_names=True)
    enc.fit(df, ignore_index=True)
    df_value = enc.transform(df).astype("float64").values
    names = enc.get_feature_names()
    return df_value, names

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(sys.argv[0], ' input1.csv  [out.csv]')
        #sys.exit(0)
        # 共分散行列の計算．

    df = pd.read_csv(sys.argv[1], header=None)
    out = sys.argv[2] if len(sys.argv) == 3 else sys.stdout

    df = df.loc[:,[0,1,2,3,4,5,6,7,10,11]]
# #    categories = list(np.where(df.dtypes == "object")[0])
#     categories = df.dtypes[df.dtypes == 'object'].index
#     enc = ce.OneHotEncoder(cols=categories, drop_invariant=False, use_cat_names=True)
# #    enc.fit(pd.concat([dfB, dfD], ignore_index=True))
#     enc.fit(df, ignore_index=True)
#     df_value = enc.transform(df).astype("float64").values
#    names = enc.get_feature_names()
    df_value, names = OneHot(df)
    cor = get_cor(df_value, names)
    cor.to_csv(out)
    