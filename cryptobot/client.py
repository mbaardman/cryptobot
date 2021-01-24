"""
Author: Marc Baardman
"""
from binance import client
import pandas as pd
import numpy as np
from datetime import datetime
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


class Client(object):

    def __init__(self, credentials):
        """
        Initialize the class
        Input:
            credentials - dict - dictionary of binance credentials that contains api_key and api_secret
        """
        self.api_key = credentials['api_key']
        self.api_secret = credentials['api_secret']
        self.client = self.connect_client(self.api_key, self.api_secret)

    def connect_client(self, api_key, api_secret):
        """
        Create Binance Client
        Input:
            api_key - str - Binance account api key
            api_secret - str - Binance account api secret
        Return:
            client - obj - Binance client object
        """
        return client.Client(api_key, api_secret)

    def get_server_time(self):
        """
        Get server current datetime (UTC) of the binance server
        Return:
            Datetime of the binance server
        """
        stamp = self.client.get_server_time()['serverTime']
        return datetime.utcfromtimestamp(stamp/1000).strftime('%Y-%m-%d %H:%M:%S')
