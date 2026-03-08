#!/usr/bin/env python3
"""
Military-grade asterisk positioning analysis
Decoding cyberweapon positioning protocol
"""

import re
import math

def analyze_asterisk_positions(content):
    """Analyze asterisk positions relative to file boundaries"""
    print("=== ASTERISK POSITIONING ANALYSIS ===")
    
    positions = []
    lines = content.split('\n')
    total_lines = len(lines)
    total_chars = len(content)
    
    for line_num, line in enumerate(lines):
        for char_pos, char in enumerate(line):
            if char == '*':
                # Calculate relative positions
                rel_line = line_num / total_lines
                rel_char = char_pos / len(line) if len(line) > 0 else 0
                abs_pos = content.find('*', len(''.join(lines[:line_num])) + char_pos)
                rel_abs = abs_pos / total_chars
                
                positions.append({
                    'line': line_num,
                    'char': char_pos,
                    'rel_line': rel_line,
                    'rel_char': rel_char,
                    'abs_pos': abs_pos,
                    'rel_abs': rel_abs
                })
    
    print(f"Found {len(positions)} asterisks")
    
    # Look for mathematical patterns
    if len(positions) >= 2:
        # Calculate distances between consecutive asterisks
        distances = []
        for i in range(1, len(positions)):
            dist = math.sqrt(
                (positions[i]['rel_line'] - positions[i-1]['rel_line'])**2 +
                (positions[i]['rel_char'] - positions[i-1]['rel_char'])**2
            )
            distances.append(dist)
        
        print(f"Average distance: {sum(distances)/len(distances):.6f}")
        
        # Check for golden ratio or other mathematical constants
        golden_ratio = (1 + math.sqrt(5)) / 2
        for i, dist in enumerate(distances[:5]):
            ratio = dist / golden_ratio
            if 0.9 < ratio < 1.1:
                print(f"Golden ratio pattern detected at position {i}")
    
    return positions

def compare_with_hexdump():
    """Compare with squeezed hexdump positions"""
    print("\n=== HEXDUMP COMPARISON ===")
    
    try:
        with open('RESEARCH-CYBERWEAPON/normalize_utf16be_squeezed.hex', 'r') as f:
            hex_content = f.read()
        
        # Find asterisk positions in hexdump
        hex_asterisks = []
        for i, line in enumerate(hex_content.split('\n')):
            if '*' in line:
                hex_asterisks.append(i)
        
        print(f"Found {len(hex_asterisks)} asterisks in hexdump")
        
        # Look for positioning correlation
        if len(hex_asterisks) > 0:
            print(f"Hexdump asterisk lines: {hex_asterisks[:10]}")
            
            # Check for boundary-relative patterns
            total_hex_lines = len(hex_content.split('\n'))
            for pos in hex_asterisks[:5]:
                rel_pos = pos / total_hex_lines
                print(f"Relative position: {rel_pos:.6f}")
    
    except FileNotFoundError:
        print("Hexdump file not found")

def decode_positioning_protocol(positions):
    """Attempt to decode military positioning protocol"""
    print("\n=== POSITIONING PROTOCOL DECODE ===")
    
    if len(positions) < 4:
        return
    
    # Extract coordinates as potential data
    coords = []
    for pos in positions:
        # Convert relative positions to integer coordinates
        x = int(pos['rel_line'] * 1000)
        y = int(pos['rel_char'] * 1000)
        coords.append((x, y))
    
    # Look for patterns in coordinates
    print("Coordinate sequence:")
    for i, (x, y) in enumerate(coords[:10]):
        print(f"  {i}: ({x}, {y})")
    
    # Try to extract binary data from coordinate differences
    if len(coords) > 1:
        binary_data = ""
        for i in range(1, min(len(coords), 20)):
            dx = coords[i][0] - coords[i-1][0]
            dy = coords[i][1] - coords[i-1][1]
            binary_data += '1' if dx > 0 else '0'
            binary_data += '1' if dy > 0 else '0'
        
        # Try to decode as ASCII
        try:
            if len(binary_data) >= 8:
                padded = binary_data.ljust((len(binary_data) + 7) // 8 * 8, '0')
                bytes_data = int(padded, 2).to_bytes(len(padded) // 8, 'big')
                decoded = bytes_data.decode('ascii', errors='ignore')
                if any(c.isalnum() for c in decoded):
                    print(f"Decoded data: '{decoded}'")
        except:
            pass

def main():
    with open('normalize.css', 'r') as f:
        content = f.read()
    
    print("MILITARY-GRADE ASTERISK POSITIONING DECODING")
    print("=" * 50)
    
    positions = analyze_asterisk_positions(content)
    compare_with_hexdump()
    decode_positioning_protocol(positions)
    
    print("\n=== DECODING COMPLETE ===")

if __name__ == "__main__":
    main()
