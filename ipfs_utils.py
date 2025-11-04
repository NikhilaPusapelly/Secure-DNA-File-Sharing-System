"""
IPFS Utilities
Handles file upload and download from IPFS
"""

import requests
import io


class IPFSClient:
    
    def __init__(self, api_url='http://127.0.0.1:5001'):
        """Initialize IPFS client with API URL"""
        self.api_url = api_url
        self.available = self._check_availability()
    
    def _check_availability(self):
        """Check if IPFS daemon is running"""
        try:
            response = requests.get(f"{self.api_url}/api/v0/version", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def upload_file(self, file_data, filename='file'):
        """
        Upload file to IPFS
        Returns: IPFS hash (CID)
        """
        if not self.available:
            return self._simulate_upload(file_data, filename)
        
        try:
            files = {'file': (filename, io.BytesIO(file_data))}
            response = requests.post(
                f"{self.api_url}/api/v0/add",
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['Hash']
            else:
                return self._simulate_upload(file_data, filename)
        except Exception as e:
            print(f"IPFS upload error: {e}")
            return self._simulate_upload(file_data, filename)
    
    def download_file(self, ipfs_hash):
        """
        Download file from IPFS
        Returns: file data as bytes
        """
        if not self.available:
            return self._simulate_download(ipfs_hash)
        
        try:
            response = requests.post(
                f"{self.api_url}/api/v0/cat",
                params={'arg': ipfs_hash},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.content
            else:
                return self._simulate_download(ipfs_hash)
        except Exception as e:
            print(f"IPFS download error: {e}")
            return self._simulate_download(ipfs_hash)
    
    def _simulate_upload(self, file_data, filename):
        """Simulate IPFS upload when daemon is not available"""
        import hashlib
        import os
        
        os.makedirs('ipfs_storage', exist_ok=True)
        
        file_hash = hashlib.sha256(file_data).hexdigest()
        ipfs_hash = f"Qm{file_hash[:44]}"
        
        storage_path = f"ipfs_storage/{ipfs_hash}"
        with open(storage_path, 'wb') as f:
            f.write(file_data)
        
        print(f"[SIMULATED] IPFS upload: {ipfs_hash}")
        return ipfs_hash
    
    def _simulate_download(self, ipfs_hash):
        """Simulate IPFS download when daemon is not available"""
        import os
        
        storage_path = f"ipfs_storage/{ipfs_hash}"
        
        if os.path.exists(storage_path):
            with open(storage_path, 'rb') as f:
                data = f.read()
            print(f"[SIMULATED] IPFS download: {ipfs_hash}")
            return data
        else:
            raise FileNotFoundError(f"File not found in simulated IPFS storage: {ipfs_hash}")


if __name__ == "__main__":
    client = IPFSClient()
    
    test_data = b"This is a test file for IPFS!"
    print(f"Test data: {test_data}")
    
    ipfs_hash = client.upload_file(test_data, "test.txt")
    print(f"IPFS Hash: {ipfs_hash}")
    
    downloaded = client.download_file(ipfs_hash)
    print(f"Downloaded: {downloaded}")
    
    print(f"Match: {test_data == downloaded}")
