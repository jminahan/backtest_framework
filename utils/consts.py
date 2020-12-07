##imports
import datetime

##FIELDS
DB_CONNECTION_FIELD = "DB_CONNECTION_FIELD"
DB_CONNECTION_HOST_FIELD = "DB_CONNECTION_HOST"
DB_CONNECTION_PORT_FIELD = "DB_CONNECTION_POST"

#SIM FIELDS
SIM_PARAMS_FIELD = "SIM_PARAMS_FIELD"
SIM_PARAMS_TICKER_LIST_FIELD = "SIM_PARAMS_TICKER_LIST_FIELD"
SIM_PARAMS_START_DATE_FIELD = "SIM_PARMS_START_DATE_FIELD"
SIM_PARAMS_END_DATE_FIELD = "SIM_PARAMS_END_DATE_FIELD"

##VALUES
DB_CONNECTION = "test"
DB_CONNECTION_HOST = "localhost"
DB_CONNECTION_PORT = 27017

##
DEFAULT_YAHOO_HISTORICAL_START_DATE = 0
DEFAULT_YAHOO_HISTORICAL_END_DATE = 9607126400

###Sim Vars

##Sim Run params
SIM_PARAMS_TICKER_LIST = ["AAPL","SPY"]
SIM_PARAMS_START_DATE = datetime.datetime(2020, 11, 2)
SIM_PARAMS_END_DATE =  datetime.datetime(2020, 11, 30)

##Trade types
TRADE_BUY = "BUY_SIGNAL"
TRADE_SELL = "SELL_SIGNAL"
VALID_TRADE_TYPES = [TRADE_BUY, TRADE_SELL]

###Strategy titles
BUY_AND_HOLD_TITLE = "BUY_AND_HOLD"
BUY_AND_HOLD_SPECIFIC_TITLE = "BUY_AND_HOLD_SPECIFIC_TITLE"

##HOLIDAYS
HOLIDAYS = [
    datetime.datetime(2020, 11, 26)
]