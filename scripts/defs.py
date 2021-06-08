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


def shares_outstanding(ticker):
    """Get Shares outstanding"""
    url = (f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    shares = (data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["sharesOutstanding"]["raw"])
    return shares


def average_income(ticker):
    """Average income for last 4 years"""
    url = (f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=incomeStatementHistory")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    year1 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][0]["netIncome"]["raw"])
    year2 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][1]["netIncome"]["raw"])
    year3 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][2]["netIncome"]["raw"])
    year4 = (data["quoteSummary"]["result"][0]["incomeStatementHistory"]["incomeStatementHistory"][3]["netIncome"]["raw"])
    return (year1 + year2 + year3 + year4) / 4


def get_close_price(share):
    """Last close price"""
    try:
        ticker = si.get_quote_table(share)['Previous Close']
        return ticker
    except:
        return 0


def get_ep(share):
    """E/P"""
    try:
        e_p = round(((average_income(share) / shares_outstanding(share))
                      / get_close_price(share)), 2)
        return e_p
    except:
        return 0

def get_pe(share):
    """P/E"""
    try:
        ticker = si.get_quote_table(share)['PE Ratio (TTM)']
        if ticker == '' or pd.isnull(ticker):
            ticker = 0
        return ticker
    except:
        return 0


def get_momentum(share):
    """Momentum_12_1"""
    ticker = yf.Ticker(share)
    ticker = ticker.history(start=start_time, end=month_ago, interval="1mo")
    ticker = ticker[ticker["Close"].notna()]
    ticker["Price0"] = ticker["Close"].shift(12)
    ticker["Price1"] = ticker["Close"]
    ticker["mom_12"] = (ticker["Price1"] / ticker["Price0"]) - 1
    return round(ticker["mom_12"][-1], 2)


def get_10ma(share):
    """Last close price compare to MA10, 1 = close price higher than MA10"""
    ticker = yf.Ticker(share)
    ticker = ticker.history(start=start_time, end=month_ago, interval="1mo")
    ticker = ticker[ticker["Close"].notna()]
    ticker["MA10"] = ticker["Close"].rolling(10).mean()
    ticker["Difference"] = (ticker["Close"] / ticker["MA10"]) - 1
    ticker["Direction"] = [1 if ticker.loc[ei, "Difference"] > 0 else -1 for ei in ticker.index]
    result = ticker["Direction"][-1]
    return float(result)


def get_mom_12_2(share):
    """Get Momentum_12_2"""
    try:
        ticker = si.get_data(f"{share}", start_date =start_time, end_date = month_ago, interval = '1mo')
        ticker = ticker[ticker["close"].notna()]
        ticker["Price0"] = ticker["close"].shift(12)
        ticker["Price1"] = ticker["close"].shift(1)
        ticker["mom_12_1"] = (ticker["Price1"] / ticker["Price0"]) - 1
        return (round(ticker["mom_12_1"][-1], 2))
    except:
        return 0


def get_div(share):
    """Dividend average for last 5 years / last close price"""
    try:
        div = si.get_dividends(share)[-20:].mean()
        div_income = (div * 4) / get_close_price(share)
        if  len(div_income) < 1:
            div_income = 0
        return round(div_income[0], 3)
    except:
        return 0


def get_avg_momentum(share):
    """Get AVG Momentum(12, 6, 3)"""
    ticker = yf.Ticker(share)
    ticker = ticker.history(start=start_time, end=month_ago, interval="1mo")
    ticker = ticker[ticker["Close"].notna()]
    ticker['Close0'] = ticker['Close'].shift(12)
    ticker['Close1'] = ticker['Close'].shift(6)
    ticker['Close2'] = ticker['Close'].shift(3)
    ticker['Mom_0'] = ((ticker['Close'] / ticker['Close0']) - 1) * 0.33
    ticker['Mom_1'] = ((ticker['Close'] / ticker['Close1']) - 1) * 0.33
    ticker['Mom_2'] = ((ticker['Close'] / ticker['Close2']) - 1) * 0.33
    ticker['Avg_Mom'] = ticker['Mom_0'] + ticker['Mom_1'] + ticker['Mom_2']
    return round(ticker['Avg_Mom'][-1], 2)
