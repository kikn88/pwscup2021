#!/bin/bash

source test-0config.sh

# 加工データ (D, X)のフォーマット検査
pytest checkDX.py $B $D $X

# 攻撃データ (E)のフォーマット検査
pytest checkE.py $B $E
