#!/bin/bash

source test-0config.sh

# 攻撃
pytest rlink.py $CT  $D  $E

# 安全性評価
pytest lmark.py  $EA  $E
