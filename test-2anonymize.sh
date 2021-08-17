#!/bin/bash

source test-0config.sh

# 第1匿名化: top, bottom, k-匿名を適用．列の削除のみ．
pytest top2.py $B 1_5 75_50 $Csv/e-top.csv
pytest bottom2.py $B 1_5 22_20 $Csv/e-bot.csv
pytest kanony2.py $B 7 2_3_4  $Csv/e-ka.csv

# 3つの行番号を束ねる．
$python join.py $Csv/e-top.csv $Csv/e-bot.csv $Csv/e-ka.csv > $X
pytest exclude.py $B $X $C $Csv/e-in2.csv

# 有用性評価, 一意率評価
pytest umark.py $B $C
pytest uniqrt.py  $C

# 第2匿名化: rr, dp, quantify 行の削除はなし．
pytest rr.py $C  0.9 $Csv/d-xrr2.csv  0_2_3_4_6_7_10
pytest dp2.py $Csv/d-xrr2.csv 1_5 1.0_2.0 $D
pytest umark.py $B $D

