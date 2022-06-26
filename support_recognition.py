"""
support and resistance
the purpose of this scripts find support and resistance area
1. detect "spikes" in the data:
    a. "spikes" will be defined as "spikes":
    -  if n days before there is down trend
    -  and n days after there is up trend
    b. we will change n few times in order to get more types of spikes
2. detect area of support:
    a. an area of support will be defined if a minimum of spikes touch this area.
    b. number of spikes for definition of an area is a parameter to decide the
    c. the minimum distance between the spikes is also a parameter
    d. the maximum distance between the spikes is also a parameter
    e. the maximum high between the spikes is also a parameter
"""
# Importing necessary python libraries for this project
import pandas as pd
import numpy as np
import yfinance
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

# Obtaining historical stock pricing data
ticker_symbol = 'AMD'
ticker = yfinance.Ticker(ticker_symbol)

start_date = '2021-11-01'
end_date = '2022-01-14'

df = ticker.history(interval='1d', start=start_date, end=end_date)

df['Date'] = pd.to_datetime(df.index)



#Check if NA values are in data
# df=df[df['volume']!=0]
df.reset_index(drop=True, inplace=True)
# df.isna().sum()
# df.tail()


def support(df1, candle, days_before1, days_after1): #n1 n2 before and after candle l
    for i in range(candle-days_before1+1, candle+1):
        if(df1.Low[i]>df1.Low[i-1]):
            return 0
    for i in range(candle+1,candle+days_after1+1):
        if(df1.Low[i]<df1.Low[i-1]):
            return 0
    return 1

#support(df,46,3,2)


def resistance(df1, candle, days_before1, days_after1): #days_before, days_after the candle l
    for i in range(candle-days_before1+1, candle+1):
        if(df1.High[i]<df1.High[i-1]):
            return 0
    for i in range(candle+1,candle+days_after1+1):
        if(df1.High[i]>df1.High[i-1]):
            return 0
    return 1
#resistance(df, 30, 3, 5)

dfpl = df[0:50]
import plotly.graph_objects as go
from datetime import datetime

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])

fig.show()

sr = []
days_before=3
days_after=2
for row in range(3, 205): #len(df)-n2
    if support(df, row, days_before, days_after):
        sr.append((row,df.Low[row],1))
    if resistance(df, row, days_before, days_after):
        sr.append((row,df.High[row],2))
print(sr)