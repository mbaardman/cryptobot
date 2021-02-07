# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 21:16:57 2021

@author: marcb
"""
from cryptobot.cryptobot import Cryptobot
import logging
import psycopg2
import sys
import traceback
from datetime import datetime

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
if 'crypto' not in hostname:
    sys.path.append('../..')
    import config_secured as config
else:
    import config


class PostgreSQLHandler(logging.Handler, Cryptobot):
    
    # default query
    _query = "INSERT INTO marc.{} ({}) VALUES ({})"
    #_query = "CREATE TABLE marc.{} {} VALUES {}"
    # see TYPE log_level
    _levels = ('debug', 'info', 'warning', 'error', 'critical')
    # logging level
    _logLevel = logging.DEBUG
    # tables
    _tables = ('logs', 'transactions', 'orders', 'account', 'balances')
    _tableSuffix = '_colNames'
    _valueSuffix = '_values'
    
    def __init__(self, db_config):
        Cryptobot.__init__(self)
        logging.Handler.__init__(self)
        self.db_config = db_config
        self.connection = self.set_connection(db_config)
        self.connection.autocommit = False
        self.failed = False
        self.cursor = self.connection.cursor()
        
       
    def set_connection(self, db_config):
        try:    
            conn = psycopg2.connect(**db_config)
            return conn
        except:
            self.create_alert('Failed to connect to PostgreSQL database.')
    
    
    def emit(self, record):
        """
        Hier moet puur het wegschrijven
        1 arg is verplicht (namelijk tabel waar het heen moet)
        2e arg is niet verplicht denk ik
        """
        try:
            # First args (table) is mantarory
            if (len(record.args) == 0) | (record.args[0] not in self._tables):
                table = 'logs'
            else:
                table = record.args[0]
            # Second args (params of the logging table) is optional because
            # it is not required for the logging table
            try:
                params = record.args[1]
            except:
                params = None
            colNames = getattr(self, table+self._tableSuffix)
            recordDict = self.get_recordDict(record, params)
            for col in colNames.split(','):
                if col not in recordDict.keys():
                    recordDict[col] = None
            func = getattr(self, table+self._valueSuffix)
            values = func(recordDict)
            #self.create_table_first_time(table, values, colNames)
            query = self._query.format(table, colNames, values)
            self.cursor.execute(query)
        except Exception as err:
            print(err)
            self.failed = True
            #failed_query = self.failed_query(record, err)
            #self.cursor.execute(self.failed_query)
    
    def initialize_tables(self):
        import pandas as pd
        from sqlalchemy import create_engine
        engine =  create_engine(config.connectionString)
        for table in self._tables:
            colNames = getattr(self, table+self._tableSuffix)
            recordDict = {"timestamp": datetime.utcnow().timestamp()}
            for col in colNames.split(','):
                if col not in recordDict.keys():
                    recordDict[col] = None
            func = getattr(self, table+self._valueSuffix)
            values = func(recordDict)
            df = pd.DataFrame(values.split(','), index=colNames.split(',')).T
            df.to_sql(table, con=engine, schema = 'marc', index = False, if_exists = 'replace')
            
    def failed_query(self, record, err):
        return "INSERT INTO marc.logs" \
                "(datetime, level, filename, script, message, linenr, params)" \
             "VALUES " \
                "(utcnow(), critical , {}, {}, {}, None, None)".format(record.filename, record.module, err)
    
    def get_recordDict(self, record, params):
        level = record.levelname.lower()
        if level not in self._levels:
            level = "debug"
        msg_args = {
                "timestamp": datetime.utcnow().timestamp(),
                "date": datetime.utcnow().date(),
                "time": datetime.utcnow().strftime("%H.%M.%S"),
                "timezone": 'UTC',
                "level": level,
                "message": record.msg,
                "filename": record.filename,
                "script": record.module,
                "logger": record.name,
                "function": record.funcName,
                "linenr": record.lineno,
                "request_path": getattr(record, "request_path", None),
                "flask_endpoint": getattr(record, "flask_endpoint", None),
                "remote_addr": getattr(record, "remote_addr", None),
                "session_id": getattr(record, "session_id", None),
                "user_id": getattr(record, "user_id", None),
                "params": params
            }
        if type(params) == dict:
            msg_args.update(params)
        return msg_args
    
    @property
    def logs_colNames(self):
        return 'timestamp,date,time,timezone,level,filename,script,message,linenr,params'
    
    @property
    def account_colNames(self):
        return 'timestamp,date,time,timezone,level,filename,script,status,permissions,can_trade'
    
    @property
    def balances_colNames(self):
        return 'timestamp,date,time,timezone,level,filename,script,coin,free_balance,locked_balance,total_balance'
    
    @property
    def orders_colNames(self):
        return 'timestamp,date,time,timezone,level,filename,script,coin,orderId,clientOrderId,orderType,side,timeInForce,quantity,price,stopPrice'
    
    @property
    def transactions_colNames(self):
        return 'timestamp,date,time,timezone,level,filename,script,coin,orderId,clientOrderId,status'
    
    def logs_values(self, dictRecord):
        return '%(timestamp)f, %(date)s, %(time)s, %(timezone)s, %(level)s , %(filename)s, %(script)s, %(message)s, %(linenr)s, %(params)s'%(dictRecord)
    
    def account_values(self, dictRecord):
        return '%(timestamp)f, %(date)s, %(time)s, %(timezone)s, %(level)s , %(filename)s, %(script)s, %(status)s, %(permissions)s, %(can_trade)s'%(dictRecord)
    
    def balances_values(self, dictRecord):
        return '%(timestamp)f, %(date)s, %(time)s, %(timezone)s, %(level)s , %(filename)s, %(script)s, %(coin)s, %(free_balance)s, %(locked_balance)s, %(total_balance)s'%(dictRecord)
    
    def orders_values(self, dictRecord):
        return '%(timestamp)f, %(date)s, %(time)s, %(timezone)s, %(level)s , %(filename)s, %(script)s, %(coin)s, %(orderId)s, %(clientOrderId)s, %(orderType)s, %(side)s, %(timeInForce)s, %(quantity)s, %(price)s, %(stopPrice)s'%(dictRecord)
    
    def transactions_values(self, dictRecord):
        return '%(timestamp)f, %(date)s, %(time)s, %(timezone)s, %(level)s , %(filename)s, %(script)s, %(coin)s, %(orderId)s, %(clientOrderId)s, %(status)s'%(dictRecord)

