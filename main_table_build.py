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
    """
    this function check if a touch is close to the last touch
    :param now_ind: current index
    :param last_ind: last touch index
    :param min_distance_between_touches: the minimum distance between touches as depended in the interval
    :return: boolean - True or False
    """
    if (now_ind - last_ind) > min_distance_between_touches:
        return False
    else:
        return True


def get_min_max_local_to_touch(price_of_touch_t,df_t,ind_t,interval_time):
    local_df = df_t.iloc[ind_t+1:ind_t+interval_time]
    local_max = local_df['High'].max()
    high_d = np.abs(local_max - price_of_touch_t)
    local_min = local_df['Low'].min()
    low_d = np.abs(local_min - price_of_touch_t)
    if high_d > low_d:
        return local_max
    else:
        return local_min


def calculate_change_in_price(price_to_check_after,ind, df, percent_change, interval_time_to_check):
    if (ind + interval_time_to_check) >= len(df):
        return False,False,False,0

    price_of_touch = price_to_check_after
    close_price_column_index = 3

    # the most farthest value from price in the interval frame
    farthest_price_after_some_time = get_min_max_local_to_touch(price_of_touch,df,ind,interval_time_to_check)
    abs_change_in_price_after_some_time = (np.abs(price_of_touch - farthest_price_after_some_time) / price_of_touch ) * 100
    if (abs_change_in_price_after_some_time > percent_change) & (farthest_price_after_some_time > price_of_touch):
        return abs_change_in_price_after_some_time,price_of_touch,farthest_price_after_some_time, 1
    elif (abs_change_in_price_after_some_time > percent_change) & (price_of_touch > farthest_price_after_some_time):
        return abs_change_in_price_after_some_time, price_of_touch, farthest_price_after_some_time, -1
    else:
        return abs_change_in_price_after_some_time, price_of_touch, farthest_price_after_some_time, 0


def drop_price_with_too_much_or_too_low_touches(df,max_number_of_touches,min_number_of_touches):
    """
    :param df: the levels df
    :param max_number_of_touches: maximum number of touches to be accounted as level
    :param min_number_of_touches: minimum number of touches to be accounted as level
    :return: final chosen df with levels
    """
    df_drop = df.copy()
    # first take all prices with high number of touches
    df_max_touch_for_price = pd.DataFrame(df.groupby('price')['current_number_of_touches'].max()).reset_index()
    df_high_low_number_touches_for_price = df_max_touch_for_price[(df_max_touch_for_price['current_number_of_touches'] > max_number_of_touches) |
                                          (df_max_touch_for_price['current_number_of_touches'] < min_number_of_touches)]
    list_high_low_number_touches_for_price = df_high_low_number_touches_for_price['price'].tolist()
    df_to_keep = df_drop[~df_drop['price'].isin(list_high_low_number_touches_for_price)]
    return df_to_keep


def insert_levels(df_stock,
                  min_distance_between_touches,
                  max_distance_before_touch,
                  percent_change_calc,
                  percent_change_interval_to_check,
                  step_between_prices=1):
    """
    'This function inserts the levels into a dataFrame'
    :param percent_change_interval_to_check: define the time after touch to check for percentage of change
    :param percent_change_calc: which percentage counts as change
    :param min_distance_between_touches: in order to avoid many close touches
    :param df_stock: the dataFrame to take the levels from
    :param step_between_prices: default is one
    :return: returns level dataFrame
    """

    min_price = int(df_stock['Low'].min())
    max_price = int(df_stock['High'].max())
    dict_prices_touches = {}
    list_df = []

    for price in range(min_price, max_price):  # iterate over all prices from min to max
        dict_prices_touches[price] = []
        last_ind_touch = 0
        for ind, row in df_stock.iterrows():         # for each level of price iterate over all candles and count touches
            time_from_last_ind = check_last_date_touch(ind,last_ind_touch,min_distance_between_touches)
            if time_from_last_ind: # if time from last touch is less then minimum parameter min_distance_between_touches
                # skip the counting
                continue
            # print(ind, row)
            # if a price is between candle low and high values then we count as touch
            if row['Low'] <= price <= row['High']:
                date = str(row['Date'])

                current_num_of_touches = len(dict_prices_touches[price]) # count the number of touches until now
                if current_num_of_touches >= 2:
                    # print(price, current_num_of_touches, dict_prices_touches[price], date)
                    abs_change_in_price_after_some_time, price_of_touch, price_after_some_time, target = \
                        calculate_change_in_price(price,ind, df_stock, percent_change_calc,
                                                  percent_change_interval_to_check)

                    list_df.append([price,
                                    current_num_of_touches,
                                    dict_prices_touches[price],
                                    date,
                                    abs_change_in_price_after_some_time,
                                    price_of_touch,
                                    price_after_some_time,
                                    target])
                last_ind_touch = ind
                dict_prices_touches[price].append(date)
                # print(price, current_num_of_touches, dict_prices_touches[price])

    list_of_columns_names = ['price',
                             'current_number_of_touches',
                             'history',
                             'prediction_time',
                             'abs_change_in_price_after_some_time',
                             'price_of_touch',
                             'price_after_some_time',
                             'target']
    # make df with all levels
    df_l = pd.DataFrame(list_df, columns=list_of_columns_names)
    return df_l


# def create_table(df, min_touches_to_define, space_between_touches):
#     if


df_tsla = download_stock_data(ticker_name='TSLA', start_date='2021-01-14', end_date='2022-07-14', interval='1h')
df = insert_levels(df_tsla,min_distance_between_touches=4,percent_change_calc=3,percent_change_interval_to_check=5)
df_levels = drop_price_with_too_much_or_too_low_touches(df,max_number_of_touches=15,min_number_of_touches=4)
print(df_levels['target'].value_counts())
# plot
# print_list_of_lines(df_tsla,df_levels)
