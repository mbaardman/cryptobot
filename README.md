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
│   │   ├── dag.py
│   │   ├── trade
│   │   |   ├── BTC-USDT.py
│   │   |   ├── ETH-USDT.py
│   │   |   ├── ADA-USDT.py
│   │   |   ├──...
│   │   ├── cryptobot
│   │   |   ├──  __init__.py
│   │   |   ├──  alerts.py
│   │   |   ├──  client.py
│   │   |   ├──  account.py
│   │   |   ├──  coin.py
│   │   |   ├──  indicators.py
│   │   |   ├──  order.py
│   │   ├──  README.MD
├──  production
│   ├──  cryptobot
│   │   ├── config.py
│   │   ├── dag.py
│   │   ├── trade
│   │   |   ├── BTC-USDT.py
│   │   |   ├── ETH-USDT.py
│   │   |   ├── ADA-USDT.py
│   │   |   ├──...
│   │   ├── cryptobot
│   │   |   ├──  __init__.py
│   │   |   ├──  alerts.py
│   │   |   ├──  client.py
│   │   |   ├──  account.py
│   │   |   ├──  coin.py
│   │   |   ├──  indicators.py
│   │   |   ├──  order.py
│   │   ├──  README.MD
```

# Visualization
![ ](https://github.com/mbaardman/cryptobot/blob/main/structure.png)

# PostgreSQL database Structure
- **Account** - store all information that is related to my Binance account
- **Balance** - all balances (per coins and total balance)
- **Orders** - all orders that are being pushed to Binance
- **Transactions** - save all successfull orders
- **Logs** - store all error messages in the code

(datamodel might be added later)
