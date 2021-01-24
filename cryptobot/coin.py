"""
Author: Marc Baardman
"""
from binance import client
from datetime import datetime
import pandas as pd
import sys

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
if 'crypto' not in hostname:
    sys.path.append('../..')
    import config_secured as config
else:
    import config
    
class Coin(object):
    
    def __init__(self, market):
        self.market = market
        self._client =  client.Client()
    
    def get_history(self, interval = '15m', limit = 500):
        history = self._client.get_klines(symbol = self.market, 
                                          interval = interval,
                                          limit = limit)
        df = pd.DataFrame(history, columns = config.history_colnames)
        print(df.head())
        df['open_time'] = self.ms_to_datetime(df['open_time'])
        print(df.head())
        
    def get_recent_trades(self):
        # verhouding buy/sell
        return 1
    
    def get_orderbook(self):
        # verhouding buy/sell
        return 1
    
    def ms_to_datetime(self, ms):
        ms = ms/1000
        print(ms)
        return datetime.fromtimestamp(ms/1000)
    
    
        
        
        
if __name__=="__main__":
    coin = Coin('BTCUSDT')
    coin.get_history()
    