import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/IGN1L.VS.csv')
data['Date'] = pd.to_datetime(data['Date'], format="%Y-%m-%d")

apple = pd.read_csv('data/AAPL.csv')
apple['Date'] = pd.to_datetime(apple['Date'], format="%Y-%m-%d")

#1 William %R

def william(period, high, low, close):
    highh = high.rolling(period).max()
    lowl = low.rolling(period).min()
    apple['wr'] = -100 * ((highh - close) / (highh - lowl))

william(14, apple['High'], apple['Low'], apple['Close'])

#2 AD
def AD(data, high='High', low='Low', close='Close', volume='Volume'):
    data['AD'] = 0
    for index, row in data.iterrows():
        if (index == 0):
            ad = ((row[close] - row[low]) - (row[high] - row[close])) / (row[high] - row[low]) * row[volume]
            data.at[index, 'AD'] = ad
        elif (row[high] != row[low]):
            ad = ((row[close] - row[low]) - (row[high] - row[close])) / (row[high] - row[low]) * row[volume]
            data.at[index, 'AD'] = ad + data.at[index-1, 'AD']
        else:
            clv = data.at[index-1, 'AD']
            data.at[index, 'AD'] = clv

    data['AD'].fillna(0.0)
    return data

AD(apple)
#apple['AD'].fillna(0.0)

#3
def NVI(df):
    df['nvi'] = 0.
    vol_decrease = df['Volume'].shift(1) > df['Volume']

    df['nvi'].iloc[0] = 1000

    for i in range(1, len(df['nvi'])):
        if vol_decrease[i]:
            df['nvi'].iloc[i] = df['nvi'].iloc[i-1] + ((df['Close'].iloc[i] - df['Close'].iloc[i-1])
                                                      / df['Close'].iloc[i-1] * df['nvi'].iloc[i-1])
        else:
            df['nvi'].iloc[i] = df['nvi'].iloc[i-1]

NVI(apple)

apple.plot(x='Date', y='AD', kind='line')
apple.plot(x='Date', y='wr', kind='line')
apple.plot(x='Date', y='nvi', kind='line')