import pandas as pd
import numpy as np
import yfinance
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt


def download_stock_data(ticker_name, start_date, end_date, interval):
    ticker_symbol = ticker_name
    ticker = yfinance.Ticker(ticker_symbol)

    df = ticker.history(interval=interval, start=start_date, end=end_date)
    df['Date'] = pd.to_datetime(df.index)  # turn the index into a date column
    df = df.reset_index().drop('index', axis=1)

    return df


def insert_levels(df, step_between_prices=1):
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
        for ind, row in df.iterrows():         # for each level of price iterate over all candles and count touches
            # print(ind, row)
            # if a price is between candle low and high values then we count as touch
            if row['Low'] <= price <= row['High']:
                date = str(row['Date'])
                current_num_of_touches = len(dict_prices_touches[price])
                if current_num_of_touches >= 3:
                    print(price, current_num_of_touches, dict_prices_touches[price], date)
                    list_df.append([price, current_num_of_touches, dict_prices_touches[price], date])
                dict_prices_touches[price].append(date)
                # print(price, current_num_of_touches, dict_prices_touches[price])
    df = pd.DataFrame(list_df, columns=['price', 'current_number_of_touches', 'history', 'prediction'])
    return df


# def create_table(df, min_touches_to_define, space_between_touches):
#     if


df_tsla = download_stock_data(ticker_name='TSLA', start_date='2021-02-14', end_date='2021-06-14', interval='1h')
df = insert_levels(df_tsla)
