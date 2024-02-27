# Blowfish Encryption and Decryption Project
---
## Overview
This project implements a file encryption and decryption system using the Blowfish encryption algorithm. It provides a user-friendly interface to encrypt and decrypt files securely.

## Features
- Encrypt files using Blowfish encryption algorithm.
- Decrypt encrypted files with the corresponding key.
- Store encrypted files and their keys securely in a MySQL database.
- Generate encryption keys using a genetic algorithm.
- User-friendly GUI for file selection and interaction.

## Prerequisites
- Python 3.x installed on your system.
- Required Python packages installed:
  - `pymysql`: For MySQL database connection.
  - `PyCryptoDome`: For Blowfish encryption and decryption.
  - `Tkinter`: For GUI components.
  
## Setup
1. Clone the repository to your local machine.
2. Install the required Python packages using pip:
   ```
   pip install pymysql pycryptodome
   ```
3. Ensure you have access to a MySQL database and configure the connection details in the `config.py` file.
4. Create the necessary table in the database using the provided SQL script.
5. Run the `main.py` script to start the application.

## Usage
- Upon running the application, you'll be prompted to choose between encrypting (E) or decrypting (D) a file.
- To encrypt a file, select the file using the file dialog and an encryption key will be generated automatically.
- To decrypt a file, choose from the list of encrypted files stored in the database and provide the corresponding encryption key.
- Decrypted files will be saved to the specified directory.

## Architecture
- The project is structured into several modules:
  - `main.py`: Entry point of the application.
  - `file_encryptor_decryptor.py`: Contains the `FileEncryptorDecryptor` class responsible for file encryption and decryption operations.
  - `database_handler.py`: Defines the `DatabaseHandler` class to handle database interactions.
  - `config.py`: Configuration file for database connection details.
- GUI components are implemented using Tkinter for a user-friendly experience.
- Encryption keys are generated using a genetic algorithm implemented within the `FileEncryptorDecryptor` class.


## Acknowledgements
- The project uses the Blowfish encryption algorithm from the PyCryptoDome library.
- Special thanks to the contributors and the open-source community for their valuable contributions and support.
