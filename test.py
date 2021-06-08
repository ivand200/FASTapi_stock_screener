from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other, get_quote_table
import yahoo_fin.stock_info as si
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import pandas as pd
import json
import urllib.request, urllib.parse, urllib.error


# Define previous month
now = datetime.now()
lastmonth = now - timedelta(weeks=5)
endoflastmonth = lastmonth.replace(day=28)
month_ago = endoflastmonth.strftime("%Y-%m-%d")
start_ = now - timedelta(weeks=120)
start_time = start_.strftime("%Y-%m-%d")
