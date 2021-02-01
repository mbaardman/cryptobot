"""
Author: Marc Baardman
"""
from cryptobot import Cryptobot
from datetime import datetime
import pandas as pd
import sys
import inspect
#from itertools import filter

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

    def __init__(self, client, market, interval='15m', limit=500):
        self.market = market
        self._client =  client
        self.interval = interval
        self.limit = limit
        self.start_time, self.end_time = self._interval_to_milliseconds(interval, limit)


    def get_historic_klines(self, return_=False):
        """
        Get all historic data for the coin.
        Input:
            interval - str - Binance interval specification (default = 15 minutes)
            limit - int - # of historic interval periods that are imported (default = 500)
        """
        history = self._client.get_klines(symbol=self.market,
                                          interval=self.interval,
                                          limit=self.limit)
        df = pd.DataFrame(history, columns=config.all_history_colnames)
        df = df[config.select_historic_colnames]
        df['datetime'] = self.ms_to_datetime(df[config.klines_datetime_column])
        df.set_index('datetime', inplace=True)
        self.set_klines_attr(df)
        if return_:
            return df

    def get_ticker_info(self):
        return self._client.get_ticker(symbol=self.market)

    def set_ticker_info(self):
        self.ticker_info = self.get_ticker_info()


    def set_klines_attr(self, df):
        """
        Set the columns of the historic klines as individual attributes.
        This will be usefull for all technical indicators.
        """
        self.klines_open = df['open']
        self.klines_high = df['high']
        self.klines_low = df['low']
        self.klines_close = df['close']
        self.klines_volume = df['volume']
        self.klines_trades = df['cnt_trades']
        self.klines_timestamp = df[config.klines_datetime_column]
        self.klines_buy_base_asset_volume = df['taker_buy_base_asset_volume']
        self.klines_buy_quote_asset_volume = df['taker_buy_quote_asset_volume']

    def get_recent_trades(self, start = None, stop = None, limit = 500):
        if hasattr(self, 'klines_timestamp'):
            self._client.get_aggregate_trades(symbol=self.market,
                                              startTime=min(self.klines_timestamp),
                                              endTime=max(self.klines_timestamp))
        else:
            self._client.get_aggregated_trade

    def get_orderbook(self):
        orderbook = self._client.get_order_book(symbol=self.market, limit = 1000)
        df = pd.DataFrame()
        for col in config.orderbook_colnames:
            df_temp = pd.DataFrame(orderbook[col].copy())
            df_temp.columns = [col + metric for metric in ['_rate', '_quantity']]
            df = pd.concat([df, df_temp], axis = 1)
        self.orderbook = df
        self.set_orderbook_ratio(df, config.orderbook_ratios)

    def set_orderbook_ratio(self, orderbook, ratios):
        output = {}
        for ratio in ratios:
            buy_quantity = (
                    orderbook.loc[orderbook['bids_rate'].astype(float) >= (float(max(orderbook['bids_rate']))*(1-ratio)), 'bids_quantity']
                            .astype(float)
                            .sum()
            )
            sell_quantity = (
                    orderbook.loc[orderbook['asks_rate'].astype(float) >= (float(max(orderbook['asks_rate']))*(1-ratio)), 'asks_quantity']
                            .astype(float)
                            .sum()
            )
            output['ratio_'+str(ratio)] = buy_quantity/sell_quantity
        self.orderbook_ratios = output

    def ms_to_datetime(self, ms):
        return pd.to_datetime(ms, unit = 'ms')

    def _interval_to_milliseconds(self, interval, limit):
        """
        Convert a Binance interval string to milliseconds
        :param interval: Binance interval string, e.g.: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
        :type interval: str
        :return:
             int value of interval in milliseconds
             None if interval prefix is not a decimal integer
             None if interval suffix is not one of m, h, d, w
        """
        seconds_per_unit = {
            "m": 60,
            "h": 60 * 60,
            "d": 24 * 60 * 60,
            "w": 7 * 24 * 60 * 60,
        }
        interval_time = int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
        now = self.get_current_ms_time_utc()

        return now, now - (interval_time * limit)

    def get_current_ms_time_utc(self):
        """ Get the current datetime in UTC timezone in milliseconds. """
        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)





if __name__=="__main__":
    from connectors import Binance
    client = Binance(config.binance_parameters)
    coin = Coin(client.client, 'BTCUSDT')
    #coin.get_orderbook()
    coin.get_historic_klines()
