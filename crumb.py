import urllib.request

import http.cookiejar

def findCrumb():
#Create a CookieJar object to hold the cookies
    cj = http.cookiejar.CookieJar()

#Create an opener to open pages using the http protocol and to process cookies.
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

#create a request object to be used to get the page.
    #req = opener.open("https://finance.yahoo.com/quote/AIR.NZ/history?p=AIR.NZ")
    req = opener.open("https://finance.yahoo.com/quote/AIR.NZ/history")

    bread = str(req.read())
    crumbtrail = bread.find('\"CrumbStore\":')
    crumb = bread[crumbtrail+23:crumbtrail+34]

    return [crumb, cj]
