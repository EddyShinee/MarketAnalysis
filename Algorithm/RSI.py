import pandas as pd

def calculate_rsi(dataframe, window=7):
    """
    Calculate the Relative Strength Index (RSI).

    Parameters:
    - dataframe: DataFrame containing the 'Close' prices.
    - window: The period window for RSI calculation (default is 7).

    Returns:
    - DataFrame with a new 'RSI' column.
    """
    if 'Close' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'Close' column")

    df = dataframe.copy()
    delta = df['Close'].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def detect_rsi_signals(dataframe, overbought_threshold=70, oversold_threshold=30):
    """
    Detect signals based on RSI.

    Parameters:
    - dataframe: DataFrame with 'RSI' column.
    - overbought_threshold: RSI threshold for overbought conditions (default is 70).
    - oversold_threshold: RSI threshold for oversold conditions (default is 30).

    Returns:
    - DataFrame with an additional 'RSI_Signal' column indicating potential trading signals.
    """
    if 'RSI' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'RSI' column")

    df = dataframe.copy()
    df['Signal'] = 'Hold'

    # Potential buy signal: RSI crossing above the oversold threshold
    df.loc[df['RSI'] < oversold_threshold, 'Signal'] = 'Buy'

    # Potential sell signal: RSI crossing below the overbought threshold
    df.loc[df['RSI'] > overbought_threshold, 'Signal'] = 'Sell'

    return df


def calculate_and_detect_rsi(dataframe, window=14, overbought_threshold=70, oversold_threshold=30):
    """
    Calculate RSI and detect trading signals based on RSI.

    Parameters:
    - dataframe: DataFrame containing the 'Close' prices.
    - window: The period window for RSI calculation (default is 7).
    - overbought_threshold: RSI threshold for overbought conditions (default is 70).
    - oversold_threshold: RSI threshold for oversold conditions (default is 30).

    Returns:
    - DataFrame with RSI values and trading signals.
    """
    rsi_df = calculate_rsi(dataframe, window)
    final_df = detect_rsi_signals(rsi_df, overbought_threshold, oversold_threshold)

    return final_df

# Example usage
# Assuming 'data' is a DataFrame with a 'Close' column
# result = calculate_and_detect_rsi(data)
