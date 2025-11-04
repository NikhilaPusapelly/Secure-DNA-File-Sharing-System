"""
Flask Server for Secure File Sharing System
Handles file upload, encryption, IPFS storage, and blockchain recording
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import traceback

from aes_utils import AESCipher
from dna_crypto import DNACrypto
from ipfs_utils import IPFSClient
from blockchain import BlockchainManager
from blockchain_simulator import BlockchainSimulator
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

ipfs_client = IPFSClient(config.IPFS_API_URL)
blockchain_manager = None


def initialize_blockchain():
    """Initialize blockchain manager and deploy contract if needed"""
    global blockchain_manager
    try:
        real_blockchain = BlockchainManager()
        
        if real_blockchain.is_connected():
            print("✓ Connected to real Ethereum blockchain")
            
            if not real_blockchain.contract_address:
                print("Deploying smart contract...")
                real_blockchain.deploy_contract()
                print("✓ Contract deployed successfully")
            else:
                print(f"✓ Using existing contract at {real_blockchain.contract_address}")
            
            blockchain_manager = real_blockchain
        else:
            print("⚠ Real blockchain not available - using local simulation mode")
            blockchain_manager = BlockchainSimulator()
            print("✓ Blockchain simulator initialized (perfect for local demo!)")
    except Exception as e:
        print(f"⚠ Blockchain initialization error: {e}")
        print("✓ Using blockchain simulator for local demonstration")
        blockchain_manager = BlockchainSimulator()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/upload')
def upload_page():
    """Upload page"""
    blockchain_status = blockchain_manager is not None and blockchain_manager.is_connected()
    ipfs_status = ipfs_client.available
    return render_template('upload.html', blockchain_status=blockchain_status, ipfs_status=ipfs_status)


@app.route('/download')
def download_page():
    """Download page"""
    blockchain_status = blockchain_manager is not None and blockchain_manager.is_connected()
    return render_template('download.html', blockchain_status=blockchain_status)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload file endpoint
    Process: File -> AES Encrypt -> DNA Encode Key -> Upload to IPFS -> Store on Blockchain
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        file_data = file.read()
        
        print(f"Processing file: {filename} ({len(file_data)} bytes)")
        
        aes_key = AESCipher.generate_key()
        print(f"Generated AES key: {aes_key.hex()[:32]}...")
        
        encrypted_data, iv = AESCipher.encrypt_file(file_data, aes_key)
        print(f"File encrypted: {len(encrypted_data)} bytes")
        
        key_with_iv = iv + aes_key
        dna_encoded_key = DNACrypto.encode_key(key_with_iv)
        print(f"DNA encoded key: {dna_encoded_key[:64]}...")
        
        encrypted_file_data = iv + encrypted_data
        ipfs_hash = ipfs_client.upload_file(encrypted_file_data, filename)
        print(f"Uploaded to IPFS: {ipfs_hash}")
        
        if blockchain_manager and blockchain_manager.is_connected():
            tx_receipt = blockchain_manager.store_file_record(
                ipfs_hash,
                dna_encoded_key,
                filename
            )
            if hasattr(tx_receipt, 'transactionHash'):
                blockchain_tx = tx_receipt.transactionHash.hex()
            elif isinstance(tx_receipt, dict) and 'transactionHash' in tx_receipt:
                blockchain_tx = tx_receipt['transactionHash']
            else:
                blockchain_tx = str(tx_receipt)
            print(f"Stored on blockchain: {blockchain_tx}")
        else:
            return jsonify({'error': 'Blockchain not available - cannot store file record'}), 503
        
        return jsonify({
            'success': True,
            'filename': filename,
            'ipfs_hash': ipfs_hash,
            'dna_key': dna_encoded_key[:100] + '...' if len(dna_encoded_key) > 100 else dna_encoded_key,
            'blockchain_tx': blockchain_tx,
            'file_size': len(file_data),
            'encrypted_size': len(encrypted_data)
        })
    
    except Exception as e:
        print(f"Upload error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download_file():
    """
    Download file endpoint
    Process: Get from Blockchain -> Decode DNA Key -> Download from IPFS -> AES Decrypt
    """
    try:
        data = request.get_json()
        ipfs_hash = data.get('ipfs_hash')
        
        if not ipfs_hash:
            return jsonify({'error': 'No IPFS hash provided'}), 400
        
        print(f"Retrieving file: {ipfs_hash}")
        
        if blockchain_manager and blockchain_manager.is_connected():
            try:
                file_record = blockchain_manager.get_file_record(ipfs_hash)
                dna_key = file_record['dna_key']
                original_filename = file_record['filename']
                print(f"Retrieved from blockchain: {original_filename}")
            except Exception as e:
                print(f"Blockchain retrieval error: {e}")
                return jsonify({'error': 'File not found on blockchain'}), 404
        else:
            return jsonify({'error': 'Blockchain not available - cannot retrieve DNA key'}), 503
        
        key_with_iv = DNACrypto.decode_key(dna_key)
        iv = key_with_iv[:16]
        aes_key = key_with_iv[16:]
        print(f"Decoded AES key from DNA")
        
        encrypted_file_data = ipfs_client.download_file(ipfs_hash)
        print(f"Downloaded from IPFS: {len(encrypted_file_data)} bytes")
        
        file_iv = encrypted_file_data[:16]
        encrypted_data = encrypted_file_data[16:]
        
        decrypted_data = AESCipher.decrypt_file(encrypted_data, aes_key, file_iv)
        print(f"File decrypted: {len(decrypted_data)} bytes")
        
        output_path = os.path.join(config.DECRYPTED_FOLDER, original_filename)
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        return jsonify({
            'success': True,
            'filename': original_filename,
            'file_size': len(decrypted_data),
            'download_path': output_path
        })
    
    except Exception as e:
        print(f"Download error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/files', methods=['GET'])
def list_files():
    """List all files stored on blockchain"""
    try:
        if not blockchain_manager or not blockchain_manager.is_connected():
            return jsonify({'error': 'Blockchain not available'}), 503
        
        file_hashes = blockchain_manager.get_all_files()
        files = []
        
        for ipfs_hash in file_hashes:
            try:
                record = blockchain_manager.get_file_record(ipfs_hash)
                files.append({
                    'ipfs_hash': record['ipfs_hash'],
                    'filename': record['filename'],
                    'timestamp': record['timestamp'],
                    'uploader': record['uploader']
                })
            except:
                continue
        
        return jsonify({'files': files})
    
    except Exception as e:
        print(f"List files error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def system_status():
    """Get system status"""
    blockchain_connected = blockchain_manager is not None and blockchain_manager.is_connected()
    
    return jsonify({
        'blockchain': {
            'connected': blockchain_connected,
            'contract_address': blockchain_manager.contract_address if blockchain_connected else None
        },
        'ipfs': {
            'available': ipfs_client.available,
            'mode': 'daemon' if ipfs_client.available else 'simulated'
        }
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Secure File Sharing System with Blockchain & DNA Cryptography")
    print("=" * 60)
    
    initialize_blockchain()
    
    print("\nStarting Flask server...")
    print("Access the application at: http://0.0.0.0:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
