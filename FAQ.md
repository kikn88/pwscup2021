# PWS Cup 2021 FAQ

Q1. umark.py などで次のエラーが出ます．

```
FutureWarning: is_categorical is deprecated and will be removed in a future version.  Use is_categorical_dtype instead
```

pythonのライブラリ `category_encoders` によるものです．おおらかなお気持ちで，そのままご利用ください．

Q2. 次のエラーが出ます．
```
TypeError: 'values' is not ordered, please explicitly specify the categories order by passing in a categories argument.
```


加工された値にフォーマットに合わないものが入っている可能性があります．`checkDX.py` にかけて形式を確認してください．

Q3. pythonのバージョンはいくらですか？

- MacOS 11.5 (Python 3.9.5)
- centOS 7 (python 3.6.8)
- windows (python 3.6.5)
  などで動作を確認済み．

Q4. データのダウンロードの時に，次のエラーが出ます．

```
AttributeError: 'bytes' object has no attribute 'encode'
```

pandasのバージョンが古い可能性があります．

```
python3 -m pip install --upgrade pandas
```

でライブラリを更新してみてください．

 `pandas-1.1.5` を使って動作を確認しています．

Q5. Umark.py にて，次のエラーが出ます．

```
PerfectSeparationError: Perfect separation detected, results not available
```

加工されたデータが小さすぎるために，ロジスティック回帰が収束しないことが原因です．データ長を広げて試みてください．

2021/8/18

