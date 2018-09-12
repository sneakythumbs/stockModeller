import os
import matplotlib
matplotlib.use('svg')
import dataFit
import crumb
import pullStock
import buildPage

#pwd = '/home/fingers/finance'
pwd = os.getcwd()
filename = 'ticker_list'
path = '/var/www/html'

[crum, cook] = crumb.findCrumb()

buildPage.removeOldPlots(path)

with open(pwd + '/' + filename, 'r') as f:  
    page = f.readlines()

for line in page:
    if (line[0] == '#'):
        continue
    ticker = line.rstrip()
    try:
        pullStock.pullData(ticker, crum, cook, pwd)
        print('Pulled', ticker )
        print('...')
    except:
        print('Error pulling', ticker, 'skipping')
        print('...')
        continue
    [Date,Open,High,Low,Close,Adj_Close,Volume] = dataFit.loadData(ticker, pwd)
    [line, sine] = dataFit.fitData(Date, Low, dataFit.line, dataFit.sine)
    dataFit.plotData(ticker, Date, Low, line, sine, path)
    print('Plotted', ticker)
    print('...')

buildPage.writeWebPage(path)
print('Written Webpage')
print('...')
