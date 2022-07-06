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

import plotly.io as pio
pio.renderers.default = "browser"

# Obtaining historical stock pricing data
ticker_symbol = 'AMD'
ticker = yfinance.Ticker(ticker_symbol)

start_date = '2020-08-01'
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
        # print(f'i is: {i}')
        # print(f'df1.High[i] is: {df1.High[i]}')
        # print(f'df1.High[i-1] is: {df1.High[i-1]}')

        if df1.High[i] < df1.High[i-1]:
            return 0
    for i in range(candle+1,candle+days_after1+1):

        if df1.High[i] > df1.High[i-1]:
            return 0
    return 1


# resistance(df, 30, 3, 5)


# dfpl = df[0:250]
# import plotly.graph_objects as go
# from datetime import datetime

# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close'])])
#
# fig.show()
#
# sr = []
# days_before=4
# days_after=4
# for row in range(6, 205): #len(df)-n2
#     print(f'row is {row}')
#     print(f'support is :{support(df, row, days_before, days_after)}')
#     if support(df, row, days_before, days_after):
#         sr.append((row,df.Low[row],1))
#     print(f'resistance is :{resistance(df, row, days_before, days_after)}')
#     if resistance(df, row, days_before, days_after):
#         sr.append((row,df.High[row],2))
# print(sr)
#
#
# s = 0
# e = 200
# dfpl = df[s:e]
# import plotly.graph_objects as go
# from datetime import datetime
# import matplotlib.pyplot as plt
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close'])])
#
# c=0
# while (1):
#     if(c>len(sr)-1 ):#or sr[c][0]>e
#         break
#     fig.add_shape(type='line', x0=s, y0=sr[c][1],
#                   x1=e,
#                   y1=sr[c][1]
#                   )#x0=sr[c][0]-5 x1=sr[c][0]+5
#     c+=1
# fig.show()



# # -----------------------------------------------
# plotlist1 = [x[1] for x in sr if x[2]==1]
# plotlist2 = [x[1] for x in sr if x[2]==2]
# plotlist1.sort()
# plotlist2.sort()
#
# for i in range(1,len(plotlist1)):
#     if(i>=len(plotlist1)):
#         break
#     if abs(plotlist1[i]-plotlist1[i-1])<=0.005:
#         plotlist1.pop(i)
#
# for i in range(1,len(plotlist2)):
#     if(i>=len(plotlist2)):
#         break
#     if abs(plotlist2[i]-plotlist2[i-1])<=0.005:
#         plotlist2.pop(i)
# plotlist2
# # plt.hist(plotlist, bins=10, alpha=0.5)
# # ---------------------------------------------
# s = 0
# e = 200
# dfpl = df[s:e]
# import plotly.graph_objects as go
# from datetime import datetime
# import matplotlib.pyplot as plt
#
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close'])])
#
# c=0
# while (1):
#     if(c>len(plotlist1)-1 ):#or sr[c][0]>e
#         break
#     fig.add_shape(type='line', x0=s, y0=plotlist1[c],
#                   x1=e,
#                   y1=plotlist1[c],
#                   line=dict(color="MediumPurple",width=3)
#                   )
#     c+=1
#
# c=0
# while (1):
#     if(c>len(plotlist2)-1 ):#or sr[c][0]>e
#         break
#     fig.add_shape(type='line', x0=s, y0=plotlist2[c],
#                   x1=e,
#                   y1=plotlist2[c],
#                   line=dict(color="RoyalBlue",width=1)
#                   )
#     c+=1
#
# fig.show()
#
# # ---------------------------------------------------------

ss = []
rr = []
n1=2
n2=2
for row in range(4, 205): #len(df)-n2
    if support(df, row, n1, n2):
        ss.append((row,df.Low[row]))
    if resistance(df, row, n1, n2):
        rr.append((row,df.High[row]))

# -----------------------------------------------
s = 0
e = 200
dfpl = df[s:e]
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])

c=0
while (1):
    if(c>len(ss)-1 ):
        break
    fig.add_shape(type='line', x0=ss[c][0], y0=ss[c][1],
                  x1=rr[c][0] -30,
                  y1=ss[c][1],
                  line=dict(color="MediumPurple",width=1)
                  )
    c+=1

c=0
while (1):
    if(c>len(rr)-1 ):
        break
    print(rr[c][0])
    print(rr[c][1])

    fig.add_shape(type='line', x0=rr[c][0], y0=rr[c][1],
                  x1=rr[c][0] - 30,
                  y1=rr[c][1],
                  line=dict(color="RoyalBlue",width=1)
                  )
    c+=1

fig.show()

# ---------------------------------------------------------------------