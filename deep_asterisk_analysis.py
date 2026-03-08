#!/usr/bin/env python3
"""
Deep Asterisk Position Analysis - All File Variants
Finds equivalent relative positions across all normalize.css variants
"""

import os
import re
import math
from collections import defaultdict

def analyze_all_asterisk_positions():
    """Deep analysis of asterisk positions across all file variants"""
    print("=== DEEP ASTERISK POSITION ANALYSIS - ALL VARIANTS ===")
    print("Finding equivalent relative positions across file variants")
    
    # Find all normalize.css variants
    variants = find_all_variants()
    
    print(f"\nFound {len(variants)} file variants:")
    for variant in variants:
        print(f"  {variant['name']}: {variant['size']} bytes")
    
    # Extract asterisk positions from all variants
    all_positions = {}
    for variant in variants:
        positions = extract_asterisk_positions(variant['path'])
        all_positions[variant['name']] = {
            'positions': positions,
            'count': len(positions),
            'variant': variant
        }
        print(f"  {variant['name']}: {len(positions)} asterisks")
    
    # Find equivalent relative positions
    print(f"\n=== EQUIVALENT RELATIVE POSITION ANALYSIS ===")
    equivalent_positions = find_equivalent_positions(all_positions)
    
    # Analyze patterns in equivalent positions
    print(f"\n=== PATTERN ANALYSIS ===")
    analyze_equivalent_patterns(equivalent_positions, all_positions)
    
    # Cross-variant mathematical analysis
    print(f"\n=== CROSS-VARIANT MATHEMATICAL ANALYSIS ===")
    cross_variant_analysis(all_positions)
    
    return all_positions, equivalent_positions

def find_all_variants():
    """Find all normalize.css variants"""
    variants = []
    
    # Base file
    if os.path.exists('normalize.css'):
        variants.append({
            'name': 'normalize.css',
            'path': 'normalize.css',
            'size': os.path.getsize('normalize.css'),
            'type': 'base'
        })
    
    # RESEARCH-CYBERWEAPON folder variants
    research_dir = 'RESEARCH-CYBERWEAPON'
    if os.path.exists(research_dir):
        for file in os.listdir(research_dir):
            if file.startswith('normalize_') and file.endswith('.css'):
                file_path = os.path.join(research_dir, file)
                if os.path.isfile(file_path):
                    # Extract encoding info from filename
                    encoding = extract_encoding_from_filename(file)
                    variants.append({
                        'name': file,
                        'path': file_path,
                        'size': os.path.getsize(file_path),
                        'type': 'encoded',
                        'encoding': encoding
                    })
    
    # Test file
    if os.path.exists('test.html'):
        variants.append({
            'name': 'test.html',
            'path': 'test.html',
            'size': os.path.getsize('test.html'),
            'type': 'test'
        })
    
    return sorted(variants, key=lambda x: x['name'])

def extract_encoding_from_filename(filename):
    """Extract encoding information from filename"""
    encodings = {
        'utf7': 'UTF-7',
        'utf16be': 'UTF-16BE',
        'utf16le': 'UTF-16LE',
        'utf32be': 'UTF-32BE',
        'utf32le': 'UTF-32LE'
    }
    
    for key, value in encodings.items():
        if key in filename.lower():
            return value
    
    return 'Unknown'

def extract_asterisk_positions(file_path):
    """Extract asterisk positions with full context"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        # Try different encodings
        for encoding in ['latin-1', 'cp1252', 'utf-16']:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                break
            except:
                continue
        else:
            return []
    
    lines = content.split('\n')
    total_lines = len(lines)
    total_chars = len(content)
    
    positions = []
    for line_num, line in enumerate(lines):
        line_len = len(line)
        for char_pos, char in enumerate(line):
            if char == '*':
                # Calculate multiple position metrics
                abs_pos = len(''.join(lines[:line_num])) + char_pos
                
                position_data = {
                    'line': line_num,
                    'char': char_pos,
                    'abs_pos': abs_pos,
                    'rel_line': line_num / total_lines,
                    'rel_char': char_pos / max(line_len, 1),
                    'rel_abs': abs_pos / total_chars,
                    'line_boundary_dist': min(line_num, total_lines - line_num - 1),
                    'char_boundary_dist': min(char_pos, line_len - char_pos - 1) if line_len > 0 else 0,
                    'line_len': line_len,
                    'context': line[max(0, char_pos-10):char_pos+11]
                }
                
                # Calculate boundary factors
                position_data['line_boundary_factor'] = position_data['line_boundary_dist'] / (total_lines / 2)
                position_data['char_boundary_factor'] = position_data['char_boundary_dist'] / (max(line_len, 1) / 2) if line_len > 0 else 0
                position_data['combined_boundary'] = (position_data['line_boundary_factor'] + position_data['char_boundary_factor']) / 2
                
                positions.append(position_data)
    
    return positions

def find_equivalent_positions(all_positions):
    """Find equivalent relative positions across variants"""
    equivalent_positions = defaultdict(list)
    
    variant_names = list(all_positions.keys())
    
    # Compare each pair of variants
    for i, variant1 in enumerate(variant_names):
        for j, variant2 in enumerate(variant_names[i+1:], i+1):
            pos1 = all_positions[variant1]['positions']
            pos2 = all_positions[variant2]['positions']
            
            print(f"\nComparing {variant1} vs {variant2}:")
            
            # Find positions with similar relative coordinates
            matches = find_position_matches(pos1, pos2, variant1, variant2)
            
            if matches:
                print(f"  Found {len(matches)} equivalent positions")
                for match in matches[:5]:  # Show first 5
                    equivalent_positions[f"{variant1}_{variant2}"].append(match)
                    print(f"    {match}")
            else:
                print(f"  No equivalent positions found")
    
    return equivalent_positions

def find_position_matches(pos1, pos2, name1, name2):
    """Find matching positions between two variant position sets"""
    matches = []
    tolerance = 0.01  # 1% tolerance for relative positions
    
    for p1 in pos1[:50]:  # Check first 50 asterisks
        for p2 in pos2[:50]:
            # Check relative line position
            if abs(p1['rel_line'] - p2['rel_line']) < tolerance:
                # Check relative character position
                if abs(p1['rel_char'] - p2['rel_char']) < tolerance:
                    # Check combined boundary factor
                    if abs(p1['combined_boundary'] - p2['combined_boundary']) < tolerance:
                        matches.append({
                            'variant1': name1,
                            'variant2': name2,
                            'pos1': {'line': p1['line'], 'char': p1['char'], 'rel_line': p1['rel_line'], 'rel_char': p1['rel_char']},
                            'pos2': {'line': p2['line'], 'char': p2['char'], 'rel_line': p2['rel_line'], 'rel_char': p2['rel_char']},
                            'similarity': calculate_similarity(p1, p2)
                        })
                        break
    
    return matches

def calculate_similarity(p1, p2):
    """Calculate similarity score between two positions"""
    line_diff = abs(p1['rel_line'] - p2['rel_line'])
    char_diff = abs(p1['rel_char'] - p2['rel_char'])
    boundary_diff = abs(p1['combined_boundary'] - p2['combined_boundary'])
    
    # Lower differences = higher similarity
    similarity = 1 - (line_diff + char_diff + boundary_diff) / 3
    return similarity

def analyze_equivalent_patterns(equivalent_positions, all_positions):
    """Analyze patterns in equivalent positions"""
    if not equivalent_positions:
        print("No equivalent positions found")
        return
    
    # Group by similarity
    high_similarity = []
    medium_similarity = []
    
    for pair_key, matches in equivalent_positions.items():
        for match in matches:
            if match['similarity'] > 0.95:
                high_similarity.append(match)
            elif match['similarity'] > 0.8:
                medium_similarity.append(match)
    
    print(f"High similarity matches (>95%): {len(high_similarity)}")
    print(f"Medium similarity matches (>80%): {len(medium_similarity)}")
    
    # Look for mathematical patterns
    if high_similarity:
        print(f"\nHigh similarity patterns:")
        analyze_position_patterns(high_similarity)
    
    if medium_similarity:
        print(f"\nMedium similarity patterns:")
        analyze_position_patterns(medium_similarity)

def analyze_position_patterns(matches):
    """Analyze mathematical patterns in position matches"""
    # Extract line and character positions
    lines1 = [m['pos1']['line'] for m in matches]
    lines2 = [m['pos2']['line'] for m in matches]
    chars1 = [m['pos1']['char'] for m in matches]
    chars2 = [m['pos2']['char'] for m in matches]
    
    # Check for prime number patterns
    prime_lines1 = [x for x in lines1 if is_prime(x)]
    prime_lines2 = [x for x in lines2 if is_prime(x)]
    
    if prime_lines1 or prime_lines2:
        print(f"  Prime line positions: {len(prime_lines1)} in variant1, {len(prime_lines2)} in variant2")
    
    # Check for Fibonacci patterns
    fib_lines1 = [x for x in lines1 if is_fibonacci(x)]
    fib_lines2 = [x for x in lines2 if is_fibonacci(x)]
    
    if fib_lines1 or fib_lines2:
        print(f"  Fibonacci line positions: {len(fib_lines1)} in variant1, {len(fib_lines2)} in variant2")
    
    # Check for mathematical relationships
    if len(lines1) > 1:
        line_ratios = []
        for i in range(1, min(len(lines1), 10)):
            if lines1[i-1] > 0:
                ratio = lines1[i] / lines1[i-1]
                line_ratios.append(ratio)
        
        # Check for golden ratio
        golden_ratios = [r for r in line_ratios if 0.5 < r < 2.5 and abs(r - 1.618) < 0.1]
        if golden_ratios:
            print(f"  Golden ratio patterns detected: {len(golden_ratios)} occurrences")

def cross_variant_analysis(all_positions):
    """Perform cross-variant mathematical analysis"""
    variant_names = list(all_positions.keys())
    
    # Create position matrix
    position_matrix = {}
    
    for variant_name in variant_names:
        positions = all_positions[variant_name]['positions']
        if positions:
            # Create normalized position vectors
            vectors = []
            for pos in positions[:32]:  # First 32 asterisks
                vector = [
                    pos['rel_line'],
                    pos['rel_char'],
                    pos['combined_boundary']
                ]
                vectors.append(vector)
            
            position_matrix[variant_name] = vectors
    
    # Compare vectors across variants
    print("Vector similarity analysis:")
    for i, variant1 in enumerate(variant_names):
        for j, variant2 in enumerate(variant_names[i+1:], i+1):
            if variant1 in position_matrix and variant2 in position_matrix:
                vectors1 = position_matrix[variant1]
                vectors2 = position_matrix[variant2]
                
                # Calculate vector similarity
                similarity = calculate_vector_similarity(vectors1, vectors2)
                print(f"  {variant1} vs {variant2}: {similarity:.3f}")

def calculate_vector_similarity(vectors1, vectors2):
    """Calculate similarity between two sets of position vectors"""
    if not vectors1 or not vectors2:
        return 0.0
    
    min_len = min(len(vectors1), len(vectors2))
    total_similarity = 0.0
    
    for i in range(min_len):
        v1 = vectors1[i]
        v2 = vectors2[i]
        
        # Calculate Euclidean distance
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
        # Convert to similarity (lower distance = higher similarity)
        similarity = 1 / (1 + distance)
        total_similarity += similarity
    
    return total_similarity / min_len

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    """Check if number is in Fibonacci sequence"""
    if n < 0:
        return False
    
    # Check if 5*n^2 + 4 or 5*n^2 - 4 is a perfect square
    def is_perfect_square(x):
        s = int(math.sqrt(x))
        return s * s == x
    
    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

def main():
    print("DEEP ASTERISK POSITION ANALYSIS - ALL VARIANTS")
    print("=" * 60)
    
    all_positions, equivalent_positions = analyze_all_asterisk_positions()
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Total variants analyzed: {len(all_positions)}")
    print(f"Equivalent position pairs: {len(equivalent_positions)}")
    
    # Summary
    total_asterisks = sum(data['count'] for data in all_positions.values())
    print(f"Total asterisks across all variants: {total_asterisks}")
    
    if equivalent_positions:
        total_matches = sum(len(matches) for matches in equivalent_positions.values())
        print(f"Total equivalent position matches: {total_matches}")
    else:
        print("No equivalent positions found across variants")

if __name__ == "__main__":
    main()
