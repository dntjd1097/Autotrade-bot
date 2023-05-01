import pyupbit
from config import coin


ticker = "KRW-" + coin


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


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


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
