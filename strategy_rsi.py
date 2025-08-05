import requests

class RSI_Strategy:
    def __init__(self, api_key, secret_key, symbol="KRW-BTC", period=14, upper=70, lower=30):
        self.symbol = symbol
        self.period = period
        self.upper = upper
        self.lower = lower

    def get_ohlcv(self):
        url = f"https://api.upbit.com/v1/candles/minutes/1?market={self.symbol}&count={self.period + 1}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def calc_rsi(self, closes):
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        ups = [d for d in deltas if d > 0]
        downs = [-d for d in deltas if d < 0]
        avg_up = sum(ups)/self.period
        avg_down = sum(downs)/self.period
        rs = avg_up / (avg_down or 1)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def check_signal(self):
        data = self.get_ohlcv()
        closes = [candle['trade_price'] for candle in reversed(data)]
        rsi = self.calc_rsi(closes)
        if rsi > self.upper:
            return f"{self.symbol} overbought (RSI {rsi:.2f})"
        if rsi < self.lower:
            return f"{self.symbol} oversold (RSI {rsi:.2f})"
        return None
