import time
import pyupbit
from datetime import datetime, timedelta, timezone
import requests
from config import *
from backlog import *

m1 = get_moving_average(ticker, 1)
m15 = get_moving_average(ticker, 15)
m30 = get_moving_average(ticker, 30)
m7 = get_moving_average(ticker, 7)
current = get_current_price(ticker)

print("현재가 : " + str(current))
print("m1 : " + str(m1))
print("m7 : " + str(m7))
print("m15 : " + str(m15))
print("m30 :" + str(m30))
