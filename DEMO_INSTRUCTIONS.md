# Secure File Sharing System - Demo Instructions

## System Status

You now have a **REAL local blockchain demonstration** running!

### Running Components

1. **Ganache Blockchain** (Port 8000)
   - Local Ethereum blockchain
   - 10 test accounts with 1000 ETH each
   - Smart contract deployed at: `0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab`

2. **Flask Server** (Port 5000)  
   - Web interface at: http://localhost:5000
   - Connected to real blockchain
   - IPFS simulation mode (local storage)

## How to Test the Complete Workflow

### Step 1: Upload a File

1. Go to http://localhost:5000
2. Click "Upload File" button
3. Select any file (PDF, image, text file, etc.)
4. Click "Encrypt & Upload"
5. Watch the progress:
   - ✓ Encrypting with AES-256
   - ✓ Encoding key to DNA  
   - ✓ Uploading to IPFS
   - ✓ Recording on blockchain (REAL transaction!)
6. Copy the IPFS hash shown (e.g., `QmX...`)

### Step 2: Download the File

1. Click "Download File" or go to http://localhost:5000/download
2. Paste the IPFS hash you copied
3. Click "Retrieve & Decrypt"
4. Watch the progress:
   - ✓ Retrieving from blockchain (REAL blockchain query!)
   - ✓ Decoding DNA key
   - ✓ Downloading from IPFS  
   - ✓ Decrypting file
5. File will be saved to `decrypted/` folder

### Step 3: View All Files

On the download page, click "Refresh File List" to see all files stored on the blockchain!

## What's Happening Behind the Scenes

### Upload Process
1. File is encrypted with AES-256 (random key)
2. AES key is converted to DNA sequence (A, T, C, G)
3. Encrypted file is stored in simulated IPFS
4. **REAL blockchain transaction** stores:
   - IPFS hash
   - DNA-encoded encryption key
   - Original filename
   - Timestamp
   - Uploader address

### Download Process
1. **REAL blockchain query** retrieves file metadata
2. DNA sequence is decoded back to AES key
3. Encrypted file is downloaded from IPFS simulation
4. File is decrypted using the recovered AES key
5. Original file is restored

## Blockchain Details

**Network:** Local Ganache (Ethereum)
**Chain ID:** 1337
**Smart Contract:** FileRegistry.sol
**Contract Address:** 0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab
**Account Used:** 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 (1000 ETH)

## Files Created During Demo

- `uploads/` - Original files (temporary)
- `encrypted/` - Encrypted files (temporary)
- `decrypted/` - Decrypted downloaded files
- `ipfs_storage/` - Simulated IPFS storage
- `blockchain_storage.json` - Simulator backup (fallback only)
- `contract_abi.json` - Smart contract ABI

## Technology Stack

- **Blockchain:** Ganache (local Ethereum)
- **Smart Contract:** Solidity
- **Backend:** Python + Flask + Web3.py
- **Encryption:** AES-256-CBC (PyCryptodome)
- **DNA Encoding:** Custom binary-to-DNA algorithm
- **Storage:** IPFS simulation
- **Frontend:** HTML + CSS + JavaScript

## Stop/Restart

Both services run automatically:
- Flask server will restart when you modify code
- Ganache blockchain persists until manually stopped

## Notes

- This is a **LOCAL demonstration** - everything runs on localhost
- The blockchain is REAL (Ganache) - actual Ethereum transactions!
- IPFS is simulated for easy local testing
- DNA encoding is for demonstration - see README for security notes
