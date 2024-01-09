import pandas as pd

def calculate_bollinger_bands(dataframe, window=7, num_std=2):
    if 'Close' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'Close' column")

    df = dataframe.copy()
    df['Middle_Band'] = df['Close'].rolling(window=window).mean()
    df['STD'] = df['Close'].rolling(window=window).std()
    df['Upper_Band'] = df['Middle_Band'] + (df['STD'] * num_std)
    df['Lower_Band'] = df['Middle_Band'] - (df['STD'] * num_std)

    return df.drop(['STD'], axis=1)


def detect_bollinger_bands(dataframe):
    if not all(x in dataframe.columns for x in ['Close', 'Upper_Band', 'Middle_Band', 'Lower_Band']):
        raise ValueError("DataFrame must contain 'Close', 'Upper_Band', 'Middle_Band', 'Lower_Band' columns")

    df = dataframe.copy()
    df['Signal'] = 'Hold'

    # Iterate through DataFrame and set signals, skipping NaN values
    for i in range(len(df)):
        # Skip rows where any of the necessary values are NaN
        if pd.isna(df.loc[i, 'Close']) or pd.isna(df.loc[i, 'Upper_Band']) or pd.isna(df.loc[i, 'Lower_Band']):
            continue

        # Potential buy signal: price crossing below the lower band
        if df.loc[i, 'Close'] < df.loc[i, 'Lower_Band']:
            df.at[i, 'Signal'] = 'Buy'

        # Potential sell signal: price crossing above the upper band
        elif df.loc[i, 'Close'] > df.loc[i, 'Upper_Band']:
            df.at[i, 'Signal'] = 'Sell'

    return df


def calculate_and_detect_bollinger_bands(dataframe, window=7, num_std=2):
    # First, calculate the Bollinger Bands
    bb_df = calculate_bollinger_bands(dataframe, window, num_std)

    # Next, detect the signals based on Bollinger Bands
    final_df = detect_bollinger_bands(bb_df)

    return final_df