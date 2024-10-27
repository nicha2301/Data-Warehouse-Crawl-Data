import logging
import mysql.connector
from mysql.connector import Error

class DatabaseLogHandler(logging.Handler):
    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        self.setup_db()  # Thiết lập kết nối và tạo bảng nếu chưa tồn tại

    def setup_db(self):
        try:
            # Kết nối ban đầu để tạo database nếu chưa tồn tại
            initial_connection = mysql.connector.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host']
            )
            initial_cursor = initial_connection.cursor()
            initial_cursor.execute("CREATE DATABASE IF NOT EXISTS products_db")
            initial_cursor.close()
            initial_connection.close()

            # Kết nối vào database `products_db`
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            
            # Tạo bảng logs trong products_db nếu chưa tồn tại
            create_table_query = """
            CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level VARCHAR(50),
                logger_name VARCHAR(100),
                message TEXT,
                traceback TEXT
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Error as e:
            print(f"Error setting up database: {e}")

    def emit(self, record):
        log_entry = self.format(record)
        traceback = record.exc_text if record.exc_info else None
        
        try:
            if self.connection is None or not self.connection.is_connected():
                self.setup_db()  # Cố gắng kết nối lại
            
            sql = "INSERT INTO logs (level, logger_name, message, traceback) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (record.levelname, record.name, log_entry, traceback))
            self.connection.commit()
        except Error as e:
            print(f"Error logging to database: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        super().close()
