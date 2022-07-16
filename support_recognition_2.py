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

start_date = '2021-02-14'
end_date = '2022-06-14'

df = ticker.history(interval='1h', start=start_date, end=end_date)

df['Date'] = pd.to_datetime(df.index)

#Check if NA values are in data
# df=df[df['volume']!=0]
df.reset_index(drop=True, inplace=True)
# df.isna().sum()
# df.tail()

min_price = df.Low.min()
max_price = df.High.max()
touches_min = 5
touches_max = 6
list_prices = []
list_prices_type_touches = []
list_prices_to_print = []
list_all_touches = []
dict_all_touches = {}
for price in range(int(min_price), int(max_price)):
    dict_all_touches[price] = []
    price_counter = 0
    ind_counter = 0
    touch_inside_counter = 0
    touch_outside_counter = 0
    for ind, row in df.iterrows():
        if ind_counter == 0:
            first_ind = ind + 1

        if (price >= row['Low']) & (price <= row['High']):
            # make sore not to count if candle is close to the last count place
            list_last_t = dict_all_touches[price]
            if len(list_last_t) >=1:
                last_time_count = list_last_t[-1]
                if ind - last_time_count <=5: # if the count two close days , skip second day
                    continue
            # if not keep on counting
            ind_counter = 1
            price_counter = price_counter + 1
            list_all_touches.append((price, price_counter, ind))
            dict_all_touches[price].append(ind)
            # print(f'day and hour is: {row["Date"]}\n')
            # print(f'price is: {price}\n')
            # print(f'number of touch: {price_counter}\n')
            #
            # print(f'day Low is : {row["Low"]}\n')
            # print(f'day High is : {row["High"]}\n')
            # print(f'day Open is : {row["Open"]}\n')
            # print(f'day Close is : {row["Close"]}\n')
            if row["Open"] < row["Close"]: # positive day
                if (price >= row['Open']) & (price <= row['Close']):
                    touch_inside_counter = touch_inside_counter + 1
                    # print('touch_inside_counter')
                else:
                    touch_outside_counter = touch_outside_counter +1
                    # print('touch_outside_counter')
            if row["Close"] < row["Open"]:  # negative day
                if (price >= row['Close']) & (price <= row['Open']):
                    touch_inside_counter = touch_inside_counter + 1
                    # print('touch_inside_counter')
                else:
                    touch_outside_counter = touch_outside_counter +1
                    # print('touch_outside_counter')

        if ind > (first_ind + 300):
            break

    list_prices.append((price, price_counter, ind))
    if (price_counter >= touches_min) & (price_counter <= touches_max):
        list_prices_type_touches.append((price, price_counter, touch_outside_counter, touch_inside_counter))
        if touch_outside_counter > touch_inside_counter:
            list_prices_to_print.append((price, price_counter, ind))


s = 0
e = len(df)
dfpl = df[s:e]
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])


def print_list_of_lines(list1):
    # plot last list
    c = 0
    while c <= len(list1) - 1:
        # print(list_prices[c][0])
        # print(list_prices[c][1])
        # number_of_touch = list1[c][1]
        # print()

        fig.add_shape(type='line', x0=0, y0=list1[c][0],
                      x1=e,
                      y1=list1[c][0],
                      line=dict(color="RoyalBlue", width=1)
                      )
        c += 1


print_list_of_lines(list1=list_prices_to_print)
fig.show()

# c = 0
# while c <= len(list_prices) - 1:
#     # print(list_prices[c][0])
#     # print(list_prices[c][1])
#     number_of_touch = list_prices[c][1]
#     print()
#     if (number_of_touch >= touches_min) & (number_of_touch <= touches_max):
#         fig.add_shape(type='line', x0=list_prices[c][2], y0=list_prices[c][0],
#                       x1=list_prices[c][2] + 0.2,
#                       y1=list_prices[c][0],
#                       line=dict(color="magenta", width=3)
#                       )
#     c += 1

#     if (c > len(list_all_touches) - 1):
#         break
#     number_of_touch = list_all_touches[c][2]
#     if (number_of_touch >= 6) & (number_of_touch <= 9):
#         fig.add_shape(type='line', x0=list_all_touches[c][0], y0=list_all_touches[c][1],
#                       x1=list_all_touches[c][0],
#                       y1=list_all_touches[c][1]+1,
#                       line=dict(color="purple", width=2)
#                       )
#
#     c+=1

