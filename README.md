# Cryptobot
Build a trading bot in crypto coins using the Binance API.

This is a first though of what the structure on the server could look like.
Of course, this will probably change over time ;)

You can find the structure of all files in this repository. However, I will keep the final trading strategy for myself (at least for now).

# Directory Structure of the dag folder

```bash
├──  testing
│   ├──  cryptobot
│   │   ├── config.py
│   │   ├── utils.py
│   │   ├── dag.py
│   │   ├── requirements.txt
│   │   ├── trade
│   │   |   ├── BTC-USDT.py
│   │   |   ├── ETH-USDT.py
│   │   |   ├── ADA-USDT.py
│   │   |   ├──...
│   │   ├── cryptobot
│   │   |   ├──  __init__.py
│   │   |   ├──  account.py
│   │   |   ├──  coin.py
│   │   |   ├──  connectors.py
│   │   |   ├──  cryptobot.py
│   │   |   ├──  indicators.py
│   │   |   ├──  postgreslogger.py
│   │   ├──  README.MD
├──  production
│   ├──  cryptobot
│   │   ├── config.py
│   │   ├── utils.py
│   │   ├── dag.py
│   │   ├── requirements.txt
│   │   ├── trade
│   │   |   ├── BTC-USDT.py
│   │   |   ├── ETH-USDT.py
│   │   |   ├── ADA-USDT.py
│   │   |   ├──...
│   │   ├── cryptobot
│   │   |   ├──  __init__.py
│   │   |   ├──  account.py
│   │   |   ├──  coin.py
│   │   |   ├──  connectors.py
│   │   |   ├──  cryptobot.py
│   │   |   ├──  indicators.py
│   │   |   ├──  postgreslogger.py
│   │   ├──  README.MD
```

# Visualization
![ ](https://github.com/mbaardman/cryptobot/blob/main/structure.png)

# PostgreSQL Logger
This is the default database structure that is used for logging and storing relevant information. The structure of the database can be initialized via the initialize_tables function:
```
handler = PostgreSQLHandler(db_params)
handler.initialize_tables()
```

The tables and their structures can be modified in the PostgreSQLHandler object by adjusting the _tables property. Note that you will also need to define the colNames and the values that need to be stored. Example: if you want to add a 'test' table, you will need to (i) add 'test' to the _tables property, (ii) add a test_colNames functions that returns all colnames (no spaces after comma!) and (iii) add a test_values function that is able to define all values that will be logged in the tables.

**Default database structure**
![ ](https://github.com/mbaardman/cryptobot/blob/main/db_structure.png)

**Important note for usage:**
For logging, the user will need to specify the table where the information should be stored, this needs to be the first arg parameter. If nothing is specified, the logs table will be used. The second arg parameter should be a dictionary containing all additional information that is required to fill the table. If something is not specified, it will be set to None by the PostgreSQL handler. 

Example:
```
logger.info(message, # the logging message  
            table,   # the table where the info should be logged
            params)  # additional parameters that might be required for the table (e.g. information regarding the order)
```

Default info that is not required to be included in the addidional parameters and is obtained by the Handler itself: timestamp, date, time, timezone, level, filename, script and the message.

Example of how to use the logger:
```
logger = utils.get_PostgreSQLLogger()
order_info = {'coin': 'BTCUSDT', 
              'orderId':'xxx',
              'clientOrderId':'xxx',
              'orderType':'xxx',
              'side':'xxx',
              'timeInForce':'xxx',
              'quantity':'xxx',
              'price':'xxx',
              'stopPrice':'xxx'}
logger.info('this is a test message, 'orders', order_info)
```
