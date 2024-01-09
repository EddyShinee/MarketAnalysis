import numpy as np
import pandas as pd

from Algorithm.HeikenAshi import calculate_and_detect_ha_signal
from Algorithm.MACD import calculate_and_detect_macd_signal
from Algorithm.BB import calculate_and_detect_bollinger_bands
from Common.Utils.GlobalConfig import BARS, ALLOW_ONCE_TIME_ORDER
from Common.Utils.Redis import redis_manager


def detect_signal(symbol, data):
    macd_signal = calculate_and_detect_macd_signal(data)
    ha_signal = calculate_and_detect_ha_signal(data)
    bb_signal = calculate_and_detect_bollinger_bands(data)

    pd.set_option('display.max_columns', None)
    print(ha_signal['Signal'])
    print(bb_signal['Signal'])
    print(macd_signal['Signal'])
    data['Buy_Signal'] = ((ha_signal['Signal'] == 'Buy') &
                          (ha_signal['Trend'] == 'Upward') &
                          (ha_signal['Strength'] == 'Increasing') &
                          (macd_signal['Signal'] == 'Buy') &
                          (bb_signal['Signal'] == 'Buy'))

    data['Sell_Signal'] = ((ha_signal['Signal'] == 'Sell') &
                           (ha_signal['Trend'] == 'Downward') &
                           (ha_signal['Strength'] == 'Increasing') &
                           (macd_signal['Signal'] == 'Sell') &
                           (bb_signal['Signal'] == 'Sell'))

    last_record = data.iloc[-1]
    if (last_record['Buy_Signal'] == True or last_record['Sell_Signal'] == True):
        for field, value in last_record.to_dict().items():
            # Chuyển đổi giá trị uint64 và Timestamp thành chuỗi
            if isinstance(value, pd.Timestamp):
                value = value.isoformat()
            elif isinstance(value, (int, np.uint64)):
                value = str(value)
            SYMBOL_OPENED = symbol + "_IS_OPENED"
            pairsOpened = redis_manager.get_value(SYMBOL_OPENED)
            if ALLOW_ONCE_TIME_ORDER == True and pairsOpened == 'True':
                print(f"Pairs: {symbol} - Opened Order")
                return
            else:
                redis_manager.hset_value(symbol, field, value)
        print(f"Pairs: {symbol} - Trading Signal")
    else:
        print(f"Pairs: {symbol} - No signal")
