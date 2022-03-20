from tkinter import SEL_LAST
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from datetime import datetime
from binance.enums import *

#import urllib3
#urllib3.disable_warnings()
#in case of failed bnb dependency: https://stackoverflow.com/questions/59973858/why-am-i-getting-this-error-modulenotfounderror-no-module-named-binance-clien


#BNB library: https://python-binance.readthedocs.io/en/latest/general.html
#BNB API: https://binance-docs.github.io/apidocs/spot/en/#test-new-order-trade

client = Client('P9J7BuCrMHmOaxyKf6zMQ9IGkKXYx1mMz2CCkz0jxVfJaIaiceijcYFGUeb8U365', 'nNCxE9JXN1OJHwglHmRKe3B4C5TaU1lq3XuGgbQTyU0ONYrzBkVxrFA3dwH4UidI', {"verify": True, "timeout": 20})
ping = client.ping()
status = client.get_system_status()
print(f'The status is {status}')

"""
# trading info
info = client.get_symbol_info('BTCUSDT')
print(info['filters'][2]['minQty'])
raise NotImplementedError
#info = client.get_account()
#print(f'The client info {info}')
"""

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
    amount = float(round(amount,6))
    #{'Date': Timestamp('2022-01-31 11:28:00'), 'High': 37889.0, 'Low': 37846.36, 'total': 0.026397043742277217, 'type': 'buy', 'current_price': 37883.03}
    print(f'AI bought {amount}, trade: {trades[-1]}')
    order = client.create_test_order(
            symbol='BTCUSDT',
            side="BUY",
            type="MARKET",
            quantity=0.1)

def closeTrade(amount,trades):
    print(f'AI sold {amount}, trade: {trades[-1]}')
    order = client.create_test_order(
            symbol='BTCUSDT',
            side="SELL",
            type="MARKET",
            quantity=0.1)

def getOrders():
    orders = client.get_all_orders(symbol='BTCUSDT', limit=10)
    print(orders)

def getFees(symbol):
    fees = client.get_trade_fee(symbol='BTCUSDT')
