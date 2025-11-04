"""
AES Encryption/Decryption Utilities
Handles file encryption and decryption using AES-256
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os


class AESCipher:
    
    @staticmethod
    def generate_key():
        """Generate a random 256-bit AES key"""
        return get_random_bytes(32)
    
    @staticmethod
    def encrypt_file(file_data, key):
        """
        Encrypt file data using AES-256 in CBC mode
        Returns: (encrypted_data, iv)
        """
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        
        padded_data = pad(file_data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        
        return encrypted_data, iv
    
    @staticmethod
    def decrypt_file(encrypted_data, key, iv):
        """
        Decrypt file data using AES-256 in CBC mode
        Returns: decrypted_data
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded, AES.block_size)
        
        return decrypted_data
    
    @staticmethod
    def encrypt_file_path(input_path, output_path, key):
        """Encrypt a file from disk"""
        with open(input_path, 'rb') as f:
            file_data = f.read()
        
        encrypted_data, iv = AESCipher.encrypt_file(file_data, key)
        
        with open(output_path, 'wb') as f:
            f.write(iv + encrypted_data)
        
        return iv
    
    @staticmethod
    def decrypt_file_path(input_path, output_path, key):
        """Decrypt a file from disk"""
        with open(input_path, 'rb') as f:
            file_data = f.read()
        
        iv = file_data[:16]
        encrypted_data = file_data[16:]
        
        decrypted_data = AESCipher.decrypt_file(encrypted_data, key, iv)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        return decrypted_data


if __name__ == "__main__":
    key = AESCipher.generate_key()
    print(f"Generated AES Key (hex): {key.hex()}")
    
    test_data = b"This is a secret message that will be encrypted!"
    print(f"Original data: {test_data}")
    
    encrypted, iv = AESCipher.encrypt_file(test_data, key)
    print(f"Encrypted (hex): {encrypted.hex()[:64]}...")
    
    decrypted = AESCipher.decrypt_file(encrypted, key, iv)
    print(f"Decrypted: {decrypted}")
    
    print(f"Match: {test_data == decrypted}")
