import pandas as pd
import re
import os
from logger_config import get_logger

# Khởi tạo logger
logger = get_logger(__name__)

# Đường dẫn đến thư mục 'data' và file CSV
output_directory = 'data'
file_path = os.path.join(output_directory, 'cellphoneS_products.csv')

# Kiểm tra xem file có tồn tại không
if not os.path.isfile(file_path):
    logger.error(f"File '{file_path}' khong ton tai. Vui long kiem tra lai.")
else:
    logger.info("Bat dau qua trinh lam sach du lieu.")

    # Đọc dữ liệu từ file CSV
    try:
        data = pd.read_csv(file_path)
        logger.info("Da doc thanh cong du lieu tu file CSV.")
    except Exception as e:
        logger.error(f"Loi khi doc file CSV '{file_path}': {e}")
        exit()

    # Định nghĩa hàm để loại bỏ thẻ HTML khỏi văn bản
    def clean_text(text):
        if not isinstance(text, str):
            return ''
        
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return ''.join(c for c in text if ord(c) >= 32 and ord(c) <= 126)

    # Áp dụng hàm clean_text cho các cột cần thiết
    columns_to_clean = [
        'name', 'brand', 'type', 'warranty_info',
        'feature', 'voice_control', 'microphone', 'battery_life', 'dimensions', 'weight', 'compatibility'
    ]
    for column in columns_to_clean:
        if column in data.columns:
            data[column] = data[column].apply(clean_text)
            logger.info(f"Da lam sach cot '{column}'.")
        else:
            logger.warning(f"Cot '{column}' khong ton tai trong du lieu.")

    # Lưu dữ liệu đã làm sạch vào file Excel mới
    cleaned_file_path = os.path.join(output_directory, 'cleaned_cellphoneS_products.xlsx')
    try:
        data.to_excel(cleaned_file_path, index=False)
        logger.info(f"Du lieu da duoc lam sach va luu vao '{cleaned_file_path}'.")
    except Exception as e:
        logger.error(f"Loi khi luu du lieu vao file Excel '{cleaned_file_path}': {e}")
