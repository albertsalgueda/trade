from tkinter import SEL_LAST
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from datetime import datetime


#in case of failed bnb dependency: https://stackoverflow.com/questions/59973858/why-am-i-getting-this-error-modulenotfounderror-no-module-named-binance-clien

client = Client('P9J7BuCrMHmOaxyKf6zMQ9IGkKXYx1mMz2CCkz0jxVfJaIaiceijcYFGUeb8U365', 'nNCxE9JXN1OJHwglHmRKe3B4C5TaU1lq3XuGgbQTyU0ONYrzBkVxrFA3dwH4UidI')

def get_min_data(symbol,interval,lookback):
    #calls the API to get raw data
    frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame['Close'] = frame['Close'].map(lambda x: float(x))
    frame['Time'] = frame['Time'].map(lambda d: datetime.fromtimestamp(int(d)/1000))
    frame.index = frame['Time']
    return frame


def dataset_loader(asset):
    #transforms data so the model can eat it 
    dataset = get_min_data(asset,'1m','1200m')
    close = dataset['Close']
    return close

def openTrade(amount,trades):
    #{'Date': Timestamp('2022-01-31 11:28:00'), 'High': 37889.0, 'Low': 37846.36, 'total': 0.026397043742277217, 'type': 'buy', 'current_price': 37883.03}
    client.open_trade
    order = client.create_test_order(
            symbol='BNBBTC',
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=amount,
            price='0.00001')
    print(order)
    print(f"AI bought {amount} of BTC")
    print(trades)