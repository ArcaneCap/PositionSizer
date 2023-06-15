import yfinance as yf
import os
import time

color_codes = {
    "red": "\033[1;31m",
    "white": "\033[0;1m",
    "blue": "\033[1;34m",
    "yellow": "\033[1;33m",
    "green": "\033[1;32m",
    "purple": "\033[1;35m",
    "light": "\033[0;2;3m",
    "reset": "\033[0m"
}

ticker_mapping = {
    "EURUSD": "EURUSD=X",
    "Crude Oil WTI": "CL=F",
    "USDTRY": "USDTRY=X",
    "XAUUSD": "GC=F",
    "BTCUSD": "BTC-USD",
    "Brent Oil": "BZ=F",
    "Natural Gas": "NG=F"
}

def print_mapped_tickers():
    print()
    print(f"{colorChange('blue')}Tickers:{colorChange('reset')}")
    for i, (key, value) in enumerate(ticker_mapping.items(), 1):
        print(f"{i}. {key}: {value}")
    input("Press any button to return home")


def colorChange(color):
    return color_codes.get(color, "")


def clear ():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def get_ticker_price(ticker):
    try:
        ticker_data = yf.Ticker(ticker)
        ticker_price = ticker_data.history(period='1m')['Close'].iloc[-1]
        return ticker_price
    except:
        print(f"Error: Failed to fetch price data for ticker {ticker}.")
        return None

def calculate_position_size(account_size, account_risk, trade_risk):
    calculate_leverage = account_risk / trade_risk
    position_size = account_size * calculate_leverage
    return position_size

def calculate_max_loss(position_size, trade_risk):
    max_loss = position_size * (trade_risk / 100)
    return max_loss

def calculate_ticker_quantity(position_size, ticker_price):
    ticker_quantity = position_size / ticker_price
    return ticker_quantity

def menu():
    print("1. List of Tickers")
    print("2. Risk Calculator\n")
    choice = input(f"{colorChange('light')}Enter 1 or 2{colorChange('reset')} > ")
    time.sleep(3)
    return int(choice)

def intro():
    welcome = "===} Welcome to {==="
    sizer = "PositionSizer"
    subtitle = "An Open-Source basic calculator for Risk and Position Sizing"

    print(f"{colorChange('white')}{welcome:^100}")
    print(f"{colorChange('blue')}{sizer:^100}\n")
    print(f"{colorChange('light')}{subtitle:^100}\n{colorChange('reset')}")
    print("\n\n")

def main():
    clear()
    account_size = int(input("Account size? ($) > "))
    account_risk = int(input("Account risk? (%) > "))
    trade_risk = float(input("Trade risk? (%) > "))
    ticker_input = str(input("Ticker? > "))
    ticker = ticker_mapping.get(ticker_input.upper(), "")
    if not ticker:
        print("Invalid ticker symbol. Please try again.")
        return

    ticker_price = get_ticker_price(ticker)
    if ticker_price is None:
        return

    position_size = calculate_position_size(account_size, account_risk, trade_risk)
    ticker_quantity = calculate_ticker_quantity(position_size, ticker_price)
    max_loss = calculate_max_loss(position_size, trade_risk)

    clear()
    print(f"{colorChange('light')}{ticker}: {round(ticker_price, 4)}{colorChange('reset')}")
    print(f"Quantity: {int(ticker_quantity):,} units")
    print(f"Size: {int(position_size):,}$")
    print(f"Max Loss: {max_loss}$")
    again = input("Again? (Y/N): ")

again = "Y"
while again != "n":
    clear()
    intro()
    choice = menu()
    if choice == 1:
        print_mapped_tickers()

    elif choice == 2:
        main()
        print()
    print("Thanks for using this program!")

