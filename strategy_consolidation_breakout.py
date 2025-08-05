import requests

class ConsolidationBreakoutStrategy:
    def __init__(self, api_key, secret_key, symbol="KRW-BTC", period=20, threshold=0.02):
        self.symbol = symbol
        self.period = period
        self.threshold = threshold

    def get_ohlcv(self):
        url = f"https://api.upbit.com/v1/candles/minutes/1?market={self.symbol}&count={self.period}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def detect_consolidation_breakout(self):
        data = self.get_ohlcv()
        prices = [candle['trade_price'] for candle in reversed(data)]

        high = max(prices)
        low = min(prices)
        range_ratio = (high - low) / low

        if range_ratio < self.threshold:
            return f"{self.symbol} ⚠️ 가격 수렴 구간 감지됨 (Range: {range_ratio:.2%})"
        elif prices[-1] > high:
            return f"{self.symbol} 🚀 상단 돌파 감지 (현재가: {prices[-1]}, 저항: {high})"
        elif prices[-1] < low:
            return f"{self.symbol} ⛔ 하단 이탈 감지 (현재가: {prices[-1]}, 지지: {low})"
        else:
            return None
