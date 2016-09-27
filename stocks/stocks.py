import pandas as pd
import pandas.io.data as web
import datetime

start = datetime.datetime(2016,1,1)
end = datetime.datetime.today()

apple = web.DataReader("AAPL", "yahoo", start, end)

type(apple)

print apple.head()

import matplotlib.pyplot as plt
from matplotlib.dates import date2num as d2n
import pylab

pylab.rcParams['figure.figsize'] = (15, 9)

apple["Adj Close"].plot(grid = True)