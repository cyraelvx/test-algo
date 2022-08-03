import pandas as pd
import yfinance
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.graph_objects as go
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from datetime import datetime


def print_list_of_lines(df,df2):
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    # plot last list
    list1 = df2['price'].unique().tolist()
    c = 0
    #print(len(list1))
    while c <= len(list1) - 1:
        # print(list_prices[c][0])
        # print(list_prices[c][1])
        # number_of_touch = list1[c][1]
        # print()

        fig.add_shape(type='line', x0=0, y0=list1[c],
                      x1=len(df),
                      y1=list1[c],
                      line=dict(color="RoyalBlue", width=1)
                      )

        c += 1
    fig.show()


def download_stock_data(ticker_name, start_date, end_date, interval):
    ticker_symbol = ticker_name
    ticker = yfinance.Ticker(ticker_symbol)

    df = ticker.history(interval=interval, start=start_date, end=end_date)
    df['Date'] = pd.to_datetime(df.index)  # turn the index into a date column
    df = df.reset_index().drop('index', axis=1)

    return df


def check_last_date_touch(now_ind,last_ind,min_distance_between_touches):
    if (now_ind - last_ind) > min_distance_between_touches:
        return False
    else:
        return True


def drop_price_with_too_much_or_too_low_touches(df,max_number_of_touches,min_number_of_touches):
    df_drop = df.copy()
    # first take all prices with high number of touches
    df_max_touch_for_price = pd.DataFrame(df.groupby('price')['current_number_of_touches'].max()).reset_index()
    df_high_low_number_touches_for_price = df_max_touch_for_price[(df_max_touch_for_price['current_number_of_touches'] > max_number_of_touches) |
                                          (df_max_touch_for_price['current_number_of_touches'] < min_number_of_touches)]
    list_high_low_number_touches_for_price = df_high_low_number_touches_for_price['price'].tolist()
    df_to_keep = df_drop[~df_drop['price'].isin(list_high_low_number_touches_for_price)]
    return df_to_keep


def insert_levels(df, min_distance_between_touches,step_between_prices=1):
    """
    'This function inserts the levels into a dataFrame'
    :param df: the dataFrame to take the levels from
    :param step_between_prices: default is one
    :return: returns level dataFrame
    """

    min_price = int(df['Low'].min())
    max_price = int(df['High'].max())
    dict_prices_touches = {}
    list_df = []

    for price in range(min_price, max_price):  # iterate over all prices from min to max
        dict_prices_touches[price] = []
        last_ind_touch = 0
        for ind, row in df.iterrows():         # for each level of price iterate over all candles and count touches
            time_from_last_ind = check_last_date_touch(ind,last_ind_touch,min_distance_between_touches)
            if time_from_last_ind: # if time from last touch is less then minimum parameter min_distance_between_touches
                # skip the counting
                continue
            # print(ind, row)
            # if a price is between candle low and high values then we count as touch
            if row['Low'] <= price <= row['High']:
                date = str(row['Date'])
                current_num_of_touches = len(dict_prices_touches[price])
                if current_num_of_touches >= 2:
                    # print(price, current_num_of_touches, dict_prices_touches[price], date)
                    list_df.append([price, current_num_of_touches, dict_prices_touches[price], date])
                last_ind_touch = ind
                dict_prices_touches[price].append(date)
                # print(price, current_num_of_touches, dict_prices_touches[price])
    df = pd.DataFrame(list_df, columns=['price', 'current_number_of_touches', 'history', 'prediction'])
    return df


# def create_table(df, min_touches_to_define, space_between_touches):
#     if


df_tsla = download_stock_data(ticker_name='TSLA', start_date='2021-02-14', end_date='2021-06-14', interval='1h')
df = insert_levels(df_tsla,min_distance_between_touches=4)
df_levels = drop_price_with_too_much_or_too_low_touches(df,max_number_of_touches=5,min_number_of_touches=4)

# plot
print_list_of_lines(df_tsla,df_levels)