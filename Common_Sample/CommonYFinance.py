#######################################################################################################################################
# Su dung cac ham ben duoi
# import sys
# sys.path.append("../Common_Sample")
# import Common_Sample

#######################################################################################################################################
# symbol = 'VCB.VN'
# from_date = '2023-11-01'
# to_date = '2023-11-30'
# interval = '1d'
# data = Common_Sample.Common_Sample.loaddataYFinance(symbol, from_date, to_date)
class CommonYFinance:

    @staticmethod
    def loaddataYFinance(symbol, from_date, to_date, interval):
        import pandas as pd
        import yfinance as yf

        data = yf.download(symbol, start=from_date, end=to_date, interval=interval)
        data.reset_index(inplace=True)
        data = data.rename(columns={'Date': 'Datetime'})
        # data = data.drop('Adj Close', axis=1)
        data = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])

        return data
