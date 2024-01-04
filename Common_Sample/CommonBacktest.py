#######################################################################################################################################
# Su dung cac ham ben duoi
# import sys
# sys.path.append("../Common_Sample")
# import Common_Sample

#######################################################################################################################################
# data = CommonBacktest.CommonBacktest.backtest(databacktest, initial_capital, shares_per_signal)
class CommonBacktest:

    @staticmethod
    def backtest(data, initial_capital, shares_per_signal): # Chung khoan
        import pandas as pd
        import matplotlib.pyplot as plt
        import plotly.graph_objects as go
        import plotly.express as px

        capital = initial_capital
        shares_held = 0

        # Xác định vị thế mua/ bán
        data['Position_Buy'] = data['Buy_Signal'].shift()
        data['Position_Sell'] = data['Sell_Signal'].shift()

        data['Trade_Action'] = ''
        data['Capital'] = capital
        data['Shares_Held'] = shares_held

        # Lặp qua mỗi hàng trong DataFrame
        for index, row in data.iterrows():
            # Nếu có tín hiệu mua và có đủ vốn để mua
            if row['Position_Buy'] == 1 and capital >= row['Close'] * shares_per_signal and row['Trade_Action'] == '':
                # Mua cổ phiếu và cập nhật vốn và số cổ phiếu được giữ
                data.at[index, 'Trade_Action'] = 'Buy'
                capital -= row['Close'] * shares_per_signal
                data.at[index, 'Capital'] = capital
                shares_held += shares_per_signal
                data.at[index, 'Shares_Held'] = shares_held
            elif row['Position_Sell'] == 1 and shares_held > 0 and row['Trade_Action'] == '':
                data.at[index, 'Trade_Action'] = 'Sell'
                capital += row['Close'] * shares_held
                data.at[index, 'Capital'] = capital
                shares_held = 0
                data.at[index, 'Shares_Held'] = shares_held  # Giảm số lượng cổ phiếu 0
            else:
                data.at[index, 'Capital'] = capital
                data.at[index, 'Shares_Held'] = shares_held

            # Cập nhật giá trị hiện tại của vốn dựa trên số cổ phiếu đang giữ và giá đóng cửa hiện tại
            current_value = capital + shares_held * row['Close']

        # Ngày vào lệnh
        first_entry_date = data[data['Position_Buy'] == 1].index.min()
        # Tính lợi nhuận
        profit = current_value - initial_capital
        # Tính lợi nhuận thị trường
        market_return = (data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]
        # Tính lợi nhuận chiến lược
        strategy_return = (current_value - initial_capital) / initial_capital

        print(f"Ngày vào lệnh đầu tiên: {first_entry_date}")
        print(f'Tổng lợi nhuận: {profit}')
        print(f'Tổng giá trị tài khoản: {current_value}')
        print(f'Lợi nhuận thị trường: {market_return * 100}%')
        print(f'Lợi nhuận chiến lược: {strategy_return * 100}%')

        # Tính toán lợi nhuận thị trường và chiến lược
        data['Market_Return'] = data['Close'].pct_change()
        data['Cumulative_Market_Returns'] = (1 + data['Market_Return']).cumprod()

        # Tính toán lợi nhuận lũy kế từ chiến lược
        data['Strategy_Value'] = data['Capital'] + data['Shares_Held'] * data['Close']
        data['Cumulative_Strategy_Returns'] = data['Strategy_Value'] / initial_capital

        # Vẽ biểu đồ so sánh lợi nhuận lũy kế từ thị trường và từ chiến lược
        plt.figure(figsize=(12, 6))
        plt.plot(data['Cumulative_Market_Returns'], label='Market Returns')
        plt.plot(data['Cumulative_Strategy_Returns'], label='Strategy Returns')
        plt.title('Comparison of Cumulative Returns: Market vs Strategy')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.show()

        # Tạo biểu đồ sử dụng Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative_Market_Returns'], mode='lines', name='Market Returns'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative_Strategy_Returns'], mode='lines', name='Strategy Returns'))

        fig.update_layout(
            title='Comparison of Cumulative Returns: Market vs Strategy',
            xaxis_title='Date',
            yaxis_title='Cumulative Returns',
        )
        fig.show()

        return data