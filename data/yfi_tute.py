"""
https://github.com/ranaroussi/yfinance
"""

import yfinance as yf
import datetime
import pandas as pd

bhp = yf.Ticker("BHP.AX")


# get stock info
bhp.info

yf.Ticker("AUDUSD=X").info["regularMarketPrice"]

# get historical market data
hist = bhp.history(period="max")

audusd = yf.Ticker("AUDUSD=X").history(period="max")

audusd.index = audusd.index.tz_convert("UTC").tz_convert(None)
audusd = audusd.sort_index()
audusd["start"] = audusd.index
audusd["end"] = audusd["start"].shift(-1)

dt = datetime.datetime.fromisoformat("2022-01-02 03:02:56")
audusd.query("start < @dt < end").to_dict("records")

# show actions (dividends, splits)
bhp.actions

# show dividends
bhp.dividends

# show splits
bhp.splits

# show financials
bhp.financials
bhp.quarterly_financials

# show major holders
bhp.major_holders

# show institutional holders
bhp.institutional_holders

# show balance sheet
bhp.balance_sheet
bhp.quarterly_balance_sheet

# show cashflow
bhp.cashflow
bhp.quarterly_cashflow

# show earnings
bhp.earnings
bhp.quarterly_earnings

# show sustainability
bhp.sustainability

# show analysts recommendations
bhp.recommendations

# show next event (earnings, etc)
bhp.calendar

# show all earnings dates
bhp.earnings_dates

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
bhp.isin

# show options expirations
bhp.options

# show news
bhp.news

# get option chain for specific expiration
opt = bhp.option_chain("YYYY-MM-DD")
# data available via: opt.calls, opt.puts
