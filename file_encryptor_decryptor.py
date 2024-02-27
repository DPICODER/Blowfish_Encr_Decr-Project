import os
from tkinter import filedialog
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import random 

class FileEncryptorDecryptor:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def encrypt_file(self):
        # File encryption logic
        root = Tk()
        root.withdraw()  # Hide the main window

        # Open a window for selecting the file
        file_path = filedialog.askopenfilename(title="Select a file for encryption")
        root.destroy()  # Close the window after selection

        if file_path:
            # Generate encryption key using BCSA
            key = self.generate_key_with_bcsa()

            # Encrypt the file
            encrypted_content = self._encrypt_file_content(file_path, key)

            # Save encrypted file and key to the database
            file_name = os.path.basename(file_path)
            self._save_encrypted_file_to_db(encrypted_content, key, file_name)
            print("File encrypted successfully!")

    def decrypt_file(self):
        # File decryption logic
        # List all the encrypted files from the database
        files = self._list_encrypted_files()

        if files:
            print("Encrypted files:")
            for idx, file in enumerate(files, 1):
                print(f"{idx}. {file['file_name']}")

            # Choose a file to decrypt
            file_idx = int(input("Enter the index of the file you want to decrypt: ")) - 1

            if 0 <= file_idx < len(files):
                encrypted_content = files[file_idx]['file_content']
                encoded_key = files[file_idx]['encryption_key']
                file_name = files[file_idx]['file_name']

                # Decrypt the file
                decrypted_content = self._decrypt_file_content(encrypted_content, encoded_key, file_name)
                print("File decrypted successfully!")
            else:
                print("Invalid file index.")
        else:
            print("No encrypted files found in the database.")

    def _encrypt_file_content(self, file_path, key):
        # Encryption logic for file content
        with open(file_path, 'rb') as file:
            file_content = file.read()

        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        encrypted_content = cipher.encrypt(pad(file_content, Blowfish.block_size))
        return encrypted_content

    def _decrypt_file_content(self, encrypted_content, encoded_key, file_path):
        # Decryption logic for file content
        key = b64decode(encoded_key)
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        decrypted_content = unpad(cipher.decrypt(encrypted_content), Blowfish.block_size)

        # Save decrypted file to specified location
        output_dir = filedialog.askdirectory(title="Select a directory to save decrypted files")
        if output_dir:
            decrypted_file_path = os.path.join(output_dir, "Decrypted_" + os.path.basename(file_path))
            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_content)

        return decrypted_content
    

    def _save_encrypted_file_to_db(self, encrypted_content, key, file_name):
        # Saving encrypted file to the database
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
    def _list_encrypted_files(self):
        # Listing encrypted files from the database
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
    def generate_key_with_bcsa(self):
        # Key generation logic
        # Choose key length in bytes (adjusted to 16 to 56 bytes)
        key_length = random.randint(16, 56)

        # Characters to use for key generation
        search_space = string.ascii_letters + string.digits + string.punctuation

        # Parameters for genetic algorithm
        population_size = 10
        max_iterations = 100

        # Generate initial population
        population = [''.join(random.sample(search_space, key_length)) for _ in range(population_size)]

        # Genetic algorithm loop
        for _ in range(max_iterations):
            # Evaluate fitness
            fitness_scores = [self.evaluate_fitness(key) for key in population]

            # Select top keys
            top_keys = self.select_top_keys(population, fitness_scores)

            # Create new population
            new_population = []
            for _ in range(population_size):
                parent1, parent2 = random.choices(top_keys, k=2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child, search_space)
                new_population.append(child)

            population = new_population

        # Select and finalize best key
        best_key = max(population)

        # Ensure key length is within range (truncate if needed)
        best_key = best_key[:56]  # Truncate if longer than 56 bytes
        best_key = best_key.ljust(16, random.choice(search_space))  # Pad if shorter than 16 bytes

        # Encode and return key
        return best_key.encode('utf-8')





    def evaluate_fitness(self, key):
        return sum(1 for char in key if char.isalpha()) / len(key)

    def select_top_keys(self, population, fitness_scores):
        sorted_keys = [key for _, key in sorted(zip(fitness_scores, population), reverse=True)]
        return sorted_keys[:int(len(population) * 0.1)]

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(parent1))
        return parent1[:crossover_point] + parent2[crossover_point:]

    def mutate(self, key, search_space):
        mutation_point = random.randint(0, len(key) - 1)
        mutation_character = random.choice(search_space)
        mutated_key = key[:mutation_point] + mutation_character + key[mutation_point + 1:]
        return mutated_key
