import csv
import numpy
import json
import pandas
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

companies = ['AAL', 'AAPL', 'DAL', 'LUV', 'UAL']
output = open('results.text', 'w')
for company in companies:
	VA = open(company + '_stock_tweet', 'r')
	VAlist = json.load(VA)
	VAcsv = open(company + '.csv', 'w')
	c = csv.writer(VAcsv)
	c.writerow(['data', 'stock0', 'stock1', 'stock2', 'stock3', 'tweet0', 'tweet1', 'tweet2', 'tweet3'])
	for i in range(3,len(VAlist)):
		row = [VAlist[i]['date'], VAlist[i]['stock'], VAlist[i - 1]['stock'], VAlist[i - 2]['stock'], VAlist[i - 3]['stock'], numpy.mean(VAlist[i]['tweets']), numpy.mean(VAlist[i - 1]['tweets']), numpy.mean(VAlist[i - 2]['tweets']), numpy.mean(VAlist[i - 3]['tweets'])]
		c.writerow(row)
	VAcsv.close()
	VA.close()
	data = pandas.read_csv(company + '.csv')
	model = ols("stock0 ~ stock1 + stock2 + stock3 + tweet0 + tweet1 + tweet2 + tweet3", data).fit()
	#print(company)
	output.write(company + '\r\n')
	output.write(str(model.summary()))
	#print(model.summary())
	output.write('\r\n')

output.close()
print("output to results")

