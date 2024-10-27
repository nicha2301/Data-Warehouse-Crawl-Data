import logging
from db_logger import DatabaseLogHandler

# Cấu hình kết nối MySQL
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'products_db'
}

# Khởi tạo DatabaseLogHandler
db_handler = DatabaseLogHandler(db_config)

# Thiết lập cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[db_handler, logging.StreamHandler()]  # Ghi vào database và console
)

# Hàm tiện lợi để lấy logger
def get_logger(name):
    return logging.getLogger(name)
