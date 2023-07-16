
import yfinance as yf

def main():
    ticker = yf.Ticker('MSFT')
    ticker.history(interval="1d")["Close"].iloc[-1]
    print(round(ticker.history(interval="1d")["Close"].iloc[-1], 2))



if __name__ == '__main__':
    main()