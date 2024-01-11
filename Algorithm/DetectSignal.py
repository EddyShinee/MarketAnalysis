import numpy as np
import pandas as pd

# from Algorithm.HeikenAshi import calculate_and_detect_ha_signal
from Algorithm.HeikenAshi import calculate_and_detect_ha_signal
from Algorithm.MACD import calculate_and_detect_macd_signal
from Algorithm.RSI import calculate_and_detect_rsi
from Common.Utils.GlobalConfig import ALLOW_ONCE_TIME_ORDER
from Common.Utils.Redis import redis_manager


def detect_signal(symbol, data):
    macd_signal = calculate_and_detect_macd_signal(data)
    ha_signal = calculate_and_detect_ha_signal(data)
    # bb_signal = calculate_and_detect_bollinger_bands(data)
    rsi_signal = calculate_and_detect_rsi(data)

    pd.set_option('display.max_columns', None)
    # print(bb_signal)
    # print(ha_signal['Signal'])
    # print(bb_signal['Signal'])
    # print(rsi_signal['Signal'])
    detect = pd.DataFrame()
    # detect['HA_Signal'] = ha_signal['Signal']
    # detect['HA_Trend'] = ha_signal['Trend']
    detect['HA_Signal'] = ha_signal['Signal']
    detect['MACD_Signal'] = macd_signal['Signal']
    # detect['BB_Signal'] = bb_signal['Signal']
    detect['RSI_Signal'] = rsi_signal['Signal']
    transposed_data = detect.T

    for column, values in transposed_data.items():
        print(f'{column}: {values.tolist()}')
    # print(vertical_df)

    # data['Sell_Signal'] = ((ha_signal['Signal'] == 'Buy') &
    #                        (ha_signal['Trend'] == 'Upward') &
    #                        (ha_signal['Strength'] == 'Changing') &
    #                        (macd_signal['Signal'] == 'Buy')
                           # (bb_signal['Signal'] == 'Buy') &
                           # (rsi_signal['Signal'] == 'Buy')
                           # )
    # data['Buy_Signal'] = ((ha_signal['Signal'] == 'Sell') &
    #                       (ha_signal['Trend'] == 'Downward') &
    #                       (ha_signal['Strength'] == 'Changing') &
    #                       (macd_signal['Signal'] == 'Sell')
                          # (bb_signal['Signal'] == 'Sell') &
                          # (rsi_signal['Signal'] == 'Sell')
                          # )

    data['Buy_Signal'] = ((macd_signal['Signal'] == 'Buy')
                          & (ha_signal['Signal'] == 'Buy')
                          & (rsi_signal['Signal'] == 'Sell'))

    data['Sell_Signal'] = ((macd_signal['Signal'] == 'Sell')
                           & (ha_signal['Signal'] == 'Sell')
                           & (rsi_signal['Signal'] == 'Buy'))



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
