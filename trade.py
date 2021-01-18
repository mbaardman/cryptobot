"""
Author: Marc Baardman
"""
from cryptobot import *
import config
import sys
from sqlalchemy import create_engine
from datetime import datetime, timedelta

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
    try:
        alert = SMSAlerts(config.twilio_account, config.twilio_token, config.twilio_from_phone, config.twilio_to_phone)
        print(prod_flow)
    except Exception as e:
        # Write error message to database (datetime, coin, type of error, exact error, complete log?)
        # Send text message?
        alert.
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
        

# Eventually, the coin will be passed as an argument in the bash command
#
coin = 'USD-BTC'
if __name__ != "__main__":
    coin = sys.argv[1]


run(prod_flow = config.prod_flow)
#run(prod_flow = config.prod_flow,
#    connectionString = config.connection_string,
#    bittrex_auth = config.bittrex_parameters,
#    coins = config.list_markets,
#    time_delta = config.transactions_time_delta,
#    colnames = config.transactions_colnames,
##    current_datetime = datetime.utcnow(),
 #   write_table = config.transactions_write_table,
 #   write_schema = config.write_schema)
