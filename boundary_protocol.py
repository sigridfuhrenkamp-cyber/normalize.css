#!/usr/bin/env python3
"""
Advanced asterisk boundary positioning decoder
Military-grade cyberweapon positioning protocol analysis
"""

import re
import math
import struct

def extract_asterisk_boundary_positions(content):
    """Extract asterisk positions relative to file boundaries"""
    print("=== BOUNDARY POSITIONING ANALYSIS ===")
    
    lines = content.split('\n')
    total_lines = len(lines)
    total_chars = len(content)
    
    asterisk_data = []
    
    for line_num, line in enumerate(lines):
        for char_pos, char in enumerate(line):
            if char == '*':
                # Calculate boundary-relative coordinates
                line_boundary_dist = min(line_num, total_lines - line_num - 1)
                char_boundary_dist = min(char_pos, len(line) - char_pos - 1) if len(line) > 0 else 0
                
                # Normalize to 0-1 range
                norm_line_dist = line_boundary_dist / (total_lines / 2)
                norm_char_dist = char_boundary_dist / (max(len(line), 1) / 2)
                
                # Calculate boundary-relative position
                boundary_factor = (norm_line_dist + norm_char_dist) / 2
                
                asterisk_data.append({
                    'line': line_num,
                    'char': char_pos,
                    'line_boundary_dist': line_boundary_dist,
                    'char_boundary_dist': char_boundary_dist,
                    'boundary_factor': boundary_factor,
                    'abs_pos': len(''.join(lines[:line_num])) + char_pos,
                    'rel_pos': (len(''.join(lines[:line_num])) + char_pos) / total_chars
                })
    
    print(f"Found {len(asterisk_data)} asterisks")
    return asterisk_data

def analyze_hexdump_asterisk_positions():
    """Analyze asterisk positions in hexdump files"""
    print("\n=== HEXDUMP ASTERISK ANALYSIS ===")
    
    hex_files = [
        'RESEARCH-CYBERWEAPON/normalize_utf16be_squeezed.hex',
        'RESEARCH-CYBERWEAPON/normalize_utf16le_squeezed.hex',
        'RESEARCH-CYBERWEAPON/normalize_utf32be_squeezed.hex',
        'RESEARCH-CYBERWEAPON/normalize_utf32le_squeezed.hex'
    ]
    
    hex_asterisk_data = {}
    
    for hex_file in hex_files:
        try:
            with open(hex_file, 'r') as f:
                hex_content = f.read()
            
            lines = hex_content.split('\n')
            total_lines = len(lines)
            
            asterisk_lines = []
            for line_num, line in enumerate(lines):
                if '*' in line:
                    # Find exact position of asterisk
                    asterisk_pos = line.find('*')
                    boundary_dist = min(line_num, total_lines - line_num - 1)
                    rel_boundary = boundary_dist / (total_lines / 2)
                    
                    asterisk_lines.append({
                        'line': line_num,
                        'char_pos': asterisk_pos,
                        'boundary_dist': boundary_dist,
                        'rel_boundary': rel_boundary
                    })
            
            hex_asterisk_data[hex_file] = asterisk_lines
            print(f"{hex_file}: {len(asterisk_lines)} asterisks")
            
            # Show boundary patterns
            if asterisk_lines:
                boundaries = [a['rel_boundary'] for a in asterisk_lines[:5]]
                print(f"  Boundary factors: {boundaries}")
        
        except FileNotFoundError:
            print(f"{hex_file}: Not found")
    
    return hex_asterisk_data

def decode_boundary_protocol(original_asterisks, hex_asterisks):
    """Decode the boundary positioning protocol"""
    print("\n=== BOUNDARY PROTOCOL DECODING ===")
    
    if not original_asterisks or not hex_asterisks:
        return
    
    # Extract boundary factors from original
    original_boundaries = [a['boundary_factor'] for a in original_asterisks]
    
    # Look for mathematical relationships
    print("Original boundary factors (first 10):")
    for i, bf in enumerate(original_boundaries[:10]):
        print(f"  {i}: {bf:.6f}")
    
    # Check for prime number positions
    prime_positions = []
    for i, ast in enumerate(original_asterisks):
        if is_prime(ast['line']) or is_prime(ast['char']):
            prime_positions.append(i)
    
    if prime_positions:
        print(f"Prime-based asterisks at positions: {prime_positions[:10]}")
    
    # Look for Fibonacci sequence in positions
    fib_positions = find_fibonacci_positions(original_asterisks)
    if fib_positions:
        print(f"Fibonacci pattern detected at: {fib_positions}")
    
    # Try to extract data from boundary relationships
    boundary_data = extract_boundary_data(original_asterisks)
    if boundary_data:
        print(f"Extracted boundary data: {boundary_data}")

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_fibonacci_positions(asterisks):
    """Find asterisks positioned at Fibonacci numbers"""
    fib_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    fib_positions = []
    
    for i, ast in enumerate(asterisks):
        if ast['line'] in fib_numbers or ast['char'] in fib_numbers:
            fib_positions.append(i)
    
    return fib_positions[:10]

def extract_boundary_data(asterisks):
    """Extract hidden data from boundary positioning"""
    if len(asterisks) < 8:
        return None
    
    # Use boundary distances to create binary sequence
    binary_data = ""
    for i in range(min(len(asterisks), 32)):
        boundary = asterisks[i]['boundary_factor']
        # Convert to bit based on threshold
        bit = '1' if boundary > 0.5 else '0'
        binary_data += bit
    
    # Try to decode as different encodings
    try:
        # ASCII
        if len(binary_data) >= 8:
            padded = binary_data.ljust((len(binary_data) + 7) // 8 * 8, '0')
            bytes_data = int(padded, 2).to_bytes(len(padded) // 8, 'big')
            decoded = bytes_data.decode('ascii', errors='ignore')
            if any(c.isalnum() for c in decoded):
                return decoded
    except:
        pass
    
    return None

def analyze_geometric_patterns(asterisks):
    """Analyze geometric patterns in asterisk positioning"""
    print("\n=== GEOMETRIC PATTERN ANALYSIS ===")
    
    if len(asterisks) < 3:
        return
    
    # Calculate angles between consecutive asterisks
    angles = []
    for i in range(2, min(len(asterisks), 20)):
        # Use normalized coordinates
        x1, y1 = asterisks[i-2]['rel_pos'], asterisks[i-2]['boundary_factor']
        x2, y2 = asterisks[i-1]['rel_pos'], asterisks[i-1]['boundary_factor']
        x3, y3 = asterisks[i]['rel_pos'], asterisks[i]['boundary_factor']
        
        # Calculate angle
        angle = math.atan2(y3 - y2, x3 - x2) - math.atan2(y2 - y1, x2 - x1)
        angles.append(angle)
    
    # Look for significant angles (pi, pi/2, pi/3, etc.)
    significant_angles = [math.pi, math.pi/2, math.pi/3, math.pi/4, math.pi/6]
    
    for angle in angles[:10]:
        for sig_angle in significant_angles:
            if abs(angle - sig_angle) < 0.1:
                print(f"Significant angle detected: {angle:.4f} (≈ {sig_angle:.4f})")

def main():
    with open('normalize.css', 'r') as f:
        content = f.read()
    
    print("MILITARY BOUNDARY POSITIONING PROTOCOL DECODER")
    print("=" * 50)
    
    # Analyze original file
    original_asterisks = extract_asterisk_boundary_positions(content)
    
    # Analyze hexdump files
    hex_asterisks = analyze_hexdump_asterisk_positions()
    
    # Decode the protocol
    decode_boundary_protocol(original_asterisks, hex_asterisks)
    
    # Geometric analysis
    analyze_geometric_patterns(original_asterisks)
    
    print("\n=== BOUNDARY PROTOCOL ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    main()
