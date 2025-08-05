import pyupbit

def get_current_price(symbol):
    try:
        price = pyupbit.get_current_price(symbol)
        return price
    except Exception as e:
        print(f"[ERROR] 현재가 조회 실패: {e}")
        return None

def get_ohlcv(symbol, interval="minute1", count=200):
    try:
        df = pyupbit.get_ohlcv(symbol, interval=interval, count=count)
        return df
    except Exception as e:
        print(f"[ERROR] OHLCV 조회 실패: {e}")
        return None

def get_balance(access_key, secret_key):
    try:
        upbit = pyupbit.Upbit(access_key, secret_key)
        balances = upbit.get_balances()
        return balances
    except Exception as e:
        print(f"[ERROR] 잔고 조회 실패: {e}")
        return None
