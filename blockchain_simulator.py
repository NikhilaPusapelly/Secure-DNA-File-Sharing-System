"""
Blockchain Simulator for local demonstration
Stores file records in a JSON file to simulate blockchain storage
"""

import json
import os
from datetime import datetime


class BlockchainSimulator:
    
    def __init__(self, storage_file='blockchain_storage.json'):
        self.storage_file = storage_file
        self.records = self._load_records()
        self.contract_address = "0xSimulatedContract"
    
    def _load_records(self):
        """Load records from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_records(self):
        """Save records to JSON file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.records, f, indent=2)
    
    def store_file_record(self, ipfs_hash, dna_key, filename):
        """Store file record (simulating blockchain transaction)"""
        self.records[ipfs_hash] = {
            'ipfs_hash': ipfs_hash,
            'dna_key': dna_key,
            'filename': filename,
            'timestamp': int(datetime.now().timestamp()),
            'uploader': '0xSimulatedAddress'
        }
        self._save_records()
        
        print(f"[SIMULATED BLOCKCHAIN] Stored record for {filename}")
        return {'transactionHash': f'0xsimulated_{ipfs_hash[:16]}'}
    
    def get_file_record(self, ipfs_hash):
        """Retrieve file record (simulating blockchain query)"""
        if ipfs_hash not in self.records:
            raise Exception(f"File not found: {ipfs_hash}")
        
        record = self.records[ipfs_hash]
        print(f"[SIMULATED BLOCKCHAIN] Retrieved record for {record['filename']}")
        return record
    
    def get_all_files(self):
        """Get all file hashes (simulating blockchain query)"""
        return list(self.records.keys())
    
    def is_connected(self):
        """Always returns True for simulator"""
        return True


if __name__ == "__main__":
    simulator = BlockchainSimulator()
    
    simulator.store_file_record(
        "QmTest123",
        "ATCGATCGATCG",
        "test.txt"
    )
    
    record = simulator.get_file_record("QmTest123")
    print(f"Retrieved: {record}")
    
    all_files = simulator.get_all_files()
    print(f"All files: {all_files}")
