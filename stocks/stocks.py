import requests
import json
import urllib
import pprint as pprint


def stock_info(symbol):
    '''
    purpose:
        get information about a stock from yahoo
    parameters:
        string -> name of stock
    return:
        dictionary -> information about the stock
    '''
    start = '2016-09-20'
    end = '2016-09-23'
    url = 'https://query.yahooapis.com/v1/public/yql?q='
    query = 'select * from yahoo.finance.historicaldata where symbol in ("' + symbol + '")'
    query += 'and startDate = "' + start + '" and endDate = "' + end + '"'
    encoded_query = urllib.parse.quote(query.encode('utf-8'))
    request = url+encoded_query
    request = request.replace('%2A', '*')
    request = request.replace('%28', '(')
    request = request.replace('%29', ')')
    request += '&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
    test = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22' + symbol + '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
    json_result = requests.get(request)
    try:
        dict_result = json.loads(json_result.text)
    except Exception:
        print('correct format:', request == test)
        print(json_result)
        dict_result = None
    return dict_result


def print_stock(symbol):
    '''
    purpose:
        pretty print the stock information that we use
    parameters:
        string -> name of stock
    return:
        None
    '''
    stock = stock_info(symbol)
    if stock:
        #pprint.pprint(stock)
        pprint.pprint(stock['query']['results']['quote'])
    else:
        print('stock not available')

stocks = ['AAPL', 'GOOGL', 'SPY']

for stock in stocks:
    print_stock(stock)
