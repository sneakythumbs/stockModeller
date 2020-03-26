import urllib.request
import http.cookiejar
import time

epoch = int(time.time())
threemonths = 15368000

def pullData(stock, crumb, cooky, path):
    fileLine = path + '/' + stock + '.txt'
    urltovisit = 'https://query1.finance.yahoo.com/v7/finance/download/'+stock+'?period1='+str(epoch-threemonths)+'&period2='+str(epoch)+'&interval=1d&events=history&crumb='+crumb

    sourceCode = ''
    data = ''

    req = urllib.request.Request(urltovisit)
    cooky.add_cookie_header(req)

    with urllib.request.urlopen(req) as f:
        sourceCode = f.read().decode('utf-8')

    urltovisit = 'https://finance.yahoo.com/quote/' + stock
    req = urllib.request.Request(urltovisit)
    cooky.add_cookie_header(req)

    with urllib.request.urlopen(req) as f:
#        data = f.read().decode('utf-8')
        data = f.read().decode('utf-8').replace('&amp;', '&')

    companyName = data.split('<h1 class=\"D(ib) Fz(16px) Lh(18px)\" data-reactid=\"7\">')[1].split('</h1>')[0] + '\n' 

    with open(fileLine,'w') as saveFile:
        saveFile.write(companyName)
        saveFile.write(sourceCode)
