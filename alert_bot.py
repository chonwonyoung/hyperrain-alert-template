import os
import time
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, COINS
from strategy_rsi import RSI_Strategy
from strategy_consolidation_breakout import ConsolidationBreakoutStrategy
from upbit_api import get_ohlcv
import requests

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[ERROR] 텔레그램 전송 실패: {e}")

def monitor():
    while True:
        for coin in COINS:
            try:
                symbol = f"KRW-{coin}"

                # 전략 1: RSI 전략
                rsi_bot = RSI_Strategy(
                    api_key="", secret_key="", symbol=coin,
                    period=14, upper=70, lower=30
                )
                rsi_signal = rsi_bot.check_signal()
                if rsi_signal:
                    send_telegram_message(rsi_signal)

                # 전략 2: 수렴 돌파 전략
                df = get_ohlcv(symbol)
                if df is not None:
                    prices = df['close'].tolist()
                    breakout_bot = ConsolidationBreakoutStrategy(
                        symbol=coin, threshold=0.02
                    )
                    breakout_signal = breakout_bot.check_signal(prices)
                    if breakout_signal:
                        send_telegram_message(breakout_signal)

            except Exception as e:
                print(f"[ERROR] {coin} 감시 중 오류 발생: {e}")

        time.sleep(60)

if __name__ == "__main__":
    send_telegram_message("📡 하이퍼레인 자동 감시 시스템 시작됨.")
    monitor()

