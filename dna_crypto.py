"""
DNA Cryptography Module
Converts binary data (AES keys) to DNA sequences and back
Uses A, T, C, G nucleotide encoding
"""

class DNACrypto:
    
    DNA_MAP = {
        '00': 'A',
        '01': 'T',
        '10': 'C',
        '11': 'G'
    }
    
    REVERSE_DNA_MAP = {v: k for k, v in DNA_MAP.items()}
    
    @staticmethod
    def binary_to_dna(binary_string):
        """Convert binary string to DNA sequence"""
        if len(binary_string) % 2 != 0:
            binary_string = '0' + binary_string
        
        dna_sequence = ''
        for i in range(0, len(binary_string), 2):
            pair = binary_string[i:i+2]
            dna_sequence += DNACrypto.DNA_MAP[pair]
        
        return dna_sequence
    
    @staticmethod
    def dna_to_binary(dna_sequence):
        """Convert DNA sequence back to binary string"""
        binary_string = ''
        for nucleotide in dna_sequence:
            binary_string += DNACrypto.REVERSE_DNA_MAP[nucleotide]
        
        return binary_string
    
    @staticmethod
    def bytes_to_dna(byte_data):
        """Convert bytes to DNA sequence"""
        binary_string = ''.join(format(byte, '08b') for byte in byte_data)
        return DNACrypto.binary_to_dna(binary_string)
    
    @staticmethod
    def dna_to_bytes(dna_sequence):
        """Convert DNA sequence back to bytes"""
        binary_string = DNACrypto.dna_to_binary(dna_sequence)
        
        byte_array = bytearray()
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i+8]
            if len(byte) == 8:
                byte_array.append(int(byte, 2))
        
        return bytes(byte_array)
    
    @staticmethod
    def encode_key(key_bytes):
        """Encode AES key bytes to DNA sequence"""
        return DNACrypto.bytes_to_dna(key_bytes)
    
    @staticmethod
    def decode_key(dna_sequence):
        """Decode DNA sequence back to AES key bytes"""
        return DNACrypto.dna_to_bytes(dna_sequence)


if __name__ == "__main__":
    test_key = b'This is a test key for DNA encoding!'
    print(f"Original key: {test_key}")
    
    dna_encoded = DNACrypto.encode_key(test_key)
    print(f"DNA encoded: {dna_encoded}")
    
    decoded_key = DNACrypto.decode_key(dna_encoded)
    print(f"Decoded key: {decoded_key}")
    
    print(f"Match: {test_key == decoded_key}")
