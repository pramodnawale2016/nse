from flask import Flask, render_template
from kite_trade import *
enctoken = "uyrBj8PojY6ZVEXXjrV8XyBPndQKUpOW+CdPwqF2CxGJDpCUIvTvctkBlaaP5nqdIi+9WXHeIu51bAz8vGTlwpuGlox0TvWAMfxlPMjqhA2DI+aa/6FJMw=="
kite = KiteApp(enctoken=enctoken)

import pandas as pd
    
# Get Historical Data to find out BANKNIFTY Open 
import datetime, time
app = Flask(__name__)

crude_pnl = []
crude_buy_at = 0
crude_sell_at=0
c_pnl = 0

@app.route('/')
def hello_world():
    return render_template("crude.html", data=crude_pnl)

@app.route('/crude/sma/20/close/hours')
def SMA(instrument_token = 63634951, length=5):
    from_datetime = datetime.datetime.now() - datetime.timedelta(minutes=length)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "minutes"
    data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)
    df = pd.DataFrame(data)
    print(df)
    return str(df['close'].mean())

@app.route('/crude')
def crude_SMA(instrument_token = 63634951, length=5):
    global crude_buy_at, crude_sell_at,c_pnl
    from_datetime = datetime.datetime.now() - datetime.timedelta(minutes=length)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "minute"
    data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)
    df = pd.DataFrame(data)
    high = df['high'].mean()
    close = kite.ltp(["MCX:CRUDEOIL23APRFUT"])["MCX:CRUDEOIL23APRFUT"]['last_price']
    low = df['low'].mean()
    print(high,close,low)
    if close > high:
        if crude_buy_at == 0:
            crude_buy_at = close
            crude_sell_at = 0
            crude_pnl.append(c_pnl)
        else:
            print("BUY at " +  str(crude_buy_at))  
    if close < low:
        if crude_sell_at == 0:
            crude_sell_at = close
            crude_buy_at = 0
            crude_pnl.append(c_pnl)
        else:
            print("SELL at " +  str(crude_sell_at))  
    if crude_buy_at != 0:
        c_pnl = (close-crude_buy_at)*100
        print("CRUDE Running PnL on LONG => "+str(c_pnl))    
    if crude_sell_at != 0:
        c_pnl = (crude_sell_at-close)*100
        print("CRUDE Running PnL on SHORT => "+str(c_pnl))      
    print("CRUDE POSITION="+str(sum(crude_pnl)))