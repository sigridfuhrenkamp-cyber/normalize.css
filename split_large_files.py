#!/usr/bin/env python3
"""
File splitter for large files (>100MB)
Splits files into chunks of maximum 99.9MB
"""

import os
import math

def split_large_files():
    """Split files larger than 100MB into chunks of 99.9MB"""
    print("=== LARGE FILE SPLITTER ===")
    print("Splitting files >100MB into chunks of 99.9MB maximum")
    
    # Find files larger than 100MB
    large_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                if file_size > 100 * 1024 * 1024:  # 100MB
                    large_files.append({
                        'path': file_path,
                        'size': file_size,
                        'size_mb': file_size / (1024 * 1024)
                    })
            except OSError:
                continue
    
    print(f"\nFound {len(large_files)} files >100MB:")
    for file_info in large_files:
        print(f"  {file_info['path']}: {file_info['size_mb']:.1f} MB")
    
    # Split each large file
    max_chunk_size = int(99.9 * 1024 * 1024)  # 99.9MB in bytes (convert to int)
    
    for file_info in large_files:
        file_path = file_info['path']
        file_size = file_info['size']
        
        print(f"\nSplitting: {file_path}")
        print(f"Original size: {file_info['size_mb']:.1f} MB")
        
        # Calculate number of chunks needed
        num_chunks = math.ceil(file_size / max_chunk_size)
        print(f"Will create {num_chunks} chunks")
        
        try:
            with open(file_path, 'rb') as f:
                chunk_num = 1
                while True:
                    chunk_data = f.read(max_chunk_size)
                    if not chunk_data:
                        break
                    
                    # Create chunk filename
                    base_name, ext = os.path.splitext(file_path)
                    chunk_filename = f"{base_name}_part{chunk_num}{ext}"
                    
                    # Write chunk
                    with open(chunk_filename, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)
                    
                    chunk_size_mb = len(chunk_data) / (1024 * 1024)
                    print(f"  Created: {chunk_filename} ({chunk_size_mb:.1f} MB)")
                    
                    chunk_num += 1
            
            # Remove original file after successful splitting
            os.remove(file_path)
            print(f"  Removed original: {file_path}")
            
        except Exception as e:
            print(f"  ERROR splitting {file_path}: {e}")
    
    print(f"\n=== FILE SPLITTING COMPLETE ===")

def main():
    split_large_files()

if __name__ == "__main__":
    main()
