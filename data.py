import yfinance as yf

def fetch_data(ticker: str):
    yf.download(ticker, period='1y').to_csv(f"./data/{ticker}.csv")