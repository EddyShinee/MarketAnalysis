import numpy as np
import pandas as pd

def calculate_kama(data, length, fastend=0.666, slowend=0.0645, efratio=1.0):
    smooth = (efratio * (fastend - slowend) + slowend) ** 2  # Định nghĩa smooth
    close = data['Close']
    kama_values = close.copy()

    # Cắt giảm kích thước `kama_values` nếu cần thiết
    if len(kama_values) > len(close):
        kama_values = kama_values[:len(close)]

    # Tính toán KAMA
    for i in range(1, len(data)):
        kama_values[i] = kama_values[i - 1] + smooth * (close[i] - kama_values[i - 1])
    data['KAMA'] = kama_values
    return data

def calculate_heiken_ashi(data, p):
    """Calculates Heiken Ashi candles."""
    data[['HA_Open', 'HA_High', 'HA_Low', 'HA_Close']] = (
        data[['Open', 'High', 'Low', 'Close']].rolling(p).mean().shift(1)
    )
def calculate_emas(data):
    """Calculates exponential moving averages."""
    data['EMA3'] = data['Close'].ewm(span=3, min_periods=2).mean()
    data['EMA30'] = data['Close'].ewm(span=30, min_periods=2).mean()
    data['EMA60'] = data['Close'].ewm(span=60, min_periods=2).mean()


def generate_buy_sell_signals(data):
    """Generates buy/sell signals based on Heiken Ashi and EMAs."""
    data['Signal'] = np.where((data['HA_Low'] < data['EMA60']) & (data['HA_Low'].shift(1) > data['EMA60'].shift(1)), 'Buy',
                              np.where((data['Close'] < data['EMA3']) & (data['Close'].shift(1) > data['EMA3'].shift(1)), 'Sell', 'Hold'))

def calculate_and_detect_ha_signal(data):
    """Calculates indicators and generates signals."""
    calculate_kama(data, 3)
    calculate_heiken_ashi(data, 3)
    calculate_emas(data)
    generate_buy_sell_signals(data)
    return data
