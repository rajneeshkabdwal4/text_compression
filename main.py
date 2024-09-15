import heapq
import os
from collections import defaultdict
import json
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(data):
    frequency = defaultdict(int)
    for char in data:
        frequency[char] += 1
    return frequency

def build_huffman_tree(frequency):
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(priority_queue, merged)
    
    return heapq.heappop(priority_queue)  # Root of the tree

def generate_huffman_codes(root):
    huffman_codes = {}
    
    def generate_codes_helper(node, current_code):
        if node is None:
            return
        
        if node.char is not None:  # It's a leaf node
            huffman_codes[node.char] = current_code
            return
        
        generate_codes_helper(node.left, current_code + '0')
        generate_codes_helper(node.right, current_code + '1')
    
    generate_codes_helper(root, "")
    return huffman_codes

def encode_data(data, huffman_codes):
    encoded_data = ""
    for char in data:
        encoded_data += huffman_codes[char]
    return encoded_data

def pad_encoded_data(encoded_data):
    extra_padding = 8 - len(encoded_data) % 8
    for _ in range(extra_padding):
        encoded_data += "0"
    
    padded_info = "{0:08b}".format(extra_padding)
    encoded_data = padded_info + encoded_data
    return encoded_data

def get_byte_array(padded_encoded_data):
    if len(padded_encoded_data) % 8 != 0:
        raise ValueError("Encoded data not padded properly")
    
    byte_array = bytearray()
    for i in range(0, len(padded_encoded_data), 8):
        byte = padded_encoded_data[i:i+8]
        byte_array.append(int(byte, 2))
    
    return byte_array

def compress_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    frequency = build_frequency_dict(data)
    huffman_tree_root = build_huffman_tree(frequency)
    huffman_codes = generate_huffman_codes(huffman_tree_root)

    encoded_data = encode_data(data, huffman_codes)
    padded_encoded_data = pad_encoded_data(encoded_data)
    byte_array = get_byte_array(padded_encoded_data)

    output_path = file_path.split('.')[0] + ".bin"
    with open(output_path, 'wb') as output_file:
        output_file.write(bytes(byte_array))

    # Save frequency table as JSON for decompression
    freq_file_path = file_path.split('.')[0] + "_freq.json"
    with open(freq_file_path, 'w') as freq_file:
        json.dump(frequency, freq_file)

    print(f"File compressed and saved as: {output_path}")
    print(f"Frequency table saved as: {freq_file_path}")


def remove_padding(padded_encoded_data):
    padded_info = padded_encoded_data[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_data = padded_encoded_data[8:]  # remove the padding info
    encoded_data = padded_encoded_data[:-extra_padding]  # remove the extra padding
    return encoded_data

def decode_data(encoded_data, huffman_tree_root):
    current_node = huffman_tree_root
    decoded_data = ""
    
    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        
        if current_node.char is not None:
            decoded_data += current_node.char
            current_node = huffman_tree_root

    return decoded_data

def decompress_file(file_path):
    with open(file_path, 'rb') as file:
        bit_string = ""
        byte = file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

    padded_encoded_data = bit_string
    encoded_data = remove_padding(padded_encoded_data)

    # Load frequency table from JSON
    freq_file_path = file_path.replace('.bin', '_freq.json')
    with open(freq_file_path, 'r') as freq_file:
        frequency = json.load(freq_file)

    huffman_tree_root = build_huffman_tree(frequency)
    decoded_data = decode_data(encoded_data, huffman_tree_root)

    original_file_path = file_path.replace('.bin', '_decompressed.txt')
    with open(original_file_path, 'w') as output_file:
        output_file.write(decoded_data)

    print(f"File decompressed and saved as: {original_file_path}")

if __name__ == "__main__":
    file_to_compress = "example.txt"
    compress_file(file_to_compress)

    compressed_file = "example.bin"
    decompress_file(compressed_file)
