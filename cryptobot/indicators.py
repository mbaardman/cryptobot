"""
Author: Marc Baardman
"""
from cryptobot import Cryptobot
from binance import client
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import btalib

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
if 'crypto' not in hostname:
    sys.path.append('../..')
    import config_secured as config
else:
    import config


class Indicator(Cryptobot):

    def list_bta_indicators(self):
        return btalib.get_ind_names()
    
    def get_bta_metrics(self, ohlcv, params):
        assert set(['open', 'high', 'low', 'close', 'volume']).issubset(ohlcv.columns.values)
        output = {}
        for indicator in params:
            indicator_params = params[indicator]
            func = getattr(btalib, indicator, self.indicator_not_found)
            ti_series = func(df[indicator_params['column']].astype(float), **indicator_params['params'])
            try:
                output[indicator] = ti_series[indicator].series[-1]
            except TypeError:
                output[indicator] = ti_series
            except:
                pass #raise alert later on
        return output
    
    def indicator_not_found(self, *args, **kwargs):
        return np.NaN
    
        
if __name__=="__main__":
    params = {
    'smsa': 
          {
              'column': 'close',
              'params': { 'period' : 4}
          },
    'rsi':
        {
              'column': 'close',
              'params': { 'period' : 14}             
        }
        }
    b = Indicator()
    df = b.get_test_data()
    b.get_bta_metrics(df, params)
    