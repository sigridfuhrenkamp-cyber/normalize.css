#!/usr/bin/env python3
"""
Cryptographic and encrypted content analysis for normalize.css
Looking for NSA-grade hidden payloads and cryptographic signatures
"""

import re
import hashlib
import struct
import base64
import binascii
from collections import Counter

def scan_for_crypto_signatures(content):
    """Scan for cryptographic signatures and patterns"""
    print("=== CRYPTOGRAPHIC SIGNATURE SCAN ===")
    
    # Common crypto signatures
    crypto_patterns = {
        'RSA': re.findall(r'-----BEGIN [^-]+-----[^-]+-----END [^-]+-----', content),
        'PGP': re.findall(r'-----BEGIN PGP[^-]+-----[^-]+-----END PGP[^-]+-----', content),
        'CERT': re.findall(r'-----BEGIN CERTIFICATE-----[^-]+-----END CERTIFICATE-----', content),
        'HEX_32': re.findall(r'\b[A-Fa-f0-9]{32}\b', content),  # MD5-like
        'HEX_40': re.findall(r'\b[A-Fa-f0-9]{40}\b', content),  # SHA1-like
        'HEX_64': re.findall(r'\b[A-Fa-f0-9]{64}\b', content),  # SHA256-like
        'HEX_128': re.findall(r'\b[A-Fa-f0-9]{128}\b', content), # SHA512-like
        'BASE64': re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', content),
    }
    
    found_sigs = False
    for sig_type, matches in crypto_patterns.items():
        if matches:
            found_sigs = True
            print(f"Found {len(matches)} {sig_type} signatures:")
            for match in matches[:3]:  # Show first 3
                print(f"  {match[:50]}...")
    
    if not found_sigs:
        print("No obvious cryptographic signatures found")
    
    return crypto_patterns

def analyze_byte_patterns(content):
    """Analyze byte patterns for hidden crypto content"""
    print("\n=== BYTE PATTERN ANALYSIS ===")
    
    # Convert to bytes
    try:
        content_bytes = content.encode('utf-8')
    except:
        content_bytes = content.encode('latin-1', errors='ignore')
    
    # Look for repeating patterns (could indicate encryption)
    pattern_counts = Counter()
    
    # Check for 4-byte patterns
    for i in range(len(content_bytes) - 3):
        pattern = content_bytes[i:i+4]
        pattern_counts[pattern] += 1
    
    # Find most common patterns
    common_patterns = pattern_counts.most_common(10)
    print("Most common 4-byte patterns:")
    for pattern, count in common_patterns:
        if count > 5:  # Only show significant patterns
            hex_pattern = pattern.hex()
            try:
                ascii_pattern = pattern.decode('ascii', errors='ignore')
                if ascii_pattern.isprintable():
                    print(f"  {hex_pattern} ('{ascii_pattern}'): {count} times")
                else:
                    print(f"  {hex_pattern}: {count} times")
            except:
                print(f"  {hex_pattern}: {count} times")
    
    return common_patterns

def scan_for_steganographic_watermarks(content):
    """Advanced scan for steganographic watermarks"""
    print("\n=== STEGANOGRAPHIC WATERMARK SCAN ===")
    
    # Zero-width character scan
    zero_width_chars = {
        '\u200B': 'Zero Width Space',
        '\u200C': 'Zero Width Non-Joiner', 
        '\u200D': 'Zero Width Joiner',
        '\u2060': 'Word Joiner',
        '\uFEFF': 'Zero Width No-Break Space',
        '\u202A': 'Left-to-Right Embedding',
        '\u202B': 'Right-to-Left Embedding',
        '\u202C': 'Pop Directional Formatting',
        '\u202D': 'Left-to-Right Override',
        '\u202E': 'Right-to-Left Override'
    }
    
    found_watermarks = False
    for char, name in zero_width_chars.items():
        count = content.count(char)
        if count > 0:
            found_watermarks = True
            print(f"Found {count} instances of {name} (U+{ord(char):04X})")
    
    if not found_watermarks:
        print("No zero-width watermark characters found")
    
    # Check for invisible Unicode sequences
    invisible_ranges = [
        (0x2060, 0x206F),  # Invisible format characters
        (0xFE00, 0xFE0F),  # Variation selectors
        (0xE0000, 0xE007F), # Tags
    ]
    
    content_codepoints = [ord(c) for c in content]
    invisible_chars = []
    
    for cp in content_codepoints:
        for start, end in invisible_ranges:
            if start <= cp <= end:
                invisible_chars.append(cp)
    
    if invisible_chars:
        print(f"Found {len(invisible_chars)} invisible Unicode characters")
        print(f"Codepoints: {[hex(cp) for cp in invisible_chars[:10]]}")
    
    return found_watermarks

def analyze_entropy_distribution(content):
    """Detailed entropy analysis for encrypted content detection"""
    print("\n=== ENTROPY DISTRIBUTION ANALYSIS ===")
    
    # Analyze entropy in different chunks
    chunk_size = 256
    content_bytes = content.encode('utf-8')
    
    entropies = []
    for i in range(0, len(content_bytes), chunk_size):
        chunk = content_bytes[i:i+chunk_size]
        if len(chunk) > 0:
            entropy = calculate_chunk_entropy(chunk)
            entropies.append(entropy)
    
    if entropies:
        avg_entropy = sum(entropies) / len(entropies)
        max_entropy = max(entropies)
        min_entropy = min(entropies)
        
        print(f"Average entropy: {avg_entropy:.4f}")
        print(f"Max entropy: {max_entropy:.4f}")
        print(f"Min entropy: {min_entropy:.4f}")
        
        # Look for high entropy chunks (possible encryption)
        high_entropy_chunks = [e for e in entropies if e > 7.0]
        if high_entropy_chunks:
            print(f"WARNING: Found {len(high_entropy_chunks)} high-entropy chunks (>7.0)")
            print("This may indicate encrypted or compressed content")
        
        # Look for suspicious patterns
        if max_entropy - min_entropy > 3.0:
            print("WARNING: Large entropy variation detected - possible hidden content")
    
    return entropies

def calculate_chunk_entropy(chunk):
    """Calculate entropy of a byte chunk"""
    if not chunk:
        return 0
    
    import math
    counts = Counter(chunk)
    total = len(chunk)
    entropy = 0
    
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy

def scan_for_polynomial_patterns(content):
    """Scan for polynomial-based encoding (NSA technique)"""
    print("\n=== POLYNOMIAL ENCODING SCAN ===")
    
    # Look for patterns that could be polynomial coefficients
    numbers = re.findall(r'\d+\.?\d*', content)
    numbers = [float(n) for n in numbers if float(n) < 1000]  # Filter reasonable numbers
    
    if len(numbers) > 20:
        # Check for mathematical patterns
        # Look for sequences that could be polynomial evaluations
        for degree in [2, 3, 4, 5]:  # Check polynomial degrees
            if len(numbers) >= degree + 3:
                # Try to fit polynomial to first degree+3 points
                try:
                    coeffs = fit_polynomial(numbers[:degree+3], degree)
                    if coeffs:
                        # Test if polynomial fits other points
                        matches = 0
                        for i in range(degree+3, min(len(numbers), degree+10)):
                            predicted = evaluate_polynomial(coeffs, i)
                            if abs(predicted - numbers[i]) < 0.001:
                                matches += 1
                        
                        if matches > degree//2:
                            print(f"Possible degree-{degree} polynomial pattern detected")
                            print(f"Coefficients: {coeffs}")
                            return True
                except:
                    pass
    
    print("No polynomial encoding patterns detected")
    return False

def fit_polynomial(points, degree):
    """Simple polynomial fitting (simplified for detection)"""
    if len(points) < degree + 1:
        return None
    
    # Use finite differences for simple cases
    diffs = points[:]
    for _ in range(degree):
        diffs = [diffs[i+1] - diffs[i] for i in range(len(diffs)-1)]
    
    # If differences become constant, we have a polynomial
    if len(set(round(d, 6) for d in diffs[-5:])) == 1:
        return diffs[:degree+1]  # Return coefficients
    
    return None

def evaluate_polynomial(coeffs, x):
    """Evaluate polynomial at point x"""
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result

def scan_for_timing_channels(content):
    """Scan for timing-based channels (advanced technique)"""
    print("\n=== TIMING CHANNEL ANALYSIS ===")
    
    # Look for patterns in comment timing
    comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)
    
    # Analyze comment lengths for timing patterns
    comment_lengths = [len(comment) for comment in comments]
    
    if len(comment_lengths) > 10:
        # Look for binary patterns in length differences
        binary_pattern = ''.join(['1' if i > 0 and comment_lengths[i] > comment_lengths[i-1] else '0' 
                                  for i in range(1, len(comment_lengths))])
        
        # Try to decode as ASCII
        try:
            if len(binary_pattern) >= 8:
                padded = binary_pattern.ljust((len(binary_pattern) + 7) // 8 * 8, '0')
                bytes_data = int(padded, 2).to_bytes(len(padded) // 8, 'big')
                decoded = bytes_data.decode('ascii', errors='ignore')
                if any(c.isalnum() for c in decoded):
                    print(f"Timing channel may encode: '{decoded[:50]}...'")
                    return True
        except:
            pass
    
    print("No timing channels detected")
    return False

def main():
    with open('normalize.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("NSA-GRADE CRYPTOGRAPHIC ANALYSIS OF NORMALIZE.CSS")
    print("=" * 60)
    
    # Run comprehensive crypto analysis
    scan_for_crypto_signatures(content)
    analyze_byte_patterns(content)
    scan_for_steganographic_watermarks(content)
    analyze_entropy_distribution(content)
    scan_for_polynomial_patterns(content)
    scan_for_timing_channels(content)
    
    print("\n=== CRYPTOGRAPHIC ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    main()
