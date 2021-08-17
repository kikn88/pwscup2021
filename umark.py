# wrote by Hiroaki Kikuchi, 2021
#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys
from ccount import ccs
from odds6 import odds
from cor import get_cor, OneHot

def mae(x, y):
	dif = (x - y).abs()
	return dif.max(), dif.mean()
	
def umark(dfB0, dfD0):
	dfB = dfB0.copy()
	dfD = dfD0.copy()
	dfBcc = ccs(dfB)
	dfDcc = ccs(dfD)
	dfBor = odds(dfB)
	dfDor = odds(dfD)
	vB,nB = OneHot(dfB)
	vD,nD = OneHot(dfD)
	dfBcor = get_cor(vB,nB)
	dfDcor = get_cor(vD,nD)
	df1 = pd.DataFrame(mae(dfBcc,dfDcc))
	df2 = pd.DataFrame(mae(dfBor,dfDor))
	mae3 = mae(dfBcor,dfDcor)
	df3 = pd.DataFrame((mae3[0].max(), mae3[1].mean()),columns=['cor'])
	df = df1.join([df2,df3])
	df.index = ['max', 'mean']
	return df

if __name__== "__main__":
	args = sys.argv
	if len(args) <= 2:
		print(args[0], ' B.csv D.csv  [out.csv]')
	# 有用性評価．BとDの，クロス集計(cnt, rate), オッズ比(Coef,OR,pvalue), 共分散cor の最大値と平均値を出力
	
	dfB = pd.read_csv(args[1], header=None)
	dfD = pd.read_csv(args[2], header=None)
# 	dfE = pd.read_csv(args[3], header=None) if len(sys.argv) == 4 else None
	out = sys.argv[3] if len(sys.argv) == 4 else sys.stdout
	df = umark(dfB, dfD)
	'''
	dfBcc = ccs(dfB)
	dfDcc = ccs(dfD)
	dfBor = odds(dfB)
	dfDor = odds(dfD)
	vB,nB = OneHot(dfB)
	vD,nD = OneHot(dfD)
	dfBcor = get_cor(vB,nB)
	dfDcor = get_cor(vD,nD)
# 	print(mae(dfBcc, dfDcc), mae(dfBor, dfDor), mae(dfBcor, dfDcor))
	df1 = pd.DataFrame(mae(dfBcc,dfDcc))
	df2 = pd.DataFrame(mae(dfBor,dfDor))
	mae3 = mae(dfBcor,dfDcor)
	df3 = pd.DataFrame((mae3[0].max(), mae3[1].mean()),columns=['cor'])
	df = df1.join([df2,df3])
	df.index = ['max', 'mean']
	'''
	if len(sys.argv) == 4: df.to_csv(out)
	else: print(df)

