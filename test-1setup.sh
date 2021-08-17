#!/bin/bash

source test-0config.sh

test -d $Csv || mkdir $Csv

# ヘルスケアデータのダウンロード．CDCから落とすので数秒かかる．
pytest activ_diabet9_csv.py $B


