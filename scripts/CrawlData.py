import requests
import re
import csv
import os
from config import API_CONFIG
from logger_config import get_logger

# Khởi tạo logger
logger = get_logger(__name__)

# Đường dẫn thư mục 'data'
output_directory = 'data'
os.makedirs(output_directory, exist_ok=True)

# Hàm làm sạch text
def clean_text(text):
    if isinstance(text, str):
        return re.sub(r'<[^>]*>', ' ', text)
    return text

def fetch_data(api_name):
    api_info = API_CONFIG.get(api_name)

    if not api_info:
        logger.error(f"API '{api_name}' không hợp lệ hoặc không tồn tại.")
        return None

    api_url = api_info["url"]
    query = api_info["query"]

    # Gửi yêu cầu tới API
    try:
        response = requests.post(api_url, json={"query": query})
        response.raise_for_status()
        logger.info(f"Da goi thanh cong API '{api_name}'.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Loi khi goi API '{api_name}': {e}")
        return None

def save_to_csv(api_name, data):
    products = data['data']['products']
    file_name = os.path.join(output_directory, f"{api_name}_products.csv")

    try:
        with open(file_name, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            header = [
                'STT', 'product_id', 'name', 'brand', 'type', 'price', 'warranty_info',
                'feature', 'voice_control', 'microphone', 'battery_life', 'dimensions', 'weight', 'compatibility'
            ]
            writer.writerow(header)

            for index, product in enumerate(products, start=1):
                general = product['general']
                attributes = general['attributes']
                filterable = product.get('filterable', {})
                price = filterable.get('price', '')

                row = [
                    index,
                    general['product_id'],
                    general['name'],
                    attributes.get('phone_accessory_brands', ''),
                    attributes.get('mobile_accessory_type', ''),
                    price,
                    attributes.get('warranty_information', '' ),
                    attributes.get('tai_nghe_tinh_nang', ''),
                    attributes.get('tai_nghe_dieu_khien', ''),
                    attributes.get('tai_nghe_micro', '' ),
                    attributes.get('tai_nghe_pin', ''),
                    attributes.get('dimensions', ''),
                    attributes.get('product_weight', ''),
                    attributes.get('tai_nghe_tuong_thich', ''),
                ]
                writer.writerow(row)

        logger.info(f"Du lieu tu API '{api_name}' da duoc luu vao '{file_name}'.")
    except Exception as e:
        logger.error(f"Loi khi luu du lieu vao file CSV '{file_name}': {e}")

# Gọi fetch_data và save_to_csv cho từng API
for api_name in API_CONFIG.keys():
    data = fetch_data(api_name)
    if data:
        save_to_csv(api_name, data) 