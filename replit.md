# Secure File Sharing System - Replit Project

## Overview
This is a complete secure file sharing system that combines AES-256 encryption, DNA cryptography, IPFS storage, and Ethereum blockchain for maximum security. Users can upload files which are encrypted, stored on IPFS, and tracked on blockchain with DNA-encoded keys.

## Recent Changes
- 2025-11-04: Initial project setup with all core modules
- Created DNA cryptography module for encoding/decoding keys
- Implemented AES encryption/decryption utilities
- Added IPFS integration with simulation mode fallback
- Built Solidity smart contract for file registry
- Created blockchain interaction module with Web3.py
- Developed Flask server with upload/download endpoints
- Designed responsive web UI with progress tracking

## Project Architecture

### Core Modules
- **server.py**: Flask web application with API endpoints
- **blockchain.py**: Ethereum blockchain interaction via Web3.py
- **dna_crypto.py**: DNA sequence encoding/decoding (A,T,C,G)
- **aes_utils.py**: AES-256 encryption/decryption
- **ipfs_utils.py**: IPFS file storage (with simulation mode)
- **config.py**: Configuration management
- **FileRegistry.sol**: Solidity smart contract

### Frontend
- Modern responsive design with gradient theme
- Real-time progress tracking for upload/download
- System status monitoring
- File list management

### Security Layers
1. AES-256-CBC encryption for files
2. DNA cryptography for key protection
3. IPFS for decentralized storage
4. Blockchain for immutable records

## Dependencies
- Flask 3.0.0
- web3 6.11.3
- pycryptodome 3.19.0
- py-solc-x 2.0.2
- requests 2.31.0
- python-dotenv 1.0.0

## Running Modes
- **Full mode**: Requires Ganache blockchain and IPFS daemon
- **Simulation mode**: Works without external dependencies (default)

## Notes
- The system runs on port 5000
- Files are stored in: uploads/, encrypted/, decrypted/, ipfs_storage/
- Smart contract ABI is saved to contract_abi.json after deployment
- Default Ganache private key is used for development
