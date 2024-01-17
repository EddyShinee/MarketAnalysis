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
def calculate_emas(data):
    """Calculates exponential moving averages."""
    data['EMA3'] = data['Close'].ewm(span=3, min_periods=2).mean()
    data['EMA30'] = data['Close'].ewm(span=30, min_periods=2).mean()
    data['EMA60'] = data['Close'].ewm(span=60, min_periods=2).mean()

def generate_buy_sell_signals_based_on_emas(data):
    """Generates buy/sell signals based on EMAs."""
    data['Signal'] = np.where((data['Close'] > data['EMA60']) & (data['Close'].shift(1) < data['EMA60'].shift(1)), 'Buy',
                    np.where((data['Close'] < data['EMA3']) & (data['Close'].shift(1) > data['EMA3'].shift(1)), 'Sell', 'Hold'))

def calculate_and_detect_ema_signals(data):
    """Calculates indicators and generates EMA-based signals."""
    calculate_kama(data, 3)
    calculate_emas(data)
    generate_buy_sell_signals_based_on_emas(data)
    return data