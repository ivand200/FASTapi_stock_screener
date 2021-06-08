import sqlite3
import json
import csv
from apscheduler.schedulers.blocking import BlockingScheduler
import defs


conn = sqlite3.connect('sql_app.db', check_same_thread=False)
cur = conn.cursor()


def dj30_db():
    """Create DJ30 table, calculate ratios and insert into DB"""
    cur.execute('''DROP TABLE IF EXISTS dj30''')
    cur.execute('''CREATE TABLE dj30 (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        symbol TEXT, name TEXT, avg_momentum REAL, ep REAL)''')
    with open('DJ30.csv', "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            symbol_ = row[1]
            name_ = row[0]
            avg_momentum_ = defs.get_avg_momentum(row[1])
            ep_ = defs.get_ep(row[1])
            cur.execute('''INSERT INTO dj30 (symbol, name, avg_momentum, ep)
                VALUES (?, ?, ?, ?)''', (symbol_, name_, avg_momentum_, ep_))
            conn.commit()
        cur.close()


def sp500_db():
    """Create SP500 table, calculate ratios and insert into DB"""
    cur.execute('''DROP TABLE IF EXISTS sp500''')
    cur.execute('''CREATE TABLE sp500 (id INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE, symbol TEXT, name TEXT, avg_momentum REAL,
        ep REAL)''')
    with open('SP500_components_raw.json', 'r') as f:
        file = f.read()
    data = json.loads(file)
    for item in data:
        symbol_ = item["Symbol"]
        name_ = item["Name"]
        avg_momentum_ = defs.get_avg_momentum(item["Symbol"])
        ep_ = defs.get_ep(item["Symbol"])
        cur.execute('''INSERT INTO sp500 (symbol, name, avg_momentum, ep)
            VALUES (?, ?, ?, ?)''', (symbol_, name_, avg_momentum_, ep_))
        conn.commit()
    cur.close()
sp500_db()

def divs_db():
    """Create divs table, calculate ratios and insert into DB"""
    cur.execute('''DROP TABLE IF EXISTS divs''')
    cur.execute('''CREATE TABLE divs (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        symbol TEXT, name TEXT, div_p REAL)''')
    with open('DJ30.csv', "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            symbol_ = row[1]
            name_ = row[0]
            div_p_ = defs.get_div(row[1])
            cur.execute('''INSERT INTO divs (symbol, name, div_p) VALUES (?, ?, ?)''',
                (symbol_, name_, div_p_))
            conn.commit()
        cur.close()


def etf_db():
    """Create etf table, calculate ratios and insert into DB"""
    cur.execute('''DROP TABLE IF EXISTS etf''')
    cur.execute('''CREATE TABLE etf (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        symbol TEXT, name TEXT, momentum_12_1 REAL, ma10 REAL)''')
    lst = {
        "Dow Jones Industrial Average": "^DJI",
        "iShares Core S&P 500": "IVV",
        "iShares Short Treasury Bond": "SHV",
        "iShares Gold Trust": "IAU",
        "iShares MSCI EAFE": "EFA",
        "iShares Core U.S. Aggregate Bond": "AGG",
        }
    for key, val in lst.items():
        symbol_ = val
        name_ = key
        momentum_ = defs.get_momentum(val)
        ma10_ = defs.get_10ma(val)
        cur.execute('''INSERT INTO etf (symbol, name, momentum_12_1, ma10)
            VALUES (?, ?, ?, ?)''', (symbol_, name_, momentum_, ma10_))
        conn.commit()
    cur.close()


"""
scheduler = BlockingScheduler()
scheduler.add_job(sp500_db, 'interval', days=25, start_date="2020-07-01", end_date="2024-12-30")
scheduler.add_job(dj30_db, 'interval', days=26, start_date="2020-07-02", end_date="2024-12-30")
scheduler.add_job(divs_db, 'interval', days=27, start_date="2020-07-03", end_date="2024-12-30")
scheduler.add_job(etf_db, 'interval', days=28, start_date="2020-07-04", end_date="2024-12-30")
scheduler.start()
"""
