import mysql.connector
import csv
import os
from logger_config import get_logger

# Khởi tạo logger
logger = get_logger(__name__)

# Cấu hình kết nối MySQL
config = {
    'user': 'root',            # Thay 'root' bằng username MySQL của bạn
    'password': '',            # Thay 'password' bằng mật khẩu của bạn
    'host': 'localhost'
}

# Đường dẫn tới file CSV đã làm sạch
output_directory = 'data'
csv_file = os.path.join(output_directory, 'cellphoneS_products.csv')

def init_database(cursor):
    """Tạo database và bảng nếu chưa tồn tại."""
    cursor.execute("CREATE DATABASE IF NOT EXISTS products_db")
    cursor.execute("USE products_db")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id VARCHAR(255),
        name VARCHAR(255),
        brand VARCHAR(255),
        type VARCHAR(255),
        price DECIMAL(10, 2),
        warranty_info TEXT,
        feature TEXT,
        voice_control VARCHAR(255),
        microphone VARCHAR(255),
        battery_life VARCHAR(255),
        dimensions VARCHAR(255),
        weight VARCHAR(255),
        compatibility VARCHAR(255)
    );
    """
    cursor.execute(create_table_query)

def import_data_from_csv(cursor):
    """Đọc dữ liệu từ CSV và chèn vào bảng."""
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cursor.execute(""" 
                INSERT INTO products (
                    product_id, name, brand, type, price, warranty_info, feature, 
                    voice_control, microphone, battery_life, dimensions, weight, compatibility
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['product_id'],
                row['name'],
                row['brand'],
                row['type'],
                row['price'] if row['price'] else None,
                row['warranty_info'],
                row['feature'],
                row['voice_control'],
                row['microphone'],
                row['battery_life'],
                row['dimensions'],
                row['weight'],
                row['compatibility']
            ))

def main():
    """Hàm chính để thực hiện toàn bộ quy trình."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Khởi tạo database và bảng
        init_database(cursor)

        # Nhập dữ liệu từ file CSV
        import_data_from_csv(cursor)

        # Xác nhận các thay đổi
        conn.commit()
        logger.info("Da import du lieu tu file CSV vao database thanh cong.")

    except mysql.connector.Error as err:
        logger.error(f"Loi khi ket noi hoac import du lieu: {err}")
    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()
        logger.info("Da dong ket noi den database.")

if __name__ == "__main__":
    main()
