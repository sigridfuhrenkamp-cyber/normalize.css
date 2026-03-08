#!/usr/bin/env python3
"""
Advanced steganographic analysis of normalize.css
Looking for hidden patterns in comments, whitespace, and structure
"""

import re
import binascii
import string
from collections import Counter

def analyze_whitespace_steganography(content):
    """Analyze whitespace patterns for hidden data"""
    print("=== WHITESPACE STEGANOGRAPHY ANALYSIS ===")
    
    # Extract all whitespace sequences
    whitespace_patterns = re.findall(r'\s+', content)
    
    # Analyze tab/space patterns
    tab_space_patterns = []
    for pattern in whitespace_patterns:
        binary_pattern = ''.join(['1' if c == '\t' else '0' for c in pattern])
        if len(binary_pattern) > 1:
            tab_space_patterns.append(binary_pattern)
    
    print(f"Found {len(tab_space_patterns)} significant whitespace patterns")
    
    # Try to decode as binary
    for i, pattern in enumerate(tab_space_patterns[:10]):  # First 10 patterns
        try:
            # Pad to multiple of 8
            padded = pattern.ljust((len(pattern) + 7) // 8 * 8, '0')
            # Convert to bytes
            bytes_data = int(padded, 2).to_bytes(len(padded) // 8, 'big')
            decoded = bytes_data.decode('utf-8', errors='ignore')
            if decoded.isprintable() and len(decoded) > 0:
                print(f"Pattern {i}: {pattern[:32]}... -> '{decoded}'")
        except:
            pass
    
    return tab_space_patterns

def analyze_comment_steganography(content):
    """Analyze comments for hidden patterns"""
    print("\n=== COMMENT STEGANOGRAPHY ANALYSIS ===")
    
    # Extract all comments
    comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)
    print(f"Found {len(comments)} comment blocks")
    
    hidden_data = []
    
    for i, comment in enumerate(comments):
        # Look for unusual character patterns
        clean_comment = re.sub(r'\s+', '', comment)
        
        # Check for suspicious character sequences
        if len(clean_comment) > 20:
            # Try to extract every Nth character
            for step in [2, 3, 4, 5, 7, 8, 13, 16]:
                extracted = ''.join(clean_comment[::step])
                if len(extracted) > 5 and all(c in string.printable for c in extracted):
                    # Check if it looks like encoded data
                    if re.match(r'^[A-Za-z0-9+/=]+$', extracted):
                        try:
                            import base64
                            decoded = base64.b64decode(extracted + '==')
                            if decoded.isascii():
                                print(f"Comment {i}, step {step}: Hidden data found")
                                print(f"  Extracted: {extracted[:50]}...")
                                print(f"  Decoded: {decoded.decode('ascii', errors='ignore')[:50]}...")
                                hidden_data.append(decoded.decode('ascii', errors='ignore'))
                        except:
                            pass
    
    return hidden_data

def analyze_line_length_patterns(content):
    """Analyze line lengths for encoding patterns"""
    print("\n=== LINE LENGTH PATTERN ANALYSIS ===")
    
    lines = content.split('\n')
    lengths = [len(line) for line in lines]
    
    # Look for patterns in line lengths
    length_diffs = [abs(lengths[i] - lengths[i-1]) for i in range(1, len(lengths))]
    
    # Check for suspicious patterns
    binary_pattern = ''.join(['1' if diff > 0 else '0' for diff in length_diffs])
    
    # Try to decode as ASCII
    try:
        padded = binary_pattern.ljust((len(binary_pattern) + 7) // 8 * 8, '0')
        if len(padded) >= 8:
            bytes_data = int(padded, 2).to_bytes(len(padded) // 8, 'big')
            decoded = bytes_data.decode('ascii', errors='ignore')
            if any(c.isalnum() for c in decoded):
                print(f"Line length pattern may encode: '{decoded[:50]}...'")
    except:
        pass
    
    return lengths

def analyze_css_selector_patterns(content):
    """Analyze CSS selectors for hidden patterns"""
    print("\n=== CSS SELECTOR PATTERN ANALYSIS ===")
    
    # Extract selectors
    selectors = re.findall(r'^([a-zA-Z0-9\-\_\[\]:\.,\s]+)\s*{', content, re.MULTILINE)
    
    # Look for patterns in selector names
    selector_chars = ''.join([s.strip() for s in selectors])
    
    # Check for character frequency anomalies
    char_counts = Counter(selector_chars)
    total_chars = sum(char_counts.values())
    
    print(f"Analyzed {len(selectors)} selectors")
    print(f"Total characters in selectors: {total_chars}")
    
    # Look for suspicious character distributions
    suspicious_chars = [char for char, count in char_counts.items() 
                        if count / total_chars > 0.15 and char.isalnum()]
    
    if suspicious_chars:
        print(f"Suspicious character frequencies: {suspicious_chars}")
    
    return selectors

def analyze_property_value_patterns(content):
    """Analyze CSS property values for encoding"""
    print("\n=== PROPERTY VALUE PATTERN ANALYSIS ===")
    
    # Extract property values
    values = re.findall(r':\s*([^;]+);', content)
    
    # Look for numeric patterns
    numeric_values = []
    for value in values:
        nums = re.findall(r'[\d.]+', value)
        numeric_values.extend([float(n) for n in nums])
    
    # Check if numbers form a pattern
    if len(numeric_values) > 10:
        # Convert to binary representation
        binary_data = ''.join(['1' if n > 1 else '0' for n in numeric_values[:64]])
        
        try:
            if len(binary_data) >= 8:
                bytes_data = int(binary_data, 2).to_bytes(len(binary_data) // 8, 'big')
                decoded = bytes_data.decode('ascii', errors='ignore')
                if any(c.isalnum() for c in decoded):
                    print(f"Numeric pattern may encode: '{decoded[:50]}...'")
        except:
            pass
    
    return values

def advanced_entropy_analysis(content):
    """Advanced entropy analysis for hidden data"""
    print("\n=== ADVANCED ENTROPY ANALYSIS ===")
    
    # Calculate entropy of different sections
    sections = {
        'comments': re.findall(r'/\*.*?\*/', content, re.DOTALL),
        'selectors': re.findall(r'^([a-zA-Z0-9\-\_\[\]:\.,\s]+)\s*{', content, re.MULTILINE),
        'properties': re.findall(r':\s*([^;]+);', content)
    }
    
    for section_name, items in sections.items():
        if items:
            text = ''.join(str(item) for item in items)
            entropy = calculate_entropy(text)
            print(f"{section_name} entropy: {entropy:.4f}")
            
            # High entropy might indicate encryption/encoding
            if entropy > 6.0:
                print(f"  WARNING: High entropy in {section_name} - possible encrypted content")

import math

def calculate_entropy(text):
    """Calculate Shannon entropy of text"""
    if not text:
        return 0
    
    counts = Counter(text)
    total = len(text)
    entropy = 0
    
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy

def main():
    with open('normalize.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("ADVANCED STEGANOGRAPHIC ANALYSIS OF NORMALIZE.CSS")
    print("=" * 60)
    
    # Run all analyses
    analyze_whitespace_steganography(content)
    analyze_comment_steganography(content)
    analyze_line_length_patterns(content)
    analyze_css_selector_patterns(content)
    analyze_property_value_patterns(content)
    advanced_entropy_analysis(content)
    
    print("\n=== ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    main()
