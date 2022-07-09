"""
support and resistance
try different approach - find the areas with list number of touches
iterate trow each of the prices and find the areas where the prices touches minimum number of times

a touch will count if the price is between the low-high of the days

"""
# Importing necessary python libraries for this project
import pandas as pd
import numpy as np
import yfinance
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

import plotly.io as pio
pio.renderers.default = "browser"

# Obtaining historical stock pricing data
ticker_symbol = 'COST'
ticker = yfinance.Ticker(ticker_symbol)

start_date = '2019-05-01'
end_date = '2022-06-14'

df = ticker.history(interval='1d', start=start_date, end=end_date)

df['Date'] = pd.to_datetime(df.index)



#Check if NA values are in data
# df=df[df['volume']!=0]
df.reset_index(drop=True, inplace=True)
# df.isna().sum()
# df.tail()

min_price = df.Low.min()
max_price = df.High.max()
list_prices = []
for price in range(int(min_price),int(max_price)):

    price_counter = 0
    ind_counter = 0
    for ind, row in df.iterrows():
        if ind_counter == 0:
            first_ind = ind + 1


        if (price >= row['Low']) & (price <= row['High']):
            ind_counter = 1
            price_counter = price_counter + 1

        if ind > (first_ind + 300):
            break
    list_prices.append((price,price_counter))

s = 0
e = 780
dfpl = df[s:e]
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])


# plot last list
c=0
while (1):
    if(c>len(list_prices)-1 ):
        break
    # print(list_prices[c][0])
    # print(list_prices[c][1])
    number_of_touch = list_prices[c][1]
    if (number_of_touch >= 6) & (number_of_touch <= 9):
        fig.add_shape(type='line', x0=0, y0=list_prices[c][0],
                      x1=e,
                      y1=list_prices[c][0],
                      line=dict(color="RoyalBlue",width=1)
                      )
    c+=1

fig.show()
