# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 20:30:32 2021

@author: marcb
"""
import logging
import sys
## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
if 'crypto' not in hostname:
    sys.path.append('..')
    import config_secured as config
else:
    import config

from cryptobot.postgreslogger import PostgreSQLHandler

def get_PostgreSQLLogger(db_params):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) 
    postgres = PostgreSQLHandler(db_params)
    logger.addHandler(postgres)
    return logger

def close_PostgreSQLLogger(logger):
    logger.handlers.clear()
    logging.shutdown()
    
        
        
        

if __name__=="__main__":
    logger = get_PostgreSQLLogger(config.db_params)
    close_PostgreSQLLogger(logger)
