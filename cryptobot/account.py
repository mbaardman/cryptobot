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

class Account(object):

    def __init__(self, client):
        """
        Initialize the class
        Input:
            client - Binance client object
        """
        self.client = client

    def get_balances(self):
        """
        Obtain all balances of assets that belong to the Binance account
        Note: only returns assets where free balance > 0
        Output:
            balances - dataframe - all active assets of the binance account
        """
        balances = pd.DataFrame.from_dict(self.client.get_account()['balances'])
        return balances[balances.free.astype(float) > 0]

    def get_open_orders(self):
        """
        Get all active open orders
        Output:
            open_orders - dict - all active open order that belong to the Binance account
        """
        self.open_orders = self.client.get_open_orders()
        return self.open_orders

    def cancel_all_orders(self):
        """
        Cancel all open orders that are not yet executed
        """
        # Obtain all open_orders if not yet called
        if not hasattr(self, 'open_orders'):
            self.get_open_orders()
        for order in self.open_orders:
            self.client.cancel_order(symbol = order['symbol'], orderId = order['orderId'])

    def cancel_orderIds(self, orderIds):
        """
        Cancel specific order ID's
        Input:
            orderIds - list - list of orderID's that you want to cancel
        """
        # If a single orderID is given as input, then transform to list
        if type(orderIds) == int:
            orderIds = list(orderIds)
        # Obtain all open_orders if not yet called
        if not hasattr(self, 'open_orders'):
            self.get_open_orders()
        for id in orderIds:
            try:
                next(self.client.cancel_order(symbol = item['symbol'], orderId = id) for item in self.open_orders if item['orderId'] == id)
            except Exception as err:
                print(err)

    def market_buy(self, market, quantity, **kwargs):
        """
        Send market buy order to Binance
        Input:
            market - str - the market
            quantity - float - total amount you want to buy

            **kwargs optional parameters:
                quoteOrderQty - float - the amount the user wants to spend of the quote asset
                newClientOrderId - str - A unique id for the order. Automatically generated if not sent.
                newOrderRespType - str - Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
                recvWindow - int - the number of milliseconds the request is valid for
        """
        self.client.order_market_buy(symbol = market, quantity = quantity, **kwargs)

    def market_sell(self, market, quantity, **kwargs):
        """
        Send market sell order to Binance
        Input:
            market - str - the market
            quantity - float - total amount you want to buy

            **kwargs optional parameters:
                quoteOrderQty - float - the amount the user wants to spend of the quote asset
                newClientOrderId - str - A unique id for the order. Automatically generated if not sent.
                newOrderRespType - str - Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
                recvWindow - int - the number of milliseconds the request is valid for
        """
        self.client.order_market_sell(symbol = market, quantity = quantity, **kwargs)

    def limit_buy(self, market, quantity, price, timeInForce = 'GTC', **kwargs):
        """
        Send limit buy order to Binance
        Input:
            market - str - the market
            quantity - float - total amount you want to buy
            price - float - price per unit
            timeInForce - str - time that the order will be valid  (default = 'Good Till Valid')

            **kwargs optional parameters:
                stopPrice - float - Used with stop orders
                icebergQty - float - Used with iceberg orders
                newClientOrderId - str - A unique id for the order. Automatically generated if not sent.
                newOrderRespType - str - Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
                recvWindow - int - the number of milliseconds the request is valid for
        """
        self.client.order_limit_buy(symbol = market, quantity = quantity, price = price, timeInForce = timeInForce, **kwargs)

    def limit_sell(self, market, quantity, price, timeInForce = 'GTC', **kwargs):
        """
        Send limit sell order to Binance
        Input:
            market - str - the market
            quantity - float - total amount you want to buy
            price - float - price per unit
            timeInForce - str - time that the order will be valid  (default = 'Good Till Valid')

            **kwargs optional parameters:
                stopPrice - float - Used with stop orders
                icebergQty - float - Used with iceberg orders
                newClientOrderId - str - A unique id for the order. Automatically generated if not sent.
                newOrderRespType - str - Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
                recvWindow - int - the number of milliseconds the request is valid for
        """
        self.client.order_limit_sell(symbol = market, quantity = quantity, price = price, timeInForce = timeInForce, **kwargs)



if __name__=="__main__":
    client = Account(config.binance_parameters)
    #print(client.get_balances())
    #print(client.get_open_orders())
    client.cancel_orderIds([96519891, 580153738])
