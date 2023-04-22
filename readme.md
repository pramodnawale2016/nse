
source venv/bin/activate

python3.9 trade.py 

docker build -t my-nse-code . 
docker run -it -p 5000:5000 my-nse-code 
http://127.0.0.1:5000/crude/sma/20/close/hours 
