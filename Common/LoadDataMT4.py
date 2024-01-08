# 1. Connect đến MT4 để lấy Token
# 2. Lấy Token để load thông tin từ MT4
from datetime import datetime

import pandas as pd
import time

from Algorithm.DetectSignal import detect_signal
from Utils.GlobalConfig import BASE_API_URL, USER, PASSWORD, HOST, PORT, TIME_FRAME, BARS, API_CONNECT, SYMBOLS, \
    API_HISTORY_PRICE_MANY
from Utils.HttpRequest import make_get_request
from Utils.Redis import redis_manager


class GetDataFromMT4:
    def __init__(self):
        self.base_url = BASE_API_URL
        self.path_connect = API_CONNECT
        self.account_number = USER
        self.password = PASSWORD
        self.host = HOST
        self.port = PORT
        self.api_get_symbols = API_HISTORY_PRICE_MANY
        self.symbols = SYMBOLS

    def get_token(self):
        print("Get account token")
        token = redis_manager.get_value('token')
        if token is None:
            url = self.base_url + self.path_connect
            request_params = {
                'user': self.account_number,
                'password': self.password,
                'host': self.host,
                'port': self.port
            }
            token = make_get_request(url, params=request_params)
            if not isinstance(token, str):
                print(f"Error system: {token['message']}")
                return
            redis_manager.set_value('token', token)
        return token

    def get_data_mt4(self):
        token = self.get_token()
        print(f"Token: {token}")
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%dT%H:%M:%S")
        url = self.base_url + self.api_get_symbols
        request_params = {
            "id": token,
            "symbol": self.symbols,
            "timeframe": TIME_FRAME,
            "from": formatted_now,
            "count": BARS
        }
        print(f"Get data pairs: {self.symbols} - Time: {now}")
        response = make_get_request(url, params=request_params)
        if 'code' in response:
            if response['code'] is not None:
                print(f"[Error] Get data from MT4")
                return None
        return response

    @staticmethod
    def process_data(currency_pair):
        print(currency_pair)
        symbol = currency_pair['symbol']
        # print(f"Symbol: {symbol}")
        bars = currency_pair['bars']
        data = pd.DataFrame(bars)
        data['time'] = pd.to_datetime(data['time'])
        data = data.rename(columns={'time': 'Datetime'})
        data = data.rename(columns={'open': 'Open'})
        data = data.rename(columns={'high': 'High'})
        data = data.rename(columns={'low': 'Low'})
        data = data.rename(columns={'close': 'Close'})
        data = data.rename(columns={'volume': 'Volume'})
        data = pd.DataFrame(data, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
        return data

    def run(self):
        response_data = self.get_data_mt4()
        if response_data is None:
            time.sleep(900)
            response_data = self.get_data_mt4()

        for currency_pair in response_data:
            symbol = currency_pair['symbol']
            data = self.process_data(currency_pair)
            detect_signal(symbol, data)
            time.sleep(2)
            # Xử lý code data ở đây
            # Hãy xử ly1 thêm code ở chỗ naày
            # print(data)
