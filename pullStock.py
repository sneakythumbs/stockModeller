import urllib.request
import http.cookiejar
import time

epoch = int(time.time())
threemonths = 15368000

def pullData(stock, crumb, cooky):
    fileLine = stock + '.txt'
    urltovisit = 'https://query1.finance.yahoo.com/v7/finance/download/'+stock+'?period1='+str(epoch-threemonths)+'&period2='+str(epoch)+'&interval=1d&events=history&crumb='+crumb

    req = urllib.request.Request(urltovisit)
    cooky.add_cookie_header(req)

    with urllib.request.urlopen(req) as f:
        sourceCode = f.read().decode('utf-8')

        saveFile = open(fileLine,'w')
        saveFile.write(sourceCode)

