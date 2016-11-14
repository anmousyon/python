import requests
import json
import pprint as pp
import pandas as pd
import numpy as np
import sympy as sy
from io import StringIO
from time import time


def get_trades(start=None):
    '''
    purpose:
        get trade information from bitcoincharts api
    input:
        start :: string -> timestamp to get trades from
    output:
        response :: dataframe -> stock data
    '''
    url = 'http://api.bitcoincharts.com/v1/trades.csv?symbol=bitstampUSD'
    if start:
        url += '&start=' + start
    response = requests.get(url)
    psuedo_file = StringIO(response.text)
    data = pd.read_csv(psuedo_file, names=['unixtime', 'price', 'amount'])
    data = data.iloc[::-1]
    return data


def load_historic():
    '''
    purpose:
        load the historic data file
    output:
        historic :: dataframe -> the historic data from bitstamp
    '''
    historic = pd.read_csv('./bitstampUSD.csv', names=['unixtime', 'price', 'amount'])
    return historic


def trends(data, splits=0, section=0):
    '''
    purpose:
        find trends in stock data
    '''
    def get_avg(splits=0, section=0):
        '''
        purpose:
            get averages over the fata
        input:
            splits :: integer -> number of sections to make
            sections :: integer -> section to iterate over (0 indexed)
        output:
            start_time :: double -> average time of first half
            start_price :: double -> average price of first half
            end_time :: double -> average time of second half
            end_price :: double -> average price of second half
        '''
        if section > 2**splits:
            print('ERROR, that section is out of range')
            print('section (0 indexed)', section)
            print('possible sections', 2**splits)
            print('splits', splits)

        #find the amount of rows to iterate over
        rows = int(len(data) / (2**splits))
        start = rows * section
        mid = int((rows * section) + (rows / 2))
        end = int((rows * section) + rows)
        initial = data['price'].iloc[start:mid].mean()
        final = data['price'].iloc[mid:end].mean()
        return initial, final

    initial, final = get_avg(splits, section)
    print('start price:', initial)
    print('end price:', final)
    trend = (final - initial) / (initial)
    percent = str(float(int(trend*10000))/100) + '%'
    return trend, percent


def test_classifier(classifier, old, new):
    '''
    purpose:
        test the classifier
    input:
        classifier :: object -> predicts the market change
        old :: pandas dataframe -> old stock data
        new :: pandas dataframe -> new stock data
    output:
        result :: ??? -> accuracy of the prediction
    '''
    start = time()
    api_timeout = 16*60
    
    old_avg = old['price'].mean()
    
    #make a classifier than can predict the change
    predicted_change = 1 #classifier(old)

    #wait for the api to be ready to check again
    while time() < start + api_timeout:
        pass

    new_avg = new['price'].mean()
    actual_change = new_avg - old_avg
    #compare predicted and actual somehow
    result = 0#compare(actual_change, predicted_change)
    return result


def moving_average(days=50, data=None):
    '''
    purpose:
        calculate the moving average over a certain period
    input:
        days :: integer -> amount of time
    output:
        avg :: double -> moving average over that time period
    '''
    # get unixtimestamp start time -> amount of seconds before current time
    start = time() - (days*24*60*60)

    # get the trades occuring since that time
    #data = get_trades(str(start))

    avg = data['price'].mean()

    return avg



def main():
    '''run the program'''
    #historic = load_historic()
    #current = get_trades()
    current = pd.read_csv('current.csv')
    #current.to_csv('current.csv', index=False)
    #print(current)
    print('current')
    current_trend, current_percent = trends(current)
    #print('historic')
    #historic_trend = find_trends(historic, 5, 31)
    print('current trend:', current_trend)
    print('current percent change', current_percent)
    #print('historic trend:', historic_trend)
    #section, mv_avg = moving_average()
    #section.to_csv('mv_avg.csv', index=False)
    section = pd.read_csv('mv_avg.csv')
    mv_avg = moving_average(data=section)
    print('moving avg:', mv_avg)

main()