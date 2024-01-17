import numpy as np
import pandas as pd


def calculate_ha_values(df):
    """
    Calculates Heiken Ashi high, low, open, and close values.

    Parameters:
    df (DataFrame): DataFrame with columns 'Open', 'High', 'Low', and 'Close'.

    Returns:
    DataFrame: DataFrame with Heiken Ashi values.
    """
    ha_df = df.copy()

    # Heiken Ashi Close
    ha_df['ha_close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

    # Heiken Ashi Open (initially set to the open price of the first candle)
    ha_df['ha_open'] = ha_df['ha_close'].shift(1)
    ha_df.loc[0, 'ha_open'] = df.loc[0, 'Open']

    for i in range(1, len(df)):
        ha_df.loc[i, 'ha_open'] = (ha_df.loc[i - 1, 'ha_open'] + ha_df.loc[i - 1, 'ha_close']) / 2

    # Heiken Ashi High and Low
    ha_df['ha_high'] = ha_df[['High', 'ha_open', 'ha_close']].max(axis=1)
    ha_df['ha_low'] = ha_df[['Low', 'ha_open', 'ha_close']].min(axis=1)

    return ha_df[['ha_high', 'ha_low', 'ha_open', 'ha_close']]


def calculate_ichimoku_values(close):
    tenkan_sen_periods = 9
    kijun_sen_periods = 24
    senkou_span_b_periods = 51
    displacement = 24

    tenkan_sen = np.roll(np.mean([close, close.shift(1)], axis=0), -tenkan_sen_periods + 1)
    kijun_sen = np.roll(np.mean([close, close.shift(1)], axis=0), -kijun_sen_periods + 1)
    senkou_span_a = (tenkan_sen + kijun_sen) / 2
    senkou_span_b = np.roll(np.mean([close, close.shift(1)], axis=0), -senkou_span_b_periods + 1)
    senkou_span_h = np.maximum(senkou_span_a[displacement - 1], senkou_span_b[displacement - 1])
    senkou_span_l = np.minimum(senkou_span_a[displacement - 1], senkou_span_b[displacement - 1])
    chikou_span = close[displacement - 1]
    ichimoku_df = pd.DataFrame({
        'TenkanSen': tenkan_sen,
        'KijunSen': kijun_sen,
        'SenkouSpanA': senkou_span_a,
        'SenkouSpanB': senkou_span_b,
        'SenkouSpanH': senkou_span_h,
        'SenkouSpanL': senkou_span_l,
        'ChikouSpan': chikou_span
    })

    return ichimoku_df

def calculate_and_detect_heikenashi_ichimoku_signals(data):
    """Calculates Heikin-Ashi, Ichimoku lines, and generates signals."""
    ha_df = calculate_ha_values(data)
    ichimoku_df = calculate_ichimoku_values(data['Close'])

    data['Signal'] = np.where(
        (ha_df['ha_high'].iloc[-1] > max(ha_df['ha_high'].iloc[-2], ha_df['ha_high'].iloc[-3])) &
        (data['Close'].iloc[-1] > ichimoku_df['ChikouSpan'].iloc[-1]) &
        (data['Close'].iloc[-1] > ichimoku_df['SenkouSpanH'].iloc[-1]) &
        ((ichimoku_df['TenkanSen'].iloc[-1] >= ichimoku_df['KijunSen'].iloc[-1]) or (data['Close'].iloc[-1] > ichimoku_df['KijunSen'].iloc[-1])),
        'Buy',
        np.where(
            (ha_df['ha_low'].iloc[-1] < min(ha_df['ha_low'].iloc[-2], ha_df['ha_low'].iloc[-3])) &
            (data['Close'].iloc[-1] < ichimoku_df['ChikouSpan'].iloc[-1]) &
            (data['Close'].iloc[-1] < ichimoku_df['SenkouSpanL'].iloc[-1]) &
            ((ichimoku_df['TenkanSen'].iloc[-1] <= ichimoku_df['KijunSen'].iloc[-1]) or (data['Close'].iloc[-1] < ichimoku_df['KijunSen'].iloc[-1])),
            'Sell',
            'Hold'
        )
    )

    return data

