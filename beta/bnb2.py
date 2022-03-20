from tkinter import SEL_LAST
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from datetime import datetime
from binance.enums import *

#in case of failed bnb dependency: https://stackoverflow.com/questions/59973858/why-am-i-getting-this-error-modulenotfounderror-no-module-named-binance-clien

client = Client('P9J7BuCrMHmOaxyKf6zMQ9IGkKXYx1mMz2CCkz0jxVfJaIaiceijcYFGUeb8U365', 'nNCxE9JXN1OJHwglHmRKe3B4C5TaU1lq3XuGgbQTyU0ONYrzBkVxrFA3dwH4UidI', {"verify": False, "timeout": 20})

def get_min_data(symbol,interval,lookback):
    #calls the API to get raw data
    frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback))
    frame = frame.iloc[:,:6]
    frame.columns = ['Date','Open','High','Low','Close','Volume']
    frame['Open'] = frame['Open'].map(lambda x: float(x))
    frame['High'] = frame['High'].map(lambda x: float(x))
    frame['Low'] = frame['Low'].map(lambda x: float(x))
    frame['Close'] = frame['Close'].map(lambda x: float(x))   
    frame['Volume'] = frame['Volume'].map(lambda x: float(x))
    frame['Date'] = frame['Date'].map(lambda d: datetime.fromtimestamp(int(d)/1000))
    frame.index = frame['Date']
    del frame['Date']
    return frame

def dataset_loader(asset):
    #transforms data so the model can eat it 
    dataset = get_min_data(asset,'1m','50000m')
    df = pd.DataFrame(dataset)
    return df

def openTrade(amount,trades):
    #{'Date': Timestamp('2022-01-31 11:28:00'), 'High': 37889.0, 'Low': 37846.36, 'total': 0.026397043742277217, 'type': 'buy', 'current_price': 37883.03}
    pass

def closeTrade(trade):
    print(f"AI closed a trade")
    print(trade)