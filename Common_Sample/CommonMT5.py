#######################################################################################################################################
# symbol = 'EURUSD'
# from_date = '2023-11-01'
# to_date = '2023-11-30'
# data = Common_Sample.Common_Sample.loaddataMT5(symbol, from_date, to_date)
class CommonMT5:

    @staticmethod
    def loaddataMT5(symbol, from_date, to_date):
        import MetaTrader5 as mt5
        from datetime import datetime
        import pandas as pd 

        # Kết nối tới MetaTrader 5
        if not mt5.initialize():
            print("Khởi tạo MT5 không thành công")
            mt5.shutdown()

        from_date_str = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_str = datetime.strptime(to_date, '%Y-%m-%d')
        
        # Lấy dữ liệu OHLC cho cặp tiền symbol trong khoảng thời gian đã xác định
        ohlc_data = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_D1, from_date_str, to_date_str)
        # Ngắt kết nối với MT5
        mt5.shutdown()

        # Chuyển dữ liệu nhận được thành DataFrame và hiển thị
        data = pd.DataFrame(ohlc_data)
        data['time'] = pd.to_datetime(data['time'], unit='s')

        # ohlc_df.reset_index(inplace=True)

        data = data.rename(columns={'time': 'Datetime'})        
        data = data.rename(columns={'open': 'Open'})       
        data = data.rename(columns={'high': 'High'})       
        data = data.rename(columns={'low': 'Low'})       
        data = data.rename(columns={'close': 'Close'})       
        data = data.rename(columns={'tick_volume': 'Volume'})       

        data = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])

        return data
    
    @staticmethod
    def loaddataMT5_FromTo(symbol, from_date, to_date, timeframe):
        import MetaTrader5 as mt5
        from datetime import datetime
        import pandas as pd 

        # Kết nối tới MetaTrader 5
        if not mt5.initialize():
            print("Khởi tạo MT5 không thành công")
            mt5.shutdown()

        from_date_str = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_str = datetime.strptime(to_date, '%Y-%m-%d')
        
        # Lấy dữ liệu OHLC cho cặp tiền symbol trong khoảng thời gian đã xác định
        ohlc_data = mt5.copy_rates_range(symbol, timeframe, from_date_str, to_date_str)
        # Ngắt kết nối với MT5
        mt5.shutdown()

        # Chuyển dữ liệu nhận được thành DataFrame và hiển thị
        data = pd.DataFrame(ohlc_data)
        data['time'] = pd.to_datetime(data['time'], unit='s')

        # ohlc_df.reset_index(inplace=True)

        data = data.rename(columns={'time': 'Datetime'})        
        data = data.rename(columns={'open': 'Open'})       
        data = data.rename(columns={'high': 'High'})       
        data = data.rename(columns={'low': 'Low'})       
        data = data.rename(columns={'close': 'Close'})       
        data = data.rename(columns={'tick_volume': 'Volume'})       

        data = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])

        return data