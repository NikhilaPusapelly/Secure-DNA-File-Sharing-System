# 🔐 Secure DNA File Sharing System

A secure file sharing platform that combines **AES-256 encryption, DNA cryptography, IPFS decentralized storage, and blockchain verification** to protect and validate file transfers.

A complete secure file sharing system that combines multiple layers of security:
- **AES-256 Encryption** for file protection
- **DNA Cryptography** for encoding encryption keys into DNA sequences (A, T, C, G)
- **IPFS** for decentralized file storage
- **Ethereum Blockchain** for immutable metadata records

## Features

- 🔐 **Military-grade AES-256 encryption** for all uploaded files
- 🧬 **DNA-based key encoding** converting binary keys to biological sequences
- 📦 **IPFS integration** for decentralized storage
- ⛓️ **Blockchain verification** using Ethereum smart contracts
- 🌐 **Web interface** with upload and download pages
- ✅ **Complete workflow** from encryption to retrieval

## System Architecture

### Upload Process
1. User selects a file
2. System generates AES-256 encryption key
3. File is encrypted using AES
4. AES key is encoded into DNA sequence
5. Encrypted file is uploaded to IPFS
6. IPFS hash and DNA key are stored on blockchain

### Download Process
1. User enters IPFS hash
2. System retrieves DNA key from blockchain
3. DNA sequence is decoded to AES key
4. Encrypted file is downloaded from IPFS
5. File is decrypted and saved locally

## Project Structure

```
.
├── server.py              # Flask web server
├── blockchain.py          # Blockchain interaction (Web3.py)
├── dna_crypto.py         # DNA encoding/decoding
├── aes_utils.py          # AES encryption/decryption
├── ipfs_utils.py         # IPFS upload/download
├── config.py             # Configuration
├── FileRegistry.sol      # Solidity smart contract
├── requirements.txt      # Python dependencies
├── templates/
│   ├── index.html       # Home page
│   ├── upload.html      # Upload interface
│   └── download.html    # Download interface
└── static/
    └── css/
        └── style.css    # Styling
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Ganache (local Ethereum blockchain) - Optional
- IPFS daemon - Optional

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. The system will work in simulation mode without Ganache or IPFS
   - Files are stored locally instead of IPFS
   - Blockchain operations are simulated

3. (Optional) To use real blockchain, start Ganache:
```bash
ganache-cli
```

4. (Optional) To use real IPFS, start the daemon:
```bash
ipfs daemon
```

### Running the Application

```bash
python server.py
```

Access the application at: http://localhost:5000

## Technology Stack

- **Backend**: Python 3.11, Flask
- **Blockchain**: Solidity, Web3.py, Ganache
- **Storage**: IPFS
- **Cryptography**: PyCryptodome
- **Frontend**: HTML, CSS, JavaScript

## Security Features

1. **AES-256-CBC Encryption**: Industry-standard symmetric encryption
2. **DNA Encoding**: Novel approach to key protection using biological sequences
3. **Blockchain Immutability**: Tamper-proof record storage
4. **Decentralized Storage**: IPFS ensures no single point of failure

## Smart Contract

The `FileRegistry.sol` contract stores:
- IPFS hash (file location)
- DNA-encoded encryption key
- Original filename
- Upload timestamp
- Uploader address

## API Endpoints

- `GET /` - Home page
- `GET /upload` - Upload interface
- `GET /download` - Download interface
- `POST /api/upload` - Upload and encrypt file
- `POST /api/download` - Download and decrypt file
- `GET /api/files` - List all files on blockchain
- `GET /api/status` - System status

## License

MIT License

## Author

Nikhila Pusapelly  
B.Tech Computer Science (Cyber Security)

GitHub: https://github.com/NikhilaPusapelly
