from tkinter import Tk
from database_handler import DatabaseHandler
from file_encryptor_decryptor import FileEncryptorDecryptor

if __name__ == "__main__":
    # Database credentials
    DATABASE_HOST = '127.0.0.1'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = ''
    DATABASE_NAME = 'test'

    # Initialize database handler
    db_handler = DatabaseHandler(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)

    # Initialize file encryptor decryptor
    file_encryptor_decryptor = FileEncryptorDecryptor(db_handler)

    choice = input("Do you want to (E)ncrypt or (D)ecrypt a file? ").lower()

    if choice == 'e':
        file_encryptor_decryptor.encrypt_file()
    elif choice == 'd':
        file_encryptor_decryptor.decrypt_file()
    else:
        print("Invalid choice.")
