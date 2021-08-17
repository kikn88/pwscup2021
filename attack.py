# Created by Satoshi Hasegawa

import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce
import sys

# レコードリンケージによるメンバーシップ攻撃


class RecordLinkageAttack():

    # dfAは擬似データ, dfBはサンプリングされたデータ(もしくはそれから加工されたデータ)
    def __init__(self, dfA: pd.DataFrame, dfB: pd.DataFrame):
        self.dfA = dfA
        self.dfB = dfB
        categories = list(np.where(self.dfA.dtypes == "object")[0])
        self.enc = ce.OneHotEncoder(cols=categories, drop_invariant=False)
        self.enc.fit(pd.concat([self.dfA, self.dfB], ignore_index=True))

    def execute(self, k=1):
        encDfA = self.enc.transform(self.dfA).astype("float64").values
        encDfB = self.enc.transform(self.dfB).astype("float64").values

        # KDTreeを構築. 後のステップでクエリ探索をおこなう.
        tree = KDTree(encDfA)
        # 指定したk近傍値を取得する. 近傍の行番号がk個分付与される
        dist, index = tree.query(encDfB, k=k, return_distance=True)
        return dist, index

    def execute_(self, last=100):
        dist, index = self.execute()
        atk = np.hstack([dist, index])
        atk_sort = atk[np.argsort(atk[:, 0])]
        result = atk_sort[0:last, 1].astype("int32")
        return result


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 6:
        print("Usage : python [{}] [syntheticfilename] [anonymizefilename] [outputfilename] [header(True or False)] [skipinitialspace(True or False)]".format(
            args[0]))
        exit(1)

    filename = args[1]
    anonymfilename = args[2]  
    indexfilename = args[3]
    header = 0 if args[4] == "True" else None
    skipinitialspace = True if args[5] == "True" else False

    df = pd.read_csv(filename, header=header,
                     skipinitialspace=skipinitialspace)
    anondf = pd.read_csv(anonymfilename, header=header,
                         skipinitialspace=skipinitialspace)

    ra = RecordLinkageAttack(df, anondf)
    np.savetxt(indexfilename, ra.execute_(), fmt="%d", delimiter="\n")
