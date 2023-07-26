from flask import Flask, request, render_template
from kite_trade import *
enctoken = "kTrOQHHzFPS3bo3H7B/zbcUp8y1JC6iez+DHwsco0WDKI0pvhYzO3/NuquZtAmOha/XBtOE3O8tkvYYiavLe2H64RXvJTSixmv/FtVXrIp8GjExcRN9ITQ=="
kite = KiteApp(enctoken=enctoken)

import pandas as pd
    
# Get Historical Data to find out BANKNIFTY Open 
import datetime, time
app = Flask(__name__)

crude_pnl = []
crude_buy_at = 0
crude_sell_at=0
c_pnl = 0
nifty_pnl = []
nifty_buy_at = 0
nifty_sell_at=0
n_pnl = 0

def Nifty_SMA(kite = kite, instrument_token = 10930434, fut_name="NIFTY23JULFUT", length=5):
    global nifty_buy_at, nifty_sell_at,n_pnl
    from_datetime = datetime.datetime.now() - datetime.timedelta(minutes=length)     
    to_datetime = datetime.datetime.now()
    interval = "minute"
    data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)
    df = pd.DataFrame(data)
    high = df['high'].mean()
    close = kite.ltp(["NFO:"+fut_name])["NFO:"+fut_name]['last_price']
    low = df['low'].mean()
    print(round(high,2),round(close,2),round(low,2))
    if close > high:
        print("\a")
        if nifty_buy_at == 0:
            nifty_buy_at = close
            nifty_sell_at = 0
            nifty_pnl.append(n_pnl)
        else:
            print("BUY at " +  str(nifty_buy_at))  
            kite.place_order(variety=kite.VARIETY_REGULAR,
                            exchange=kite.EXCHANGE_NFO,
                            tradingsymbol=fut_name,
                            transaction_type="BUY",
                            quantity=50,
                            product=kite.PRODUCT_NRML,
                            order_type=kite.ORDER_TYPE_MARKET,
                            price=None,
                            validity=None,
                            disclosed_quantity=None,
                            trigger_price=None,
                            squareoff=None,
                            stoploss=None,
                            trailing_stoploss=None,
                            tag="TradeViaPramodCode")
    if close < low:
        print("\a")
        if nifty_sell_at == 0:
            nifty_sell_at = close
            nifty_buy_at = 0
            nifty_pnl.append(n_pnl)
        else:
            print("SELL at " +  str(nifty_sell_at))  
            kite.place_order(variety=kite.VARIETY_REGULAR,
                            exchange=kite.EXCHANGE_NFO,
                            tradingsymbol=fut_name,
                            transaction_type="SELL",
                            quantity=50,
                            product=kite.PRODUCT_NRML,
                            order_type=kite.ORDER_TYPE_MARKET,
                            price=None,
                            validity=None,
                            disclosed_quantity=None,
                            trigger_price=None,
                            squareoff=None,
                            stoploss=None,
                            trailing_stoploss=None,
                            tag="TradeViaPramodCode")
    if nifty_buy_at != 0:
        n_pnl = (close-nifty_buy_at)*50
        print("Nifty Running PnL on LONG => "+str(n_pnl))    
    if nifty_sell_at != 0:
        n_pnl = (nifty_sell_at-close)*50
        print("Nifty Running PnL on SHORT => "+str(n_pnl))      
    print("NIFTY POSITION="+str(sum(nifty_pnl)))

@app.route('/')
def hello_world():
    return render_template("crude.html", data=crude_pnl)

@app.route('/nifty', methods=['GET'])
def call_nifty():
    instrument_token = request.args.get('instrument_token')
    fut_name = request.args.get('fut_name')
    enctoken = request.args.get('enctoken')
    kite = KiteApp(enctoken=enctoken)
    while True:
        Nifty_SMA(kite = kite, instrument_token = instrument_token, fut_name=fut_name)
        time.sleep(10)
    return "exited"     


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
