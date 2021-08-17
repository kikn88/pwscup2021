# wrote by Hiroaki Kikuchi, 2021
#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys

def lmark(Ea, dfE):
	supp = Ea > -1
	rcall = ((dfE[0] > -1) & supp).sum()/ supp.sum()
	prec = ((dfE[0] > -1) & supp).sum()/ (dfE[0] > -1).sum()
	topk = dfE[supp].isin(Ea[supp]).any(axis=1)
	return rcall, prec, topk.sum()/supp.sum()
	
#	pd.DataFrame([{'recall': rcall, 'prec': prec, 'topk': topk.sum()/supp.sum()}])

if __name__== "__main__":
	args = sys.argv
	if len(args) <= 3:
		print(args[0], 'Ea.csv E.csv out.csv')
	# 安全性評価
	
	dfEa = pd.read_csv(args[1], header=None)
	dfE = pd.read_csv(args[2], header=None)

	'''
	supp = dfEa[0] > -1
	rcall = ((dfE[0] > -1) & supp).sum()/ supp.sum()
	prec = ((dfE[0] > -1) & supp).sum()/ (dfE[0] > -1).sum()
	topk = dfE[supp].isin(dfEa[supp]).any(axis=1)
	df = pd.DataFrame([{'recall': rcall, 'prec': prec, 'topk': topk.sum()/supp.sum()}])
	'''
	rcall, prec, topk = lmark(dfEa[0], dfE)
	df = pd.Series({'recall': rcall, 'prec': prec, 'topk': topk})
	if len(sys.argv) == 4: df.to_csv(args[3])
	else: print(df)
	