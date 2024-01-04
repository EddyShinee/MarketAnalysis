#######################################################################################################################################
# symbol = 'VCB'
# from_date = '2023-11-01'
# to_date = '2023-11-30'
# data = Common_Sample.Common_Sample.loaddataSSI(symbol, from_date, to_date)
class CommonSSI:

    @staticmethod   
    def loaddataSSI(symbol, from_date, to_date):
    # Import các module cần thiết
        from ssi_fc_data import fc_md_client, model
        from datetime import datetime
        import pandas as pd
        import json
        import configDataSSL

        # Tạo Market Data Client
        # from_date = "01/11/2023"
        # to_date = "17/11/2023"

        # Sử dụng datetime để phân tích chuỗi ngày tháng
        from_date_new = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_new = datetime.strptime(to_date, '%Y-%m-%d')

        # Định dạng lại ngày tháng sang định dạng 'dd/mm/yyyy'
        from_date_new = from_date_new.strftime('%d/%m/%Y')
        to_date_new = to_date_new.strftime('%d/%m/%Y')

        client = fc_md_client.MarketDataClient(configDataSSL)

        req = model.daily_ohlc('VCB', from_date_new, to_date_new)

        data_dict = client.daily_ohlc(configDataSSL, req)
        print(type(data_dict))

        data_list = data_dict['data']
  
        data = pd.DataFrame(data_list)
   
        data = data.rename(columns={'TradingDate': 'Datetime'})       

        data = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])

        return data