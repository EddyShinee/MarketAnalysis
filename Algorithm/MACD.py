def calculate_macd(original_df):
    if not all(field in original_df.columns for field in ['Close']):
        raise ValueError("DataFrame must contain 'Close' column")

    df = original_df.copy()
    window = 7

    df['SMA'] = df['Close'].rolling(window=window).mean()

    df['MA_5'] = df['Close'].rolling(window=7).mean()
    # Calculate Short-term Exponential Moving Average (EMA)
    df['short_ema'] = df['Close'].ewm(span=12, adjust=False).mean()
    # Calculate Long-term EMA
    df['long_ema'] = df['Close'].ewm(span=26, adjust=False).mean()
    # Calculate MACD
    df['MACD'] = df['short_ema'] - df['long_ema']
    # Calculate Signal Line
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df


def detect_macd(df):
    df['Signal'] = 'Hold'
    # Loop through the DataFrame to find crossovers
    for i in range(1, len(df)):
        # Check if the MACD crosses above the Signal Line
        if df['MACD'].iloc[i] > df['Signal_Line'].iloc[i] and df['MACD'].iloc[i - 1] <= df['Signal_Line'].iloc[i - 1]:
            df.at[i, 'Signal'] = 'Buy'
        # Check if the MACD crosses below the Signal Line
        elif df['MACD'].iloc[i] < df['Signal_Line'].iloc[i] and df['MACD'].iloc[i - 1] >= df['Signal_Line'].iloc[i - 1]:
            df.at[i, 'Signal'] = 'Sell'
    return df


def calculate_and_detect_macd_signal(original_df):
    # Calculate MACD values
    macd_df = calculate_macd(original_df)
    # Detect signals based on MACD analysis
    final_df = detect_macd(macd_df)
    return final_df
