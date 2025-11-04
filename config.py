"""
Configuration file for the Secure File Sharing System
"""

import os
from dotenv import load_dotenv

load_dotenv()

GANACHE_URL = os.getenv('GANACHE_URL', 'http://127.0.0.1:8545')

GANACHE_PRIVATE_KEY = os.getenv('GANACHE_PRIVATE_KEY', '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')

CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', None)

IPFS_API_URL = os.getenv('IPFS_API_URL', 'http://127.0.0.1:5001')

UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted'
DECRYPTED_FOLDER = 'decrypted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)
os.makedirs('ipfs_storage', exist_ok=True)

MAX_FILE_SIZE = 50 * 1024 * 1024

SECRET_KEY = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')
