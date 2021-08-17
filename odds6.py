# wrote by Ma Ruiqiang and Hiroaki Kikuchi, 2021
#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import statsmodels.api as sm            # LR
import statsmodels.formula.api as smf
import sys

def odds(df):
	df.columns = ['gen', 'age', 'race', 'edu', 'mar', 'bmi', 'dep', 'pir', 'gh', 'mets', 'qm', 'dia']
	model = smf.glm(formula='dia ~ gen + age + race + edu + mar + bmi + dep + pir + qm', data=df, family= sm.families.Binomial() )
	res = model.fit() 
	# Odds Ratio, Confidence Intervals and Pvalues
	df2 = pd.DataFrame(res.params, columns=['Coef'])
	df2['OR'] = np.exp(res.params)
	df2['pvalue'] = res.pvalues
	return(df2)

def mae(dfB, dfD):
	dfBOR = odds(dfB)['OR']
	dfDOR = odds(dfD)['OR']
	return ((dfBOR - dfDOR).abs().max(), (dfBOR - dfDOR).abs().mean())
	
if __name__== "__main__":
	args = sys.argv
	if len(args) != 2:
		print(args[0], ' diabets.csv d-rr8.csv [or.csv]')
		
	dfB = pd.read_csv(args[1], header=None)
	dfD = pd.read_csv(args[2], header=None)
	#dfBOR = odds(dfB)['Odds_Ratio']
	#dfDOR = odds(dfD)['Odds_Ratio']
	print(mae(dfB, dfD))
		
