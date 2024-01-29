import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from ta import trend  # Thư viện để tính toán MACD và các chỉ báo kỹ thuật khác

# Load data
data = pd.read_csv("data.csv")

# Xử lý dữ liệu (nếu cần)
data = data.dropna()  # Loại bỏ các hàng có giá trị thiếu
data = data.fillna(method="ffill")  # Điền các giá trị thiếu bằng phương pháp forward fill

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
train_data = data[:int(0.7 * len(data))]
test_data = data[int(0.7 * len(data)):]

# Thử nghiệm các mô hình hồi quy khác nhau
models = [
    ("LinearRegression", LinearRegression()),
    ("Ridge", Ridge()),
    ("Lasso", Lasso()),
    ("PolynomialRegression", Pipeline([("poly", PolynomialFeatures(degree=2)), ("linear", LinearRegression())])),
    ("RandomForestRegressor", RandomForestRegressor()),
]

# Tìm mô hình tốt nhất và thực hiện prediction
best_model, best_score = None, float("-inf")
for name, model in models:
    model.fit(train_data[["x1", "x2", "volume", "sentiment"]], train_data["y"])  # Thêm các biến độc lập
    predictions = model.predict(test_data[["x1", "x2", "volume", "sentiment"]])
    score = np.mean(np.abs(predictions - test_data["y"]))  # Đánh giá độ chính xác
    if score > best_score:
        best_model, best_score = model, score

predictions = best_model.predict(test_data[["x1", "x2", "volume", "sentiment"]])

# Tính toán MACD
macd = trend.MACD(test_data["close"])

# Kết hợp prediction và phân tích kỹ thuật để đưa ra quyết định giao dịch
# (Cách kết hợp tương tự như ở các ví dụ trước)
