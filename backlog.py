import pyupbit
import numpy as np
import datetime
from config import coin


ticker = "KRW-" + coin


def get_current_price(ticker):
    """Returns the current price of a ticker"""
    orderbook = pyupbit.get_orderbook(ticker=ticker)
    ask_price = orderbook["orderbook_units"][0]["ask_price"]
    return ask_price


def get_moving_average(ticker, days):
    """Returns the moving average of a ticker for a given number of days"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=days)
    ma = df["close"].rolling(days).mean().iloc[-1]
    return ma


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


ma1 = get_moving_average(ticker, 1)
ma15 = get_moving_average(ticker, 15)
ma20 = get_moving_average(ticker, 20)
ma30 = get_moving_average(ticker, 30)
current_price = get_current_price(ticker)

print(f"1-day moving average: {ma1}")
print(f"15-day moving average: {ma15}")
print(f"20-day moving average: {ma20}")
print(f"30-day moving average: {ma30}")
print(f"Current price: {current_price}")
print(get_start_time(ticker))


data = [
    get_moving_average(ticker, 1),
    get_moving_average(ticker, 15),
    get_moving_average(ticker, 20),
    get_moving_average(ticker, 30),
]
min_target_price = min(data)
max_target_price = max(data)
print((max_target_price - min_target_price) / min_target_price)
