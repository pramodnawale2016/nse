
source venv/bin/activate

python3.9 trade.py 

docker build -t my-nse-code-image . 

docker run -it -p 5000:5000 my-nse-code-image 

http://127.0.0.1:5000/crude/sma/20/close/hours 

git hub personal token for code checkin - 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
username - pramodnawale2016

http://127.0.0.1:5000/nifty?instrument_token=10930434&fut_name=NIFTY23JULFUT
