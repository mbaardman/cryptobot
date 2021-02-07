"""
Author: Marc Baardman
"""
import sys
sys.path.append('..')
from cryptobot import *
## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
if 'crypto' not in hostname:
    sys.path.append('../..')
    import config_secured as config
else:
    import config
from sqlalchemy import create_engine
from datetime import datetime, timedelta

COIN = 'BTCUSDT'

# cancel al open orders, alleen in account ding?

def run(**kwargs):
    """
    Entire process that needs to run to create the final table.
    Input parameters:
        coin - str - market that is evaluated
        prod_flow - boo - true if production flow, false if not
        connectionString - str - connectionstring to connect to database
        binanceAuth - dict - authentication parameters for Binance API
        coin
    """
    sms = alerts.SMSAlerts(config.twilio_account, config.twilio_token, config.twilio_from_phone, config.twilio_to_phone)
    try:
        engine = create_engine(config.connectionString)
        print(config.prod_flow)
    except Exception as e:
        # Write error message to database (datetime, coin, type of error, exact error, complete log?)
        # Send text message?
        sms.alert('Process failed for coin {}'.format(COIN))
        print(e.__class__.__name__)
        print(e)

def import_data():
    """
    Import all data that is required in order to create the final table
    """
    return 1

def write_data(df, connectionString, write_table, write_schema):
    """
    Write table to destination
    """
    engine = create_engine(connectionString)
    df.to_sql(name = write_table, con = engine, schema = write_schema, index = False, if_exists = 'append')
    
def finish():
    # close connection
    # check if logging all went fine --> anders een smsje met naam van het script


run(coin = COIN)
#run(prod_flow = config.prod_flow,
#    connectionString = config.connection_string,
#    bittrex_auth = config.bittrex_parameters,
#    coins = config.list_markets,
#    time_delta = config.transactions_time_delta,
#    colnames = config.transactions_colnames,
##    current_datetime = datetime.utcnow(),
 #   write_table = config.transactions_write_table,
 #   write_schema = config.write_schema)
