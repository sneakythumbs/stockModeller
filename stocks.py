import matplotlib
matplotlib.use('Agg')
import dataFit
import crumb
import pullStock
import buildPage

#path = '/home/fingers/finance'
path = '/var/www/html'

[crum, cook] = crumb.findCrumb()

with open('ticker_list', 'r') as f:  
    page = f.readlines()

for line in page:
    ticker = line.rstrip()
    pullStock.pullData(ticker, crum, cook)
    print('Pulled', ticker )
    print('...')

for line in page:
    ticker = line.rstrip()
    [Date,Open,High,Low,Close,Adj_Close,Volume] = dataFit.loadData(ticker)
    [line, sine] = dataFit.fitData(Date, Close, dataFit.line, dataFit.sine)
    dataFit.plotData(ticker, Date, Close, line, sine, path)
    print('Plotted', ticker)
    print('...')

buildPage.writeWebPage(path)
print('Written Webpage')
print('...')
