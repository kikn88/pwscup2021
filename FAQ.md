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

Q6. Uniqrt.py は，元データBと削除されて残ったデータCとの比較により計算するとありますが，データCは審判に提出しないのではないでしょうか？(DとXのみ提出)

審判で，BとXを元にしてCを計算して，uniqrt(B,C)を計算します．Cは提出しなくて結構です．

Q7. NHANESのどのデータをダウンロードしたらいいのでしょうか？拡張子XPTのファイルは何でしょうか？

`test-1setup` (実際には，`activ_diabet9.csv.py` )を実行すると，必要なファイルだけをダウンロードして，フォーマットを変換して，束ねたCSVファイルを生成します．XPTファイルは，SASのファイルです．

Q8. B.csv の第8列(gh)，第9列(mets)　はなぜ0なのですか？

（歴史的な事情です）第8列は，第11列(dia)を，第9列は，第10列(qm)を計算する過程で利用されていましたが，匿名化には無関係なので0でクリアされています．（興味がある方は，active_diabet9_csv.pyの該当行を外して値を観測しても結構です）

Q9. Test-0config.sh の環境変数 You は何ですか？

攻撃対象のチームの番号を入れてください．（サンプルは00のままで動作するはずです．分かりにくい変数名？すんません）

Q10. Ilossの，離散値の最大値は1ではないのか？ （ルールのp.16だと，5になっている？）

離散値の列（0,2,3,4,6,7,10,11)全てについて，不一致の列をカウントしています．離散値については最大8を取ります．（2021/8/26 予備戦）



2021/8/18
2021/8/26 　Q6,..,Q10を追加



