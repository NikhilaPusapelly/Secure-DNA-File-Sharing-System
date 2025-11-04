"""
Blockchain Interaction Module
Handles connection to Ethereum network and smart contract interaction
"""

from web3 import Web3
import json
import os
from solcx import compile_standard, install_solc
import config


class BlockchainManager:
    
    def __init__(self):
        """Initialize blockchain connection"""
        self.w3 = Web3(Web3.HTTPProvider(config.GANACHE_URL))
        self.account = None
        self.contract = None
        self.contract_address = config.CONTRACT_ADDRESS
        
        self._setup_account()
        
        if self.contract_address:
            self._load_contract()
    
    def _setup_account(self):
        """Set up account from private key"""
        try:
            if config.GANACHE_PRIVATE_KEY.startswith('0x'):
                private_key = config.GANACHE_PRIVATE_KEY
            else:
                private_key = '0x' + config.GANACHE_PRIVATE_KEY
            
            self.account = self.w3.eth.account.from_key(private_key)
            print(f"Connected account: {self.account.address}")
        except Exception as e:
            print(f"Error setting up account: {e}")
            if self.w3.eth.accounts:
                self.account = self.w3.eth.accounts[0]
                print(f"Using default account: {self.account}")
    
    def is_connected(self):
        """Check if connected to blockchain"""
        return self.w3.is_connected()
    
    def compile_contract(self, contract_path='FileRegistry.sol'):
        """Compile Solidity contract"""
        try:
            install_solc('0.8.0')
        except:
            pass
        
        with open(contract_path, 'r') as file:
            contract_source = file.read()
        
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {
                    "FileRegistry.sol": {
                        "content": contract_source
                    }
                },
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                        }
                    }
                }
            },
            solc_version="0.8.0"
        )
        
        contract_id = "FileRegistry.sol:FileRegistry"
        bytecode = compiled_sol["contracts"]["FileRegistry.sol"]["FileRegistry"]["evm"]["bytecode"]["object"]
        abi = compiled_sol["contracts"]["FileRegistry.sol"]["FileRegistry"]["abi"]
        
        with open('contract_abi.json', 'w') as f:
            json.dump(abi, f, indent=2)
        
        return bytecode, abi
    
    def deploy_contract(self):
        """Deploy smart contract to blockchain"""
        if not self.is_connected():
            raise Exception("Not connected to blockchain")
        
        bytecode, abi = self.compile_contract()
        
        FileRegistry = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        if hasattr(self.account, 'address'):
            account_address = self.account.address
            nonce = self.w3.eth.get_transaction_count(account_address)
            
            transaction = FileRegistry.constructor().build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 3000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, config.GANACHE_PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        else:
            tx_hash = FileRegistry.constructor().transact({'from': self.account})
        
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.contract_address = tx_receipt.contractAddress
        
        with open('.env', 'a') as f:
            f.write(f"\nCONTRACT_ADDRESS={self.contract_address}\n")
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=abi
        )
        
        print(f"Contract deployed at: {self.contract_address}")
        return self.contract_address
    
    def _load_contract(self):
        """Load existing contract"""
        if not os.path.exists('contract_abi.json'):
            print("Contract ABI not found. Please deploy contract first.")
            return
        
        with open('contract_abi.json', 'r') as f:
            abi = json.load(f)
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=abi
        )
        print(f"Contract loaded at: {self.contract_address}")
    
    def store_file_record(self, ipfs_hash, dna_key, filename):
        """Store file record on blockchain"""
        if not self.contract:
            raise Exception("Contract not deployed or loaded")
        
        if hasattr(self.account, 'address'):
            account_address = self.account.address
            nonce = self.w3.eth.get_transaction_count(account_address)
            
            transaction = self.contract.functions.storeFile(
                ipfs_hash,
                dna_key,
                filename
            ).build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, config.GANACHE_PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        else:
            tx_hash = self.contract.functions.storeFile(
                ipfs_hash,
                dna_key,
                filename
            ).transact({'from': self.account})
        
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def get_file_record(self, ipfs_hash):
        """Retrieve file record from blockchain"""
        if not self.contract:
            raise Exception("Contract not deployed or loaded")
        
        result = self.contract.functions.getFile(ipfs_hash).call()
        
        return {
            'ipfs_hash': result[0],
            'dna_key': result[1],
            'filename': result[2],
            'timestamp': result[3],
            'uploader': result[4]
        }
    
    def get_all_files(self):
        """Get all file hashes from blockchain"""
        if not self.contract:
            raise Exception("Contract not deployed or loaded")
        
        return self.contract.functions.getAllFiles().call()


if __name__ == "__main__":
    manager = BlockchainManager()
    
    if manager.is_connected():
        print("Connected to blockchain!")
        
        if not manager.contract_address:
            print("Deploying contract...")
            address = manager.deploy_contract()
            print(f"Contract deployed at: {address}")
    else:
        print("Not connected to blockchain. Make sure Ganache is running.")
