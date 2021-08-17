#!/bin/bash

source test-0config.sh

# （事務局）テストデータCをサンプリングする．答行番号 e-a.csv
pytest pick.py  $B  $X  $CT  $EA

