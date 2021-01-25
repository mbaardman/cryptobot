"""
Author: Marc Baardman
"""
from cryptobot import Cryptobot
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

class Coin(Cryptobot):

    def __init__(self, client, market):
        self.market = market
        self._client =  client

    def get_historic_klines(self, interval='15m', limit=500, return_=False):
        """
        Get all historic data for the coin. 
        Input:
            interval - str - Binance interval specification (default = 15 minutes)
            limit - int - # of historic interval periods that are imported (default = 500)
        """
        history = self._client.get_klines(symbol=self.market,
                                          interval=interval,
                                          limit=limit)
        df = pd.DataFrame(history, columns=config.history_colnames)
        df = df[config.select_historic_colnames]
        df['close_time'] = self.ms_to_datetime(df['close_time'])
        df.set_index('close_time', inplace=True)
        self.set_klines_attr(df)
        if return_:
            return df
        
    
    def set_klines_attr(self, df):
        print(df.columns)
        

    def get_recent_trades(self):
        # verhouding buy/sell
        return 1

    def get_orderbook(self):
        # verhouding buy/sell
        return 1

    def ms_to_datetime(self, ms):
        return pd.to_datetime(ms, unit = 'ms')
    





if __name__=="__main__":
    from connectors import Binance
    client = Binance(config.binance_parameters)
    coin = Coin(client.client, 'BTCUSDT')
    coin.get_historic_klines()
