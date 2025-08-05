import os
from strategy_rsi import RSI_Strategy
from strategy_consolidation_breakout import ConsolidationBreakoutStrategy
from telegram_utils import send_telegram_message
from dotenv import load_dotenv

load_dotenv()

def main():
    # 환경 변수
    UPBIT_API_KEY = os.getenv("UPBIT_API_KEY")
    UPBIT_SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # 전략 초기화
    rsi = RSI_Strategy(api_key=UPBIT_API_KEY, secret_key=UPBIT_SECRET_KEY)
    cb = ConsolidationBreakoutStrategy(api_key=UPBIT_API_KEY, secret_key=UPBIT_SECRET_KEY)

    # 루프 실행 (예: WebSocket 또는 폴링)
    while True:
        rsi_signal = rsi.check_signal()
        if rsi_signal:
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, f"RSI Signal: {rsi_signal}")

        cb_signal = cb.check_signal()
        if cb_signal:
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, f"Breakout Signal: {cb_signal}")

if __name__ == "__main__":
    main()
