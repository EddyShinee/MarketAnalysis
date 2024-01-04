#######################################################################################################################################
# Su dung cac ham ben duoi
# import sys
# sys.path.append("../Common_Sample")
# import Common_Sample

#######################################################################################################################################
# symbol = 'EURUSD=X'
# from_date = '2023-11-01'
# to_date = '2023-11-30'
# data = Common_Sample.Common_Sample.loaddataBinance(symbol, from_date, to_date)
class CommonBinance:

    @staticmethod
    def loaddataBinance_FromTo(symbol, from_date, to_date, timeframe):
        import pandas as pd
        import ccxt
        from datetime import datetime

        # Khởi tạo kết nối đến sàn Binance
        exchange = ccxt.binance()

        # Định dạng ngày tháng
        since = exchange.parse8601(from_date + 'T00:00:00Z')
        end = exchange.parse8601(to_date + 'T00:00:00Z')

        # Lấy dữ liệu thị trường từ sàn Binance
        # 1d
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)

        # Chuyển dữ liệu thành DataFrame
        data = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')         
        data = data.rename(columns={'Timestamp': 'Datetime'})

        return data
    
    @staticmethod
    def loaddataBinance_Limit(symbol, from_date, to_date):
        import pandas as pd
        import ccxt 

        # Khởi tạo kết nối đến sàn Binance
        exchange = ccxt.binance()

        # Lấy dữ liệu thị trường từ sàn Binance
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d', limit=1000)  # Lấy 1000 điểm dữ liệu

        # Chuyển dữ liệu thành DataFrame
        data = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')         
        data = data.rename(columns={'Timestamp': 'Datetime'})
    
        return data
    
    @staticmethod
    def loaddataBinance_FromToExt(symbol, from_date, to_date):
        import pandas as pd
        import ccxt
        from datetime import datetime

        # Khởi tạo kết nối đến sàn Binance
        exchange = ccxt.binance()

        from_timestamp = int(datetime.strptime(from_date, '%Y-%m-%d').timestamp() * 1000)
        to_timestamp = int(datetime.strptime(to_date, '%Y-%m-%d').timestamp() * 1000)

        # Lấy dữ liệu OHLCV
        ohlcv = []
        current_timestamp = from_timestamp
        while current_timestamp < to_timestamp:
            dataTemp = exchange.fetch_ohlcv(symbol, timeframe='1d', since=current_timestamp, limit=100000)
            if not dataTemp:
                break
            current_timestamp = dataTemp[-1][0]
            ohlcv += dataTemp

        # Chuyển dữ liệu thành DataFrame
        data = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
        data = data.rename(columns={'Timestamp': 'Datetime'})        

        data = data[data['Datetime'] <= to_date]

        return data
