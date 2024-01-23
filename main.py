from datetime import datetime

import time

from Common.Data.LoadDataMT4 import LoadDataFromMT4

# run_minutes = [0, 15, 30, 45]

# run_minutes = [0, 30]
run_minutes = [0]
# run_minutes = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
# run_minutes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
#                29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
#                55, 56, 57, 58, 59]


def schedule_running():
    while True:
        current_time = datetime.now()
        current_minute = current_time.minute
        # Kiểm tra xem phút hiện tại có nằm trong danh sách các phút cần chạy hàm không
        if current_minute in run_minutes:
            # Kiểm tra xem đã chạy hàm trong phút hiện tại hay chưa
            last_run = getattr(schedule_running, 'last_run', None)
            if last_run is None or last_run != current_minute:
                data = LoadDataFromMT4()
                data.run()
                # Lưu lại phút cuối cùng mà hàm đã chạy
                setattr(schedule_running, 'last_run', current_minute)
        # Nghỉ 10 giây trước khi kiểm tra lại
        time.sleep(1)


def main():
    print("Analysis Market server is running....")
    try:
        schedule_running()
    except Exception as e:
        # logging.error(f'Error during application initialization: {str(e)}')
        raise


if __name__ == "__main__":
    main()
