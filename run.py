import subprocess
import logging
import sys

# Cấu hình logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    try:
        logging.info(f"Bat dau chay script: {script_name}")
        # Thực thi script và dừng ngay nếu có lỗi (check=True)
        result = subprocess.run(
            ['python', script_name], 
            check=True, 
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        logging.info(f"Script '{script_name}' chay thanh cong.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Loi xay ra khi chay script '{script_name}'. Chi tiet:\n{e.stderr}")
        sys.exit(1)  # Dừng chương trình ngay lập tức khi gặp lỗi

if __name__ == "__main__":
    # Chạy các script tuần tự và dừng nếu có lỗi
    run_script('scripts/CrawlData.py')
    run_script('scripts/CleanData.py')
    run_script('scripts/LoadToDb.py')
