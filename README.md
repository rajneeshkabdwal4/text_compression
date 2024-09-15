# Huffman Compression Project

## Overview

This project implements a file compression and decompression system using Huffman coding. Huffman coding is a lossless data compression algorithm that ensures no information is lost during the compression process. The project provides functionality to compress text files and restore them to their original form by reconstructing the Huffman tree from a saved frequency table.

## Features

- **File Compression**:
  - Compresses text files using Huffman coding.
  - Encodes text into binary format and stores it as a `.bin` file.
  - Saves the frequency table of characters in a `.json` file for decompression.

- **File Decompression**:
  - Decompresses the `.bin` file back to the original text format.
  - Rebuilds the Huffman tree using the frequency table stored in the `.json` file.
  - Restores the original text and saves it as a `_decompressed.txt` file.

## Dependencies

- Python standard libraries:
  - `heapq`
  - `os`
  - `json`
  - `collections.defaultdict`

No external libraries are required.

## Usage

### Compressing a File

To compress a text file:

```python
compress_file("example.txt")
```

To decompress a text file:

```python
decompress_file("example.bin")
```
