"""
Configuration File
Author: Marc Baardman
"""


##############################################################
################### Server parameters ########################
##############################################################

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()

import os
full_path = os.path.realpath(__file__)
if hostname == '': # the name of your VM
    ENV = full_path.split("/")[:-2]
else:
    ENV = full_path.split("\\")[-2]
prod_flow = (ENV == 'prod')


##############################################################
####################### List of Coins ########################
##############################################################

# Overall parameters
list_markets = [] # list of all markets on Binance


##############################################################
############### Airflow parameters parameters ################
##############################################################

from datetime import datetime, timedelta
airflow_schedule_interval='0 * * * *' # Run every hour

airflow_default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

airflow_relative_path = 'trade.py'


##############################################################
################### Connection parameters ####################
##############################################################

# Account information
# Fill in your twilio account information
twilio_account = ''
twilio_token = ''
twilio_from_phone = ''
twilio_to_phone = ''
sleep_seconds = 40

# Connection Settings
conn_parameters = {
    'connector' : 'postgresql+psycopg2',
    'postgres_user' : '',
    'postgres_passwd': '',
    'hostname' : '',
    'database' : ''
}

# Data in this input file, should always be written in the 'input' schema in the database
if prod_flow:
    write_schema = 'production'
else:
    write_schema = 'testing'

# When run on the vm, hostname = localhost
if hostname == '': # Fill in the name of your VM
    conn_parameters['hostname'] = 'localhost'

# create connectionstring
connection_string = conn_parameters['connector']+'://'+conn_parameters['postgres_user']+':'+conn_parameters['postgres_passwd']+'@'+ conn_parameters['hostname'] + '/' + conn_parameters['database']

# bittrex authencication parameters
# Fill in your Binance account api parameters
binance_config = {
    'key' : '',
    'secret' : ''
}
