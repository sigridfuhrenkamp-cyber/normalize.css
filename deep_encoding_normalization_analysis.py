#!/usr/bin/env python3
"""
Deep Encoding and Normalization Path Analysis
Comprehensive analysis of all encoding/normalization paths for anomalies
"""

import os
import re
import unicodedata
import base64
import binascii
from collections import defaultdict, Counter

def analyze_all_encoding_normalization_paths():
    """Deep analysis of all encoding and normalization paths"""
    print("=== DEEP ENCODING & NORMALIZATION PATH ANALYSIS ===")
    print("Analyzing all variants for encoding/normalization anomalies")
    
    # Get all file variants
    variants = get_all_file_variants()
    
    print(f"\nFound {len(variants)} file variants:")
    for variant in variants:
        print(f"  {variant['name']}: {variant['size']} bytes")
    
    # Analyze each variant
    all_anomalies = {}
    
    for variant in variants:
        print(f"\n=== ANALYZING {variant['name'].upper()} ===")
        anomalies = analyze_variant_encoding_normalization(variant)
        all_anomalies[variant['name']] = anomalies
    
    # Cross-variant anomaly analysis
    print(f"\n=== CROSS-VARIANT ANOMALY ANALYSIS ===")
    cross_variant_anomalies = analyze_cross_variant_anomalies(all_anomalies)
    
    # Normalization path analysis
    print(f"\n=== NORMALIZATION PATH ANALYSIS ===")
    normalization_paths = analyze_normalization_paths(variants)
    
    # Suspicious behavior detection
    print(f"\n=== SUSPICIOUS BEHAVIOR DETECTION ===")
    suspicious_behaviors = detect_suspicious_behaviors(all_anomalies)
    
    return {
        'variant_anomalies': all_anomalies,
        'cross_variant': cross_variant_anomalies,
        'normalization_paths': normalization_paths,
        'suspicious_behaviors': suspicious_behaviors
    }

def get_all_file_variants():
    """Get all file variants including encoded versions"""
    variants = []
    
    # Base file
    if os.path.exists('normalize.css'):
        variants.append({
            'name': 'normalize.css',
            'path': 'normalize.css',
            'size': os.path.getsize('normalize.css'),
            'type': 'base'
        })
    
    # Test file
    if os.path.exists('test.html'):
        variants.append({
            'name': 'test.html',
            'path': 'test.html',
            'size': os.path.getsize('test.html'),
            'type': 'test'
        })
    
    # RESEARCH-CYBERWEAPON folder variants
    research_dir = 'RESEARCH-CYBERWEAPON'
    if os.path.exists(research_dir):
        for file in os.listdir(research_dir):
            if file.endswith('.css'):
                file_path = os.path.join(research_dir, file)
                if os.path.isfile(file_path):
                    encoding = extract_encoding_from_filename(file)
                    variants.append({
                        'name': file,
                        'path': file_path,
                        'size': os.path.getsize(file_path),
                        'type': 'encoded',
                        'encoding': encoding
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

def analyze_variant_encoding_normalization(variant):
    """Analyze encoding and normalization for a single variant"""
    print(f"Analyzing {variant['name']}...")
    
    anomalies = {
        'encoding_anomalies': [],
        'normalization_anomalies': [],
        'suspicious_sequences': [],
        'unicode_anomalies': [],
        'byte_pattern_anomalies': [],
        'linter_parser_anomalies': []
    }
    
    # Read file content with multiple encoding attempts
    content = read_file_with_encoding_fallback(variant['path'])
    if not content:
        anomalies['encoding_anomalies'].append("Failed to read file with any encoding")
        return anomalies
    
    # 1. Encoding analysis
    encoding_anomalies = analyze_encoding_patterns(content, variant)
    anomalies['encoding_anomalies'] = encoding_anomalies
    
    # 2. Unicode analysis
    unicode_anomalies = analyze_unicode_patterns(content, variant)
    anomalies['unicode_anomalies'] = unicode_anomalies
    
    # 3. Normalization analysis
    normalization_anomalies = analyze_unicode_normalization(content, variant)
    anomalies['normalization_anomalies'] = normalization_anomalies
    
    # 4. Suspicious sequence detection
    suspicious_sequences = detect_suspicious_sequences(content, variant)
    anomalies['suspicious_sequences'] = suspicious_sequences
    
    # 5. Byte pattern analysis
    byte_anomalies = analyze_byte_patterns(content, variant)
    anomalies['byte_pattern_anomalies'] = byte_anomalies
    
    # 6. Linter/parser behavior simulation
    linter_anomalies = simulate_linter_parser_behavior(content, variant)
    anomalies['linter_parser_anomalies'] = linter_anomalies
    
    # Print summary
    total_anomalies = sum(len(anomalies[key]) for key in anomalies)
    print(f"  Total anomalies found: {total_anomalies}")
    for anomaly_type, anomaly_list in anomalies.items():
        if anomaly_list:
            print(f"    {anomaly_type}: {len(anomaly_list)}")
    
    return anomalies

def read_file_with_encoding_fallback(file_path):
    """Read file with multiple encoding attempts"""
    encodings = ['utf-8', 'utf-16', 'utf-32', 'latin-1', 'cp1252', 'utf-7']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                return f.read()
        except:
            continue
    
    return None

def analyze_encoding_patterns(content, variant):
    """Analyze encoding patterns for anomalies"""
    anomalies = []
    
    # Check for BOM (Byte Order Mark)
    if content.startswith('\ufeff'):
        anomalies.append("UTF-8 BOM detected")
    elif content.startswith('\ufeff'):
        anomalies.append("BOM detected")
    
    # Check for null bytes (common in UTF-16/32)
    null_count = content.count('\x00')
    if null_count > len(content) * 0.1:  # More than 10% null bytes
        anomalies.append(f"High null byte count: {null_count} ({null_count/len(content)*100:.1f}%)")
    
    # Check for unusual byte sequences
    try:
        content_bytes = content.encode('utf-8', errors='ignore')
        
        # Look for suspicious byte patterns
        suspicious_patterns = [
            b'\x00\x00\x00',  # Null null null (UTF-32)
            b'\x00\x00',       # Null null (UTF-16)
            b'\xef\xbb\xbf',   # UTF-8 BOM
            b'\xff\xfe',       # UTF-16 LE BOM
            b'\xfe\xff',       # UTF-16 BE BOM
        ]
        
        for pattern in suspicious_patterns:
            if pattern in content_bytes:
                anomalies.append(f"Suspicious byte pattern: {pattern}")
    
    except:
        anomalies.append("Failed to analyze byte patterns")
    
    return anomalies

def analyze_unicode_patterns(content, variant):
    """Analyze Unicode patterns for anomalies"""
    anomalies = []
    
    # Check for invisible Unicode characters
    invisible_chars = []
    for i, char in enumerate(content):
        if unicodedata.category(char) in ['Cc', 'Cf', 'Cs', 'Co', 'Cn']:
            # Control, Format, Surrogate, Private Use, Unassigned
            invisible_chars.append((i, char, ord(char)))
    
    if invisible_chars:
        anomalies.append(f"Found {len(invisible_chars)} invisible/special Unicode characters")
        
        # Check for specific suspicious characters
        suspicious_unicode = {
            0x2029: 'Paragraph Separator',
            0x2060: 'Word Joiner',
            0x200B: 'Zero Width Space',
            0x200C: 'Zero Width Non-Joiner',
            0x200D: 'Zero Width Joiner',
            0x202E: 'RTL Override',
            0x202A: 'LRE',
            0x202B: 'RLE',
            0x202C: 'PDF',
            0x202D: 'LRO',
            0x202F: 'LRI',
            0x2066: 'RLI',
            0x2067: 'FSI',
            0x2069: 'PDI'
        }
        
        for pos, char, codepoint in invisible_chars:
            if codepoint in suspicious_unicode:
                anomalies.append(f"Suspicious Unicode at pos {pos}: U+{codepoint:04X} ({suspicious_unicode[codepoint]})")
    
    # Check for high Unicode code points
    high_unicode = [(i, char, ord(char)) for i, char in enumerate(content) if ord(char) > 0x1000]
    if len(high_unicode) > len(content) * 0.05:  # More than 5% high Unicode
        anomalies.append(f"High Unicode usage: {len(high_unicode)} characters")
    
    return anomalies

def analyze_unicode_normalization(content, variant):
    """Analyze Unicode normalization for anomalies"""
    anomalies = []
    
    # Test different normalization forms
    normalization_forms = ['NFC', 'NFD', 'NFKC', 'NFKD']
    
    for form in normalization_forms:
        try:
            normalized = unicodedata.normalize(form, content)
            
            if normalized != content:
                # Check for asterisk position changes
                orig_asterisks = [i for i, c in enumerate(content) if c == '*']
                norm_asterisks = [i for i, c in enumerate(normalized) if c == '*']
                
                if orig_asterisks != norm_asterisks:
                    anomalies.append(f"{form} normalization changes asterisk positions: {len(orig_asterisks)} -> {len(norm_asterisks)}")
                    
                    # Check for mathematical patterns in position changes
                    if len(orig_asterisks) == len(norm_asterisks):
                        position_shifts = [norm_asterisks[i] - orig_asterisks[i] for i in range(min(len(orig_asterisks), len(norm_asterisks)))]
                        
                        # Check for prime patterns
                        prime_shifts = [shift for shift in position_shifts if is_prime(abs(shift))]
                        if prime_shifts:
                            anomalies.append(f"{form} normalization shows prime position shifts: {prime_shifts[:5]}")
                        
                        # Check for Fibonacci patterns
                        fib_shifts = [shift for shift in position_shifts if is_fibonacci(abs(shift))]
                        if fib_shifts:
                            anomalies.append(f"{form} normalization shows Fibonacci position shifts: {fib_shifts[:5]}")
                
                # Check for content length changes
                if len(normalized) != len(content):
                    anomalies.append(f"{form} normalization changes content length: {len(content)} -> {len(normalized)}")
        
        except Exception as e:
            anomalies.append(f"Failed {form} normalization: {e}")
    
    return anomalies

def detect_suspicious_sequences(content, variant):
    """Detect suspicious sequences in content"""
    anomalies = []
    
    # Look for suspicious patterns
    suspicious_patterns = [
        (r'\\[uU][0-9a-fA-F]{4}', 'Unicode escape sequences'),
        (r'\\[xX][0-9a-fA-F]{2}', 'Hex escape sequences'),
        (r'\\[0-7]{1,3}', 'Octal escape sequences'),
        (r'%[0-9A-Fa-f]{2}', 'URL encoding'),
        (r'&#\d+;', 'HTML entity decimal'),
        (r'&#x[0-9A-Fa-f]+;', 'HTML entity hex'),
        (r'/\*.*?\*/', 'CSS comments'),
        (r'<!--.*?-->', 'HTML comments'),
    ]
    
    for pattern, description in suspicious_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            anomalies.append(f"Found {len(matches)} {description}")
    
    # Look for mathematical patterns
    math_patterns = [
        (r'1\.618', 'Golden ratio'),
        (r'3\.14159', 'Pi'),
        (r'2\.71828', 'Euler\'s number'),
        (r'0\.618', 'Golden ratio conjugate'),
    ]
    
    for pattern, description in math_patterns:
        if re.search(pattern, content):
            anomalies.append(f"Mathematical constant found: {description}")
    
    # Look for repeated patterns
    lines = content.split('\n')
    line_patterns = Counter(lines)
    
    for line, count in line_patterns.items():
        if count > 5 and len(line.strip()) > 10:  # Repeated non-trivial lines
            anomalies.append(f"Repeated line pattern: '{line[:30]}...' ({count} times)")
    
    return anomalies

def analyze_byte_patterns(content, variant):
    """Analyze byte patterns for anomalies"""
    anomalies = []
    
    try:
        content_bytes = content.encode('utf-8', errors='ignore')
        
        # Look for suspicious byte sequences
        if len(content_bytes) > 0:
            # Check for repeating byte patterns
            for length in [2, 4, 8, 16]:
                patterns = {}
                for i in range(len(content_bytes) - length + 1):
                    pattern = content_bytes[i:i+length]
                    patterns[pattern] = patterns.get(pattern, 0) + 1
                
                # Find highly repeated patterns
                repeated_patterns = [(p, c) for p, c in patterns.items() if c > 10]
                if repeated_patterns:
                    anomalies.append(f"Repeated {length}-byte patterns: {len(repeated_patterns)}")
        
        # Check for entropy anomalies
        byte_counts = Counter(content_bytes)
        total_bytes = len(content_bytes)
        
        if total_bytes > 0:
            # Calculate entropy
            entropy = 0
            for count in byte_counts.values():
                p = count / total_bytes
                if p > 0:
                    entropy -= p * (p.bit_length() - 1)  # Using bit_length for log2
            
            # Check for unusual entropy
            if entropy < 3.0:
                anomalies.append(f"Low entropy: {entropy:.2f}")
            elif entropy > 7.0:
                anomalies.append(f"High entropy: {entropy:.2f}")
    
    except Exception as e:
        anomalies.append(f"Byte pattern analysis failed: {e}")
    
    return anomalies

def simulate_linter_parser_behavior(content, variant):
    """Simulate linter/parser behavior to find anomalies"""
    anomalies = []
    
    # Simulate CSS parser behavior
    css_anomalies = simulate_css_parser(content)
    anomalies.extend(css_anomalies)
    
    # Simulate HTML parser behavior (if applicable)
    if variant['name'].endswith('.html') or '<' in content:
        html_anomalies = simulate_html_parser(content)
        anomalies.extend(html_anomalies)
    
    # Simulate JavaScript parser behavior (if applicable)
    if 'function' in content or 'var ' in content or 'let ' in content or 'const ' in content:
        js_anomalies = simulate_js_parser(content)
        anomalies.extend(js_anomalies)
    
    return anomalies

def simulate_css_parser(content):
    """Simulate CSS parser behavior"""
    anomalies = []
    
    # Look for CSS parsing anomalies
    css_rules = re.findall(r'[^{}]+\{[^{}]*\}', content, re.DOTALL)
    
    for rule in css_rules:
        # Check for unusual selectors
        selector_part = rule.split('{')[0].strip()
        
        # Check for suspicious characters in selectors
        if re.search(r'[^\w\s\-\.#:\[\]()>,+*~|]', selector_part):
            anomalies.append(f"Suspicious CSS selector: {selector_part}")
        
        # Check for asterisk abuse
        asterisk_count = selector_part.count('*')
        if asterisk_count > 5:
            anomalies.append(f"High asterisk count in selector: {asterisk_count}")
    
    # Check for CSS comment anomalies
    comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)
    
    for comment in comments:
        # Check for suspicious content in comments
        if len(comment) > 100:
            anomalies.append(f"Long CSS comment: {len(comment)} characters")
        
        # Check for invisible characters in comments
        invisible_in_comment = sum(1 for c in comment if unicodedata.category(c) in ['Cc', 'Cf'])
        if invisible_in_comment > 0:
            anomalies.append(f"Invisible characters in CSS comment: {invisible_in_comment}")
    
    return anomalies

def simulate_html_parser(content):
    """Simulate HTML parser behavior"""
    anomalies = []
    
    # Look for HTML parsing anomalies
    html_tags = re.findall(r'<[^>]+>', content)
    
    for tag in html_tags:
        # Check for suspicious attributes
        if re.search(r'on\w+\s*=', tag, re.IGNORECASE):
            anomalies.append(f"Suspicious event handler in HTML: {tag}")
        
        # Check for suspicious protocols
        if re.search(r'href\s*=\s*["\']?(javascript|data):', tag, re.IGNORECASE):
            anomalies.append(f"Suspicious protocol in HTML: {tag}")
    
    return anomalies

def simulate_js_parser(content):
    """Simulate JavaScript parser behavior"""
    anomalies = []
    
    # Look for JavaScript parsing anomalies
    js_strings = re.findall(r'(["\'])(?:\\.|(?!\1)[^\\\r\n])*\1', content)
    
    for string in js_strings:
        # Check for suspicious escape sequences
        if re.search(r'\\[uU][0-9a-fA-F]{4}', string):
            anomalies.append(f"Unicode escape in JS string: {string}")
        
        # Check for suspicious content
        if len(string) > 100:
            anomalies.append(f"Long JS string: {len(string)} characters")
    
    return anomalies

def analyze_cross_variant_anomalies(all_anomalies):
    """Analyze anomalies across all variants"""
    print("Analyzing cross-variant anomalies...")
    
    cross_variant = {
        'common_anomalies': defaultdict(list),
        'unique_anomalies': defaultdict(list),
        'severity_analysis': {}
    }
    
    # Collect all anomaly types
    all_anomaly_types = set()
    for variant_anomalies in all_anomalies.values():
        for anomaly_type in variant_anomalies.keys():
            all_anomaly_types.add(anomaly_type)
    
    # Analyze each anomaly type across variants
    for anomaly_type in all_anomaly_types:
        variant_anomalies = {}
        
        for variant_name, anomalies in all_anomalies.items():
            if anomaly_type in anomalies:
                variant_anomalies[variant_name] = anomalies[anomaly_type]
        
        # Find common anomalies
        if variant_anomalies:
            common_anomalies = set()
            
            # Find intersection of anomalies across variants
            first_variant = list(variant_anomalies.keys())[0]
            common_anomalies = set(variant_anomalies[first_variant])
            
            for other_variant in list(variant_anomalies.keys())[1:]:
                common_anomalies &= set(variant_anomalies[other_variant])
            
            if common_anomalies:
                cross_variant['common_anomalies'][anomaly_type] = list(common_anomalies)
                print(f"  Common {anomaly_type}: {len(common_anomalies)}")
    
    return cross_variant

def analyze_normalization_paths(variants):
    """Analyze normalization paths across variants"""
    print("Analyzing normalization paths...")
    
    paths = {
        'normalization_chains': [],
        'encoding_transformations': [],
        'anomaly_correlations': []
    }
    
    # Test normalization chains
    for variant in variants:
        try:
            content = read_file_with_encoding_fallback(variant['path'])
            if not content:
                continue
            
            # Test normalization chain: NFC -> NFD -> NFKD -> NFKC
            chain_results = []
            current = content
            
            for form in ['NFC', 'NFD', 'NFKD', 'NFKC']:
                normalized = unicodedata.normalize(form, current)
                
                if normalized != current:
                    chain_results.append({
                        'from': current[:50] + '...',
                        'to': normalized[:50] + '...',
                        'form': form,
                        'variant': variant['name']
                    })
                
                current = normalized
            
            if chain_results:
                paths['normalization_chains'].extend(chain_results)
        
        except Exception as e:
            print(f"  Error analyzing {variant['name']}: {e}")
    
    return paths

def detect_suspicious_behaviors(all_anomalies):
    """Detect suspicious behaviors from anomalies"""
    print("Detecting suspicious behaviors...")
    
    behaviors = {
        'mathematical_encoding': False,
        'steganographic_patterns': False,
        'parser_exploitation': False,
        'encoding_manipulation': False,
        'normalization_abuse': False
    }
    
    # Check for mathematical encoding
    for variant_name, anomalies in all_anomalies.items():
        for anomaly_list in anomalies.values():
            for anomaly in anomaly_list:
                if 'golden ratio' in anomaly.lower() or 'pi' in anomaly.lower() or 'prime' in anomaly.lower():
                    behaviors['mathematical_encoding'] = True
                if 'asterisk' in anomaly.lower():
                    behaviors['steganographic_patterns'] = True
                if 'parser' in anomaly.lower() or 'linter' in anomaly.lower():
                    behaviors['parser_exploitation'] = True
                if 'encoding' in anomaly.lower() or 'byte' in anomaly.lower():
                    behaviors['encoding_manipulation'] = True
                if 'normalization' in anomaly.lower():
                    behaviors['normalization_abuse'] = True
    
    # Print detected behaviors
    for behavior, detected in behaviors.items():
        if detected:
            print(f"  ⚠️  {behavior.replace('_', ' ').title()}: DETECTED")
    
    return behaviors

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    """Check if number is in Fibonacci sequence"""
    if n < 0:
        return False
    
    def is_perfect_square(x):
        s = int(x**0.5)
        return s * s == x
    
    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

def main():
    print("DEEP ENCODING & NORMALIZATION PATH ANALYSIS")
    print("=" * 60)
    
    results = analyze_all_encoding_normalization_paths()
    
    print(f"\n=== COMPREHENSIVE ANALYSIS SUMMARY ===")
    
    # Count total anomalies
    total_anomalies = 0
    for variant_anomalies in results['variant_anomalies'].values():
        total_anomalies += sum(len(anomaly_list) for anomaly_list in variant_anomalies.values())
    
    print(f"Total anomalies across all variants: {total_anomalies}")
    
    # Suspicious behaviors
    suspicious_behaviors = results['suspicious_behaviors']
    detected_behaviors = [behavior for behavior, detected in suspicious_behaviors.items() if detected]
    
    if detected_behaviors:
        print(f"\n🚨 SUSPICIOUS BEHAVIORS DETECTED:")
        for behavior in detected_behaviors:
            print(f"  ⚠️  {behavior.replace('_', ' ').title()}")
    
    # Cross-variant anomalies
    common_anomalies = results['cross_variant']['common_anomalies']
    if common_anomalies:
        print(f"\n🔗 CROSS-VARIANT ANOMALIES:")
        for anomaly_type, anomalies in common_anomalies.items():
            print(f"  {anomaly_type}: {len(anomalies)} common anomalies")
    
    # Risk assessment
    risk_factors = len(detected_behaviors) + len(common_anomalies)
    
    if risk_factors >= 5:
        print(f"\n🚨 HIGH RISK - Multiple suspicious behaviors detected")
    elif risk_factors >= 3:
        print(f"\n⚠️  MEDIUM RISK - Some suspicious behaviors detected")
    elif risk_factors >= 1:
        print(f"\n🔍 LOW RISK - Few suspicious behaviors detected")
    else:
        print(f"\n✅ LOW RISK - No significant suspicious behaviors detected")

if __name__ == "__main__":
    main()
