# PWSCup 2021 (NHANES diabets)

PWS Cup 2021は糖尿病罹患リスクを予測するための健康診断データの匿名化とメンバーシップとレコードリンクなどのリスクを評価するコンテスト．匿名化と再識別のためのサンプルコードを提供する．

情報処理学会 PWS Cup 2021 WG

[TOC]

### Requirement

- Python 3.6 
- Numpy
- pandas 1.1.5
- statsmodels v0.12.2

## Data

- [paper: Physical Activity Levels and Diabetes Prevalence in US Adults: Findings from NHANES 2015–2016](https://link.springer.com/content/pdf/10.1007/s13300-020-00817-x.pdf)
- [NHANES 2015-2016](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2015)


## Programs

### Dataset Generation

- `activ_diabet9_csv.py`: 

  ```
  python activ_diabet9_csv.py B.csv
  ```

  HNANESのXPTファイルをダウンロードして，SEQNで束ねて必要な列のみを抽出し，平均活動量METsなどを算出して， B.csv を出力する．

  | gen  | age  | race  | edu        | mar      | bmi  | dep  | pir  | gh   | mets | qm   | dia  |
  | ---- | ---- | ----- | ---------- | -------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  | Male | 62   | White | Graduate   | Married  | 27.8 | 0    | 0    | 7    | 920  | Q2   | 1    |
  | Male | 53   | White | HighSchool | Divorced | 30.8 | 0    | 1    | 5.5  | 0    | Q1   | 0    |
  | Male | 78   | White | HighSchool | Married  | 28.8 | 0    | 0    | 5.8  | 3840 | Q3   | 1    |

  

### Statistics Analysis 

- `ccount.py`　Cross Count クロス集計

  ```
  python ccount.py 入力.csv [集計.csv]
  ```

  0-10列目の値を11列目(diabetes)について集計．
  連続値については，$19 \le age \le 80$, $15 \le bmi \le 70$​ になるようにコーディングしてから集計．
  鬱病，貧困についても，0.5を基準として，0, 1 に置換して集計．
  出力の第1列(cnt)はカウント（行数），第2列は比率（全行における割合）を与える．

- `cor.py` covariance 共分散行列

  ```
  cor.py		入力.csv [共分散行列.csv]
  ```

  0-10列目の値を11列目(diabetes)について集計．
  離散値はOne Hot符号化をして，値の数のダミー変数に変換．（例，0列目は，`0_Male`, `0_Female`の2列で，Maleは(1,0), Femaleは(0,1)にする）

  B.csv の場合，30 x 30の共分散行列を返す．

- `odds6.py`　Odds Ratio オッズ比の比較

  ```
  odds6.py B.csv D.csv
  ```

  元データB.csvと匿名化データD.csv のそれぞれを，糖尿病(dia)を目的変数としてロジスティック回帰を行い，因子に対するオッズ比(OR)とP値(pvalue)を算出する． BとDのオッズ比の差を算出して，平均誤差と最大誤差を出力．

- `diabets_or.py`　糖尿病の罹患リスクOR

  ```
  diabets_or.py 入力.csv [OR.csv]
  ```

  gen + age + race + edu + mar + bmi + dep + pir + qmを説明変数として糖尿病 diaを目的変数としたロジスティック回帰．係数 Coef，オッズ比 OR, p値pvalue を出力．

- `activ_diabet_count.py`:クロス集計表算出．diabetes.csv を読む．

- `activ_diabet_sklearn.py`: ロジスティック回帰1. diabetes.csv を読み，sklearnライブラリでOR出力．

- `activ_diabet_stats.py`: ロジスティック回帰2. diabetes.csv を読み，statsmodelsライブラリでORとp値を算出．
### Anonymizing
- `top2.py`  Top coding 

  ```
  top2.py 入力.csv 列リスト　しきい値リスト [行番号.csv]
  例) top2.py B.csv 1_5 75_50 e-top.csv
  ```

  列col でしきい値 theta より大きい行を出力する．例は，1列(age)が75歳以上，または，5列(bmi)が 50以上 の行を出力する．

- `bottom2.py` Botom coding 

  ```
  bottom2.py 入力.csv 列リスト しきい値リスト[行番号.csv]
  例) bottom2.py B.csv 1_5 22_20 e-bot.csv
  ```

  列col でしきい値 theta より小さい行を出力する．例は，1列(age)が22歳以下，5列(bmi)が20以下の行を出力する．

- `kanony2.py` K-anonimity 

  ```
  kanony2.py 入力.csv k  列リスト [行番号.csv]
  例)  kanony2.py B.csv 7 2_3_4  e-ka.csv
  ```

  列columnsを準識別子とみなしてk-匿名化する．削除する行をex.csvへ出力．例は，2列(人種), 3列(学歴)，4列(既婚歴)を準識別子とみなして，k = 7でk-匿名性を満たさない行の番号を e-ka.csv に出力．

- join.py 

  ```
  join.py 行番号ファイルリスト > 統合行番号.csv
  ```

  行番号ファイルリスト（任意個）で指定した複数の行番号を束ねて（重複を取り除き）出力する（だけ）．`sort e1.csv e2.csv e3.csv | uniq > e-x.csv`と等価．

- exclude.py 

  ```
  exclude.py 入力.csv 排除行番号.csv [残レコード.csv] [残行番号.csv]
  例) exclude.py B.csv e-x.csv c-in.csv e-in.csv
  ```

  入力`B.csv`から排除行番号`e-x.csv` を除いて残ったレコードを`C-in.csv` へ出力する．

- `rr.py` Randomized Response 

  ```
  rr.py C.csv p D.csv 列リスト
  例) rr.py $Csv/c-in.csv  0.9 d-xrr.csv  0_2_3_4_6_7_10
  ```

  入力 C.csv の中の指定された列を維持確率pでランダマイズレスポンス（1-pの確率で値域の中から一様な確率で置換える．例は，0,2,3,4,6,7,10列を全て0.9の確率でランダマイズして，`d-xrr.csv` に出力している．

- `dp2.py` Differential Privacy

  ```
  dp2.py 入力.csv 列リスト εリスト [加工ファイル.csv]
  例) dp2.py d-xrr.csv 1_5 1.0_2.0 d-xrrdp.csv
  ```

  差分プライバシーに基づいて行colsにεのラプラスノイズ   
  $$
  \frac{\epsilon}{2} e^{-\epsilon |x|}
  $$
  を加える．例は，1列(age)にはε = 1.0, 5列(bmi)にはε = 2.0 のノイズを加えている．sensitivity = 1 とみなしているので，εで調整する．

- quantify2.py 	後でやる

### Recode Linking

- Pick.py テストレコードのサンプリング

  ```
  pick.py B.csv Ex.csv C.csv Ea.csv
  例）pick.py B.csv e-x.csv c-100.csv e-a.csv
  ```

  Bの`E-x.csv` (排除行）から50行，Ex以外の保留行から50行をランダムサンプリングして，100行のテストデータ`C.csv`と正解の行番号`e-a.csv`を出力する．

  |  B   |  Ex  |  C   |  Ea  |  D   |
  | :--: | :--: | :--: | :--: | :--: |
  |  0   |      |      |      |  0   |
  |  1   |      |      |      |  1   |
  |  2   |  2   |  ○   |  -1  |      |
  |  3   |      |  ●   |  2   |  2   |
  |  4   |      |  ●   |  3   |  3   |
  |  5   |  5   |      |      |      |
  |  6   |  6   |      |      |      |
  |  7   |      |      |      |  4   |
  |  8   |  8   |  ○   |  -1  |      |
  |  9   |      |      |      |  5   |

  Bの10行からExの2行とEx以外の2行を出力した例．Eaは正解行．

- attack.py レコードリンケージによるメンバーシップ攻撃．ユークリッド距離によるKDTreeを構築して探索している (PWS Cup 2020参照)

- rlink.py 

  ```
  rlink.py  C.csv D.csv E.csv
  例)rlink.py c-100.csv d-xrrdp.csv e-100xrrdp.csv
  ```

  テストデータCの各行が匿名化データDに属さないときは-1（非メンバーシップ），属するときは何行目かを上位k(=3)位まで予測して，Eに出力する．各列のメジアンよりも距離がある行を，-1と推測する（丁度50行を-1と推測する）．レコード間距離は，One Hot Encodingしてユークリッド距離を用いる．列8 (gh), 9 (mets)は用いない．
  sklearnのKDTree関数を用いたattack.py を呼んでいる．
  
  | 1st  | 2nd  | 3rd  |
  | :--: | :--: | :--: |
  |  29  | 847  | 2599 |
  |  -1  |  -1  |  -1  |
  |  -1  |  -1  |  -1  |
  |  -1  |  -1  |  -1  |
  | 134  | 1820 | 2580 |
  | 138  | 967  | 2636 |
  |  -1  |  -1  |  -1  |
  
  Cの2,3,4,7行目はDに属さない(Bから削除された）行と推測．1行目は，第1候補がCの29行目であることを推測．第2，第3候補がそれぞれ，847, 2599行目であることを表す．



### 有用性評価 Utility Metirics 
- `umark.py`		**U**tlity bench**mark** 

  ```
  umark B.csv D.csv
  ```

  有用性評価．BとDの，クロス集計(cnt, rate), オッズ比(Coef,OR,pvalue), 共分散cor の最大値と平均値を出力．

  |      | cnt   | rate  | Coef  | OR    | pvalue | cor   |
  | ---- | ----- | ----- | ----- | ----- | ------ | ----- |
  | max  | 69    | 0.020 | 0.309 | 0.061 | 0.159  | 0.006 |
  | mean | 2.530 | 0.001 | 0.031 | 0.017 | 0.028  | 8E-05 |

- Iloss.py Information Loss

  iloss.py C.csv D.csv
  
	有用性評価．CとDの，行を対応させたL1距離の最大値を評価する．(Max列のMax行の値)
  

  
	
  
  
	|      | 1    | 5    | cat  | Max  |
  | ---- | ---- | ---- | ---- | ---- |
  |mean |1.085297| 0.723084| 0.443483| 1.085297|
	|max  |8.000000| 4.400000| 4.000000| 8.000000|




### 安全性評価 Privacy Metrics 
- `lmark.py`　**L**inkage bench**mark** 

  ```
  lmark     Ea.csv  E.csv [out.csv]
  例) lmark.py e-a.csv e-100xrrdp.csv
  ```

  正解行番号Ea.csv と推定行番号E.csv を検査して，次の安全性 recall, precision, top-k を評価する．
  $$
  recall = \frac{|E_a \cap E|}{|E_a|}, \, prec = \frac{|E_a \cap E|}{|E|}, top_k = \frac{|\{x \in E_a| x \in E[x]\}|}{k}
  $$
  ここで，E_a とEは`Ea.csv` と`E.csv` の中の正の行番号(＝排除されていない行）からなる集合とする．$E[x]$​ は行xに対応する推測行番号の上位k位までの集合．

### 安全性評価 Unique Rate 

- `uniqrt.py`　**Uniq**ue Rate 

  ```
  uniqrt.py  B.csv C.csv
  例) uniqrt.py CSV/B.csv Csv/c-in.csv
  ```

  第一匿名化（特異な行の削除）されたデータC.csvの中の，一意な行の割合を評価する．ただし，連続値(age, bmi)については，10の位で丸めた値を用いて評価する．
  $$
  \begin{eqnarray}
  unique_1(C) &=& \frac{|\{c_i \in C| \forall c_j \in C-\{c_i\}, c_i \ne c_j\}|}{|C|} \\
  unique_2(C) &=& \frac{|\{c_i \in C| \forall c_j \in C-\{c_i\}, c_i \ne c_j\}|}{|B|} \\
  \end{eqnarray}
  $$
  
  
  

### フォーマットチェッカー

- `checkDX.py`　
  加工フェーズの提出物(匿名化データD, 排除行データX)の形式チェック

  ```
  checkDX.py B.csv D.csv X.csv
  例）python3 checkDX.py Csv/d-xrrdp.csv Csv/e-x.csv 
  D: num OK
  D: obj OK
  0 OK
  2 OK
  3 OK
  4 OK
  10 OK
  (2724, 12) OK
  X: int OK
  X: unique OK
  (695, 1) OK
  ```

  Dに関しては，

  1. 数値列(1,5,6,7,11)が整数または実数であるか
  2. 名義列(0,2,3,4,10)がオブジェクトであるか
  3. 列1(年齢)，列5(BMI)が，値域[13, 85], [13, 75]にあるか，列6(鬱病)，列7(貧困), 列11(糖尿病)が{0,1}の値か．
  4. 列0 (性別)，列2(人種)，列3(学歴)，列4(既婚歴)，列10(活動量)がB.csv の値域の中にあるかどうか
  5. Dの行数が$|B|/2 = 1709$行以上あり，12 列あるか．
  
  をそれぞれ検査します．Xに関しては，
  
  1. 整数型であるか
  2. 重複する行を指定していないか
  3. $|X|_{行数}+|D|_{行数} = |B|_{行数}$​ になっているか
  
  を検査しています．全てに OK が出れば合格です
  
- `checkE.py`

  攻撃フェーズの提出物(推定行番号データE)の形式チェック

  ```
  checkE.py B.csv E.csv
  例） python3 checkE.py Csv/B.csv Csv/e-xrrdp.csv
  (100, 1) Invalid
  E: int OK
  E: max OK
  E: min OK
  ```

  推定行番号が，

  1. 100行，3列のデータか
  2. 全ての列が整数型(int)か
  3. 全ての列について，$-1 \le 推定行 \le n$​​　の範囲内か

  を検査します．全てにOKが出れば合格です．



### 実行スクリプト

`bash スクリプト名`で実行する．（OSによってshが使えない時は，スクリプト内のpytest の部分だけを順に実行）

1. `test-0config.sh` 自分のチーム番号Team, 攻撃先チーム番号You，pythonのパス，生成ファイル格納ディレクトリCsvなどを設定する．

2. `test-1setup.sh` ヘルスケアデータをCDCからダウンロードする．最初に一度だけ実行する．全ファイルを落とすのに数秒かかる．

3. `test-2anonymize.sh` （匿名化フェーズ）加工から有用性評価を実行する．Category_encodersのwarningが出ることもある．rr, dp はランダム要素があり，毎回結果が違う．

     ```
     $ bash test-2anonymize.sh
     top2.py Csv/B.csv 1_5 75_50 Csv/e-top.csv
     bottom2.py Csv/B.csv 1_5 22_20 Csv/e-bot.csv
     kanony2.py Csv/B.csv 7 2_3_4 Csv/e-ka.csv
     exclude.py Csv/B.csv Csv/pre_anony_00_x.csv Csv2/C.csv Csv2/e-in2.csv
     umark.py Csv/B.csv Csv/C.csv
                  cnt      rate      Coef        OR    pvalue       cor
     max   519.000000  0.061190  0.749521  0.288657  0.383715  0.135895
     mean  114.106061  0.007815  0.101983  0.072791  0.086014  0.012597
     uniqrt.py Csv/C.csv
     2360 0.7038473009245452 0.5632458233890215
     rr.py Csv/C.csv 0.9 Csv/d-xrr2.csv 0_2_3_4_6_7_10
     dp2.py Csv/d-xrr2.csv 1_5 1.0_2.0 Csv2/pre_anony_00_d.csv
     umark.py Csv/B.csv Csv/pre_anony_00_d.csv
                  cnt      rate      Coef        OR    pvalue       cor
     max   596.000000  0.065067  0.385540  0.218689  0.455050  0.182816
     mean  114.606061  0.010027  0.102278  0.082985  0.129358  0.015871
     ```

4. `test-3pick.sh`　評価データをBからテストデータCTをサンプリングする．事務局が行なう処理．

5. `test-4rlink.sh` （攻撃フェーズ）メンバーシップ推定とレコードリンクを試み，推定結果を出力する．

   ```
   $ bash test-4rlink.sh 
   rlink.py Csv/pre_anony_00_c.csv Csv/pre_anony_00_d.csv Csv/pre_attack_00_from_00.csv
   lmark.py Csv/pre_anony_00_ea.csv Csv/pre_attack_00_from_00.csv
   lmark.py Ea.csv E.csv out.csv
   recall    0.84
   prec      0.84
   topk      0.74
   dtype: float64
   ```

6. Test-5check.sh 提出ファイル(D, X, E)のフォーマット検査を行なう．全てにOK が出れば良い．

### FAQ

[PWS Cup 2021 FAQ](FAQ.md)



Aug. 17, 2021 update







