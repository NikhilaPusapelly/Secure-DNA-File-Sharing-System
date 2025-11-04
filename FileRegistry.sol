// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileRegistry {
    
    struct FileRecord {
        string ipfsHash;
        string dnaKey;
        string filename;
        uint256 timestamp;
        address uploader;
    }
    
    mapping(string => FileRecord) public files;
    
    string[] public fileHashes;
    
    event FileStored(
        string indexed ipfsHash,
        string dnaKey,
        string filename,
        address indexed uploader,
        uint256 timestamp
    );
    
    function storeFile(
        string memory _ipfsHash,
        string memory _dnaKey,
        string memory _filename
    ) public {
        require(bytes(_ipfsHash).length > 0, "IPFS hash cannot be empty");
        require(bytes(_dnaKey).length > 0, "DNA key cannot be empty");
        require(bytes(files[_ipfsHash].ipfsHash).length == 0, "File already exists");
        
        files[_ipfsHash] = FileRecord({
            ipfsHash: _ipfsHash,
            dnaKey: _dnaKey,
            filename: _filename,
            timestamp: block.timestamp,
            uploader: msg.sender
        });
        
        fileHashes.push(_ipfsHash);
        
        emit FileStored(_ipfsHash, _dnaKey, _filename, msg.sender, block.timestamp);
    }
    
    function getFile(string memory _ipfsHash) public view returns (
        string memory ipfsHash,
        string memory dnaKey,
        string memory filename,
        uint256 timestamp,
        address uploader
    ) {
        FileRecord memory record = files[_ipfsHash];
        require(bytes(record.ipfsHash).length > 0, "File not found");
        
        return (
            record.ipfsHash,
            record.dnaKey,
            record.filename,
            record.timestamp,
            record.uploader
        );
    }
    
    function getAllFiles() public view returns (string[] memory) {
        return fileHashes;
    }
    
    function getFileCount() public view returns (uint256) {
        return fileHashes.length;
    }
}
