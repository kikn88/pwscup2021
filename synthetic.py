# Created by Satoshi Hasegawa
import numpy as np
import pandas as pd
import category_encoders as ce
from sklearn.neighbors import KernelDensity
import sys
import secrets


class SyntheticDataGenerator():
    # df: データフレーム. 対象となるデータを指定. , logcol: logをとってから処理する属性を指定., scale: 最大値, 最小値の補正の仕方をFalseならクリッピング, Trueなら正規化する. int_kde: 整数属性の乱数初期化をkernel density estimationを使うかどうか.
    def __init__(self, df: pd.DataFrame, logcol: list = [], scale: bool = False, int_kde: bool = False):
        if df.ndim != 2:
            raise ValueError("ndim must be 2")

        categories = list(np.where(df.dtypes == "object")[0])
        self.dtypes = df.dtypes
        self.cols = df.shape[1]
        self.enc = ce.OneHotEncoder(cols=categories, drop_invariant=False)
        transdf = self.enc.fit_transform(df).astype("float64")
        self.columns = transdf.columns
        self.data = transdf.values
        self.dim = self.data.shape[1]
        self.logcol = logcol
        cate, inte, floa, alls = self.__parse__()

        for i in logcol:
            self.data[:, alls[i]] = np.log(self.data[:, alls[i]] + 1)

        self.other = set(list(np.arange(self.dim)))
        self.uniqcol = set()
        for i in range(0, self.dim):
            if np.unique(self.data[:, i]).size == 1:
                self.other.remove(i)
                self.uniqcol.add(i)
        self.other = list(self.other)
        self.uniqcol = list(self.uniqcol)
        self.other.sort()
        self.uniqcol.sort()
        self.scale = scale
        self.KDE = int_kde

    # 度数カウントを行うメソッド
    def __count(self, vector):
        s = np.sort(vector)
        u = np.unique(s)
        map = dict.fromkeys(u, 0)
        for i in s:
            map[i] = map[i] + 1
        return map

    # 乱数生成. vectorから__countで度数分布を作成し, その度数分布からランダムに乱数を発生
    def __randomchoice(self, vector, num):
        countmap = self.__count(vector)
        keys = list(countmap.keys())
        prob = list(np.array(list(countmap.values())) /
                    sum(list(countmap.values())))
        vec = np.random.choice(
            keys, size=num, replace=True, p=prob)
        countmap2 = self.__count(vec)
        if len(countmap2.keys()) != len(countmap.keys()):
            raise RuntimeError("error")
        return vec
    # 指定数以下の場合はシャッフル, それ以上の場合は__randomchoiceで乱数列を作成

    def __shufflechoice(self, vector, num):
        if len(vector) < num:
            return self.__randomchoice(vector, num)
        else:
            return np.random.permutation(vector)[0:num]

    # kernel density estimationで乱数列を作成
    def __kdechoice(self, vector, num):
        if vector.ndim != 2:
            vector = vector.reshape(-1, 1)
        kde = KernelDensity().fit(vector)
        return kde.sample(num)[:, 0]

    # 実際に擬似データを生成するメソッド, numは数値を指定
    def generator(self, num: int):
        data = self.__correctGenerator(
            num, self.__shufflechoice, self.__kdechoice if self.KDE else self.__shufflechoice, self.__kdechoice)
        df = pd.DataFrame(data, columns=self.columns)
        reversedf = self.enc.inverse_transform(df).astype(self.dtypes)
        return reversedf

    # 擬似データの生成(__generator)及び, 最大値、最小値の補正および離散値の補正を行う.
    def __correctGenerator(self, num, catchoice, intchoice, floatchoice):
        tmp = self.__generator(num, catchoice, intchoice, floatchoice)
        cat, inte, floa, alls = self.__parse__()

        # 以下は、最大値、最小値、離散値の補正を行うロジック
        for i in list(cat.values()):
            tmp[:, i] = np.identity(
                i.stop-i.start)[np.argmax(tmp[:, i], axis=1)]
        for k, i in floa.items():
            maximum = np.max(self.data[:, i])
            minimum = np.min(self.data[:, i])
            if self.scale:
                tmpmax = np.max(tmp[:, i])
                tmpmin = np.min(tmp[:, i])
                tmp[:, i] = (tmp[:, i] - tmpmin) / \
                    (tmpmax - tmpmin) * (maximum - minimum) + minimum
            else:
                tmp[:, i] = tmp[:, i].clip(minimum, maximum)
            if k in self.logcol:
                tmp[:, i] = np.exp(tmp[:, i]) - 1
        for k, i in inte.items():
            maximum = np.max(self.data[:, i])
            minimum = np.min(self.data[:, i])
            if self.scale:
                tmpmax = np.max(tmp[:, i])
                tmpmin = np.min(tmp[:, i])
                tmp[:, i] = (tmp[:, i] - tmpmin) / \
                    (tmpmax - tmpmin) * (maximum - minimum) + minimum
            else:
                tmp[:, i] = tmp[:, i].clip(minimum, maximum)
            if k in self.logcol:
                tmp[:, i] = np.exp(tmp[:, i]) - 1
            tmp[:, i] = np.round(tmp[:, i])

        return tmp

    # 擬似データ生成の本質的なアルゴリズムを実装したメソッド
    def __generator(self, num, catchoice, intchoice, floatchoice):
        # 特異となる行列要素を排除する.
        # すべて同じ値のもの
        # 相関があるもの
        self.syn = np.zeros((num, len(self.other)))
        # 各次元ごとにw乱数を生成する
        cate, inte, floa, alls = self.__parse__()

        # 乱数を発生させる
        for i in list(cate.values()):
            for j in i:
                self.syn[:, j] = catchoice(self.data[:, self.other[j]], num)

        for i in list(floa.values()):
            for j in i:
                self.syn[:, j] = floatchoice(self.data[:, self.other[j]], num)

        for i in list(inte.values()):
            for j in i:
                self.syn[:, j] = intchoice(self.data[:, self.other[j]], num)

        # 白色化処理を行う.
        mu_tmp = np.mean(self.syn, axis=0)
        sigma_tmp = np.cov(self.syn.T)
        u_tmp, s_tmp, v_tmp = np.linalg.svd(sigma_tmp)
        u_tmp = np.linalg.inv(u_tmp.dot(np.diag(np.sqrt(s_tmp))))

        for i in range(0, num):
            self.syn[i] = u_tmp.dot(self.syn[i] - mu_tmp)

        # 平均mu, 分散共分散行列sigmaで行列を変形させる.
        mu = np.mean(self.data[:, self.other], axis=0)
        sigma = np.cov(self.data[:, self.other].T)

        u, s, v = np.linalg.svd(sigma)
        u = u.dot(np.diag(np.sqrt(s)))
        for i in range(0, num):
            self.syn[i] = u.dot(self.syn[i]) + mu

        # 以下の処理で誤差を確認.
        # print(np.linalg.norm(np.mean(self.syn, axis=0) - np.mean(self.data, axis=0)))
        # print(np.sum(np.linalg.norm(np.cov(self.syn.T) - np.cov(self.data.T))))

        if len(self.uniqcol) == 0:
            return self.syn
        else:
            self.result = np.zeros((num, self.dim))
            for i in self.uniqcol:
                self.result[:, i] = np.full(num, self.data[0, i])
            for i in range(0, len(self.other)):
                self.result[:, self.other[i]] = self.syn[:, i]
            return self.result

    def __parse__(self):
        j = 0
        k = 0
        categories = {}
        floatings = {}
        integers = {}
        alls = {}
        for i in range(self.cols):
            if len(self.enc.mapping) != 0 and self.enc.mapping[j]["col"] == i:
                size = self.enc.mapping[j]["mapping"].shape[1]
                categories[i] = range(k, k + size)
                alls[i] = range(k, k + size)
                k = k + size
                if (len(self.enc.mapping) - 1) != j:
                    j = j + 1
            else:
                if self.dtypes[i] == "float64" or self.dtypes[i] == "float32":
                    floatings[i] = range(k, k + 1)
                    alls[i] = range(k, k + 1)
                elif self.dtypes[i] == "int64" or self.dtypes[i] == "int32":
                    integers[i] = range(k, k + 1)
                    alls[i] = range(k, k + 1)
                else:
                    s = "Not support " + str(self.dtypes[i])
                    raise ValueError(s)
                k = k + 1
        return categories, integers, floatings, alls


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 7:
        print("Usage : python [{}] [inputfilename] [header(True or False)] [skipinitialspace(True or False)] [num] [outputfilename] [seed]".format(
            args[0]))
        exit(1)

    filename = args[1]
    header = 0 if args[2] == "True" else None
    skipinitialspace = True if args[3] == "True" else False
    num = int(args[4])
    outputfilename = args[5]
    seed = None if args[6] == "None" else int(args[6])

    seed = secrets.randbits(32) if seed is None else seed

    np.random.seed(seed)

    logcol = []

    df = pd.read_csv(filename, header=header,
                     skipinitialspace=skipinitialspace)

    sdg = SyntheticDataGenerator(
        df=df, scale=False, logcol=logcol, int_kde=True)
    # 擬似データの生成
    ssf = sdg.generator(num)

    ssf.to_csv(outputfilename,
               header=False if header is None else True, index=False)
    print("seed:", seed)
