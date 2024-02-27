import pymysql

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def save_encrypted_file(self, encrypted_content, key, file_name):
        # Database connection and saving logic
        connection = pymysql.connect(host=self.DATABASE_HOST, port=3306, user=self.DATABASE_USER,
                                     password=self.DATABASE_PASSWORD, database=self.DATABASE_NAME,
                                     charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                encoded_key = b64encode(key)
                sql = "INSERT INTO encrypted_files (file_content, encryption_key, file_name) VALUES (%s, %s, %s)"
                cursor.execute(sql, (encrypted_content, encoded_key, file_name))
            connection.commit()

        finally:
            connection.close()

    def list_encrypted_files(self):
        # Database connection and listing logic
        connection = pymysql.connect(host=self.DATABASE_HOST, port=3306, user=self.DATABASE_USER,
                                     password=self.DATABASE_PASSWORD, database=self.DATABASE_NAME,
                                     charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = f"SELECT file_content, encryption_key, file_name FROM {self.TABLE_NAME}"
                cursor.execute(sql)
                files = cursor.fetchall()
                return files
        finally:
            connection.close()
