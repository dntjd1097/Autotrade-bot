import time
import pyupbit
from datetime import datetime, timedelta, timezone
import requests
from config import *
from backlog import *


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )


def get_balance():
    now = datetime.now()
    # post_message(myToken, "#coin_balance", "현재시간 : " + str(now) + "\n")
    """잔고 조회"""
    balances = upbit.get_balances()
    # print(balances)
    global krw, BTC_balance, BTC_current, avg_buy_price, BTC_avg_buy_price, count
    BTC_balance = 0

    for b in balances:
        if b["currency"] is not None:
            a_ticker = b["currency"]
            count = float(b["balance"])  # 보유 수량
            if a_ticker == "KRW":
                krw = count
                count = int(count)

            else:
                avg_buy_price = int(float(b["avg_buy_price"]))  # 매수 평균가
                symbol = str("KRW-" + a_ticker)
                current_price = int(get_current_price(symbol))
                total_price = int(current_price * count)  # 평가금액
                sum = int(avg_buy_price * count)  # 매수금액
                profit = round(((total_price - sum) / sum) * 100, 2)  # 수익률
                diff = int((current_price - avg_buy_price) * count)  # 평가손익
                if a_ticker == "BTC":
                    BTC_avg_buy_price = avg_buy_price
                    BTC_balance = count
                    BTC_current = current_price

    return 0


def get_balances_krw():
    post_message(
        myToken,
        "#coin_balance",
        "\n[" + "보유현금 : " + format(count, ",") + "KRW]",
    )


def get_balances_coin():
    post_message(
        myToken,
        "#coin_balance",
        "\n["
        + a_ticker
        + "]"
        + "\n평가손익"
        + str(diff)
        + "    수익률 :"
        + str(profit)
        + " %"
        + "\n보유수량 : "
        + str(count)
        + " "
        + str(a_ticker)
        + "     \n매수평균가 : "
        + format(avg_buy_price, ",")
        + " KRW"
        + "\n평가금액 : "
        + format(total_price, ",")
        + " KRW"
        + "     \n매수금액 :"
        + format(sum, ",")
        + " KRW",
    )
    post_message(myToken, "#coin_balance", "\n==================================")


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
"""시작 메세지 슬랙 전송"""
now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
post_message(
    myToken,
    "#coin",
    "현재시간 : " + str(now) + "\n프로그램시작\n\n==================================",
)


while True:
    try:
        now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

        start_time = get_start_time("KRW-BTC")
        end_time = start_time + timedelta(seconds=120)
        get_balance()
        if start_time < now < end_time:
            current_price = get_current_price("KRW-BTC")
            ma1 = get_moving_average(ticker, 1)
            ma15 = get_moving_average(ticker, 15)
            ma20 = get_moving_average(ticker, 20)
            ma30 = get_moving_average(ticker, 30)
            data = [
                get_moving_average(ticker, 1),
                get_moving_average(ticker, 15),
                get_moving_average(ticker, 20),
                get_moving_average(ticker, 30),
            ]
            min_target_price = min(data)
            max_target_price = max(data)
            check_buy = current_price < min_target_price
            check_sell = current_price > max_target_price
            post_message(
                myToken,
                "#coin",
                "*"
                + coin
                + "*\n *현재가* : "
                + str(int(current_price))
                + "\n 구매해야됨 :"
                + str(check_buy)
                + " ["
                + str(int(min_target_price))
                + "]"
                + "\n 판매해야됨 :"
                + str(check_sell)
                + " ["
                + str(int(max_target_price))
                + "]",
            )
            # check1 = target_price > current_price
            # check2 = ma15 > current_price
            # check3 = "X"
            # if check1 and check2:
            #     check3 = "O"

            # if check1:
            #     check3 = "O"
            #     mark = "▼"
            #     # mark1=""
            #     mark1 = ""
            #     required = " X "
            #     # required=format(int(target_price)-int(current_price), ",")

            # else:
            #     # mark = "▼"
            #     mark = "▲"
            #     mark1 = "▼"
            #     # mark1 = "▲"

            #     required = ""
            #     required = format(int(current_price) - int(target_price), ",")

            # format(,",")
            # post_message(
            #     myToken,
            #     "#coin_test",
            #     "현재시간 : "
            #     + str(now)
            #     + "\nBTC target_price : "
            #     + format(int(target_price), ",")
            #     + "\nBTC ma15 : "
            #     + format(int(ma15), ",")
            #     + "\nBTC current_price : "
            #     + format(int(current_price), ",")
            #     + "  "
            #     + str(mark)
            #     + "\n"
            #     + str(check3)
            #     + "   [required ="
            #     + required
            #     + mark1
            #     + "  ]",
            # )

            if check_buy:  # and check2:
                if krw > 5000:
                    post_message(
                        myToken,
                        "#coin_test",
                        "\n 구매시작 " + "\n==================================",
                    )
                    buy_result = upbit.buy_market_order(ticker, krw * 0.9995)
                    post_message(
                        myToken, "#coin", "\n" + coin + " buy : " + str(buy_result)
                    )
                    get_balances_coin()

            if BTC_balance > 0.00008:
                if check_sell:
                    fee = BTC_avg_buy_price / (1 + comission)
                    if fee < current_price:
                        sell_result = upbit.sell_market_order(ticker, BTC_balance)
                        post_message(
                            myToken,
                            "#coin",
                            "\n" + coin + " sell : " + str(sell_result),
                        )
                        post_message(
                            myToken,
                            "#coin_reward",
                            "현재시간 : "
                            + str(now)
                            + "\n[보유현금 : "
                            + format(krw, ",")
                            + "krw ]"
                            + "\n==================================",
                        )
                        get_balances_krw()
            # elif fee < current_price:
            #    post_message(myToken,"#coin_test",
            #    "매도 X : required(" +str(current_price-fee)+
            #    " ▲ )"
            #    )

            time.sleep(120)
    except Exception as e:
        print(e)
        post_message(myToken, "#coin_error", e)
        time.sleep(1)
# get_balance()
