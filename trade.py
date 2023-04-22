
from kite_trade import *
# # First Way to Login
# # You can use your Kite app in mobile
# # But You can't login anywhere in 'kite.zerodha.com' website else this session will disconnected

# user_id = "YD1838"       # Login Id
# password = "XXXXXXXX"      # Login password
# # Second way is provide 'enctoken' manually from 'kite.zerodha.com' website
# # Than you can use login window of 'kite.zerodha.com' website Just don't logout from that window
# # # Process shared on YouTube 'TradeViaPython'

enctoken = "YL6uUcoOs/RhQuv964luiQwPF1tFWAZsoYtiTz/YSB30YVyLsd/cbdQnhueqwl53RPUJrNLr0mk0dfPNritVlZBaIxYa34VcAcxursRhgUoNBuD/dTlqQQ=="
kite = KiteApp(enctoken=enctoken)

import pandas as pd
    
# Get Historical Data to find out BANKNIFTY Open 
import datetime, time
instrument_token = 9685250
from_datetime = datetime.datetime.now() - datetime.timedelta(days=3)     # From last & days
to_datetime = datetime.datetime.now()
interval = "day"
data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

# Custom values - YOU can update values for day_open,  default is data[0]['open']
day_open = data[0]['open']
strike_diff = 00 
timeframe = 5

strike = round(day_open/100)*100
CALL_STRIKE = strike + strike_diff
PUT_STRIKE = strike - strike_diff
expiry = "23323" #2022 Oct 20
trade_count = 1
ce_order = None
pe_order = None
total = 0
PNL = 0
end_time = datetime.datetime(2022, 10, 20, 15, 20)
# print(kite.ltp(["NFO:BANKNIFTY"+expiry+"40100CE"])["NFO:BANKNIFTY"+expiry+"40100CE"]['last_price'])
print(kite.ltp(["MCX:CRUDEOIL23APRFUT"])["MCX:CRUDEOIL23APRFUT"]['last_price'])

crude_pnl = []
crude_buy_at = 0
crude_sell_at=0
c_pnl = 0
def SMA(instrument_token = 63634951, length=5):
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

nifty_pnl = []
nifty_buy_at = 0
nifty_sell_at=0
n_pnl = 0
def Nifty_SMA(instrument_token = 9685506, length=5):
    global nifty_buy_at, nifty_sell_at,n_pnl
    from_datetime = datetime.datetime.now() - datetime.timedelta(minutes=length)     # From last & days
    to_datetime = datetime.datetime.now()
    interval = "minute"
    data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)
    df = pd.DataFrame(data)
    high = df['high'].mean()
    close = kite.ltp(["NFO:NIFTY29APRFUT"])["NFO:NIFTY29APRFUT"]['last_price']
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
            # kite.place_order(variety=kite.VARIETY_REGULAR,
            #                 exchange=kite.EXCHANGE_NFO,
            #                 tradingsymbol="NIFTY23MARFUT",
            #                 transaction_type="BUY",
            #                 quantity=50,
            #                 product=kite.PRODUCT_NRML,
            #                 order_type=kite.ORDER_TYPE_MARKET,
            #                 price=None,
            #                 validity=None,
            #                 disclosed_quantity=None,
            #                 trigger_price=None,
            #                 squareoff=None,
            #                 stoploss=None,
            #                 trailing_stoploss=None,
            #                 tag="TradeViaPramodCode")
    if close < low:
        print("\a")
        if nifty_sell_at == 0:
            nifty_sell_at = close
            nifty_buy_at = 0
            nifty_pnl.append(n_pnl)
        else:
            print("SELL at " +  str(nifty_sell_at))  
            # kite.place_order(variety=kite.VARIETY_REGULAR,
            #                 exchange=kite.EXCHANGE_NFO,
            #                 tradingsymbol="NIFTY23MARFUT",
            #                 transaction_type="SELL",
            #                 quantity=50,
            #                 product=kite.PRODUCT_NRML,
            #                 order_type=kite.ORDER_TYPE_MARKET,
            #                 price=None,
            #                 validity=None,
            #                 disclosed_quantity=None,
            #                 trigger_price=None,
            #                 squareoff=None,
            #                 stoploss=None,
            #                 trailing_stoploss=None,
            #                 tag="TradeViaPramodCode")
    if nifty_buy_at != 0:
        n_pnl = (close-nifty_buy_at)*50
        print("Nifty Running PnL on LONG => "+str(n_pnl))    
    if nifty_sell_at != 0:
        n_pnl = (nifty_sell_at-close)*50
        print("Nifty Running PnL on SHORT => "+str(n_pnl))      
    print("NIFTY POSITION="+str(sum(nifty_pnl)))

while True:
    print('\n**************CRUDE*************\n')
    SMA()
    # print('\n**************NIFTY*************\n')
    # Nifty_SMA()
    print("\n\n"+str(datetime.datetime.now())+"  "+str(crude_pnl))
    time.sleep(10)

def PLACE_ORDER(strike,PE_or_CE, Buy_or_Sell):
    quantity = 25 * trade_count
    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                            exchange=kite.EXCHANGE_NFO,
                            tradingsymbol="BANKNIFTY" + expiry + str(strike) + PE_or_CE,
                            transaction_type=Buy_or_Sell,
                            quantity=quantity,
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
    return order
while True:
    current_price = kite.ltp(["NFO:BANKNIFTY23MARFUT"])["NFO:BANKNIFTY23MARFUT"]['last_price']
    print("BN future CMP:"+str(current_price))
    if day_open < current_price:
        # Place CALL Order
        if pe_order:
            # PLACE_ORDER(PUT_STRIKE, "PE", kite.TRANSACTION_TYPE_SELL)
            print(str(PUT_STRIKE)+" PE Exited Time :"+str(datetime.datetime.now()))
            exit = kite.ltp(["NFO:BANKNIFTY" + expiry +str(PUT_STRIKE)+"PE"])["NFO:BANKNIFTY" + expiry +str(PUT_STRIKE)+"PE"]['last_price']
            pe_order = None
        if ce_order is None:
            # ce_order = PLACE_ORDER(CALL_STRIKE, "CE", kite.TRANSACTION_TYPE_BUY)
            print(str(CALL_STRIKE)+" CE Entered Time :"+str(datetime.datetime.now()))
            entry = kite.ltp(["NFO:BANKNIFTY" + expiry +str(CALL_STRIKE)+"CE"])["NFO:BANKNIFTY" + expiry +str(CALL_STRIKE)+"CE"]['last_price']
            trade_count = trade_count + 1
            total = total + PNL
    else:
        # Place PUT Order
        if ce_order:
            # order = PLACE_ORDER(CALL_STRIKE, "CE", kite.TRANSACTION_TYPE_SELL)
            print(str(CALL_STRIKE)+" CE Exited Time :"+str(datetime.datetime.now()))
            exit = kite.ltp(["NFO:BANKNIFTY" + expiry +str(CALL_STRIKE)+"CE"])["NFO:BANKNIFTY" + expiry +str(CALL_STRIKE)+"CE"]['last_price']
            ce_order = None
        if pe_order is None:
            # pe_order = PLACE_ORDER(PUT_STRIKE, "PE", kite.TRANSACTION_TYPE_BUY)
            print(str(PUT_STRIKE)+" PE Entered Time :"+str(datetime.datetime.now()))
            entry = kite.ltp(["NFO:BANKNIFTY" + expiry +str(PUT_STRIKE)+"PE"])["NFO:BANKNIFTY" + expiry +str(PUT_STRIKE)+"PE"]['last_price']
            trade_count = trade_count + 1
            total = total + PNL
   # print(pd.DataFrame(kite.positions()))
    if pe_order:
        PNL = kite.ltp(["NFO:BANKNIFTY" + expiry +str(PUT_STRIKE)+"PE"])["NFO:BANKNIFTY" + expiry +str(PUT_STRIKE)+"PE"]['last_price'] - entry
    if ce_order:
        PNL = kite.ltp(["NFO:BANKNIFTY" + expiry +str(CALL_STRIKE)+"CE"])["NFO:BANKNIFTY" + expiry +str(CALL_STRIKE)+"CE"]['last_price'] - entry
    print("profit= "+str(round(PNL*(trade_count-1)*25)), "Qty= "+str(trade_count-1), "Total= "+str(round(total)))
    if datetime.datetime.now()>end_time:
        break
    time.sleep(60*timeframe) #Sleep for one minute
    # break



# import pandas as pd
# df = pd.DataFrame(data)
# import os  
# os.makedirs('folder/subfolder', exist_ok=True)  
# df.to_csv('folder/subfolder/out.csv')  
# print(df)

# Place Order
# order = kite.place_order(variety=kite.VARIETY_REGULAR,
#                          exchange=kite.EXCHANGE_NSE,
#                          tradingsymbol="ACC",
#                          transaction_type=kite.TRANSACTION_TYPE_BUY,
#                          quantity=100,
#                          product=kite.PRODUCT_MIS,
#                          order_type=kite.ORDER_TYPE_MARKET,
#                          price=None,
#                          validity=None,
#                          disclosed_quantity=None,
#                          trigger_price=None,
#                          squareoff=None,
#                          stoploss=None,
#                          trailing_stoploss=None,
#                          tag="TradeViaPython")

# print(order)