#!/usr/bin/env python3
"""
CSS Normalization Cyberweapon Analyzer
Exploits different normalization variants in linters/parsers
"""

import re
import unicodedata
import html

def analyze_normalization_variants():
    """Analyze all CSS normalization variants for cyberweapon exploits"""
    print("=== CSS NORMALIZATION CYBERWEAPON ANALYSIS ===")
    
    with open('normalize.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test different normalization forms
    normalization_forms = ['NFC', 'NFD', 'NFKC', 'NFKD']
    
    print("Testing Unicode Normalization Forms:")
    for form in normalization_forms:
        normalized = unicodedata.normalize(form, content)
        print(f"\n{form}:")
        print(f"  Original length: {len(content)}")
        print(f"  Normalized length: {len(normalized)}")
        print(f"  Difference: {len(normalized) - len(content)}")
        
        # Check for hidden content revealed by normalization
        if normalized != content:
            print(f"  *** NORMALIZATION REVEALS HIDDEN CONTENT ***")
            analyze_normalization_differences(content, normalized, form)
    
    # Test HTML entity decoding
    print("\n=== HTML ENTITY DECODING ===")
    html_decoded = html.unescape(content)
    if html_decoded != content:
        print("*** HTML ENTITY DECODING REVEALS HIDDEN CONTENT ***")
        analyze_html_differences(content, html_decoded)
    
    # Test URL encoding
    print("\n=== URL ENCODING ANALYSIS ===")
    try:
        import urllib.parse
        url_decoded = urllib.parse.unquote(content)
        if url_decoded != content:
            print("*** URL DECODING REVEALS HIDDEN CONTENT ***")
            analyze_url_differences(content, url_decoded)
    except:
        pass
    
    # Test CSS-specific normalization
    print("\n=== CSS NORMALIZATION ANALYSIS ===")
    analyze_css_normalization(content)
    
    # Test parser-specific behaviors
    print("\n=== PARSER BEHAVIOR ANALYSIS ===")
    analyze_parser_behaviors(content)

def analyze_normalization_differences(original, normalized, form):
    """Analyze differences revealed by normalization"""
    print(f"  Analyzing {form} normalization differences:")
    
    # Find character position differences
    differences = []
    min_len = min(len(original), len(normalized))
    
    for i in range(min_len):
        if original[i] != normalized[i]:
            differences.append({
                'position': i,
                'original': original[i],
                'normalized': normalized[i],
                'original_ord': ord(original[i]),
                'normalized_ord': ord(normalized[i])
            })
    
    # Check length differences
    if len(normalized) > len(original):
        for i in range(len(original), len(normalized)):
            differences.append({
                'position': i,
                'original': None,
                'normalized': normalized[i],
                'original_ord': None,
                'normalized_ord': ord(normalized[i])
            })
    elif len(original) > len(normalized):
        for i in range(len(normalized), len(original)):
            differences.append({
                'position': i,
                'original': original[i],
                'normalized': None,
                'original_ord': ord(original[i]),
                'normalized_ord': None
            })
    
    print(f"    Found {len(differences)} differences:")
    
    # Look for suspicious patterns
    suspicious_chars = []
    for diff in differences:
        if diff['normalized_ord'] and diff['normalized_ord'] > 127:
            suspicious_chars.append(diff)
        if diff['original_ord'] and diff['original_ord'] > 127:
            suspicious_chars.append(diff)
    
    if suspicious_chars:
        print(f"    *** {len(suspicious_chars)} SUSPICIOUS UNICODE CHARACTERS ***")
        for char in suspicious_chars[:10]:
            print(f"      Position {char['position']}: U+{char.get('normalized_ord', char.get('original_ord')):04X}")
    
    # Check for asterisk position changes
    asterisk_changes = []
    for diff in differences:
        if diff['original'] == '*' or diff['normalized'] == '*':
            asterisk_changes.append(diff)
    
    if asterisk_changes:
        print(f"    *** {len(asterisk_changes)} ASTERISK POSITION CHANGES ***")
        print("      This could reveal hidden positioning commands!")

def analyze_html_differences(original, decoded):
    """Analyze HTML entity decoding differences"""
    print("  HTML Entity Differences:")
    
    # Look for HTML entities in original
    entities = re.findall(r'&[a-zA-Z0-9#]+;', original)
    if entities:
        print(f"    Found {len(entities)} HTML entities: {entities[:10]}")
    
    # Check for asterisk position changes
    orig_asterisk_positions = [i for i, c in enumerate(original) if c == '*']
    decoded_asterisk_positions = [i for i, c in enumerate(decoded) if c == '*']
    
    if orig_asterisk_positions != decoded_asterisk_positions:
        print("    *** ASTERISK POSITIONS CHANGED AFTER HTML DECODING ***")
        print(f"      Original: {len(orig_asterisk_positions)} asterisks")
        print(f"      Decoded: {len(decoded_asterisk_positions)} asterisks")

def analyze_url_differences(original, decoded):
    """Analyze URL decoding differences"""
    print("  URL Decoding Differences:")
    
    # Look for URL-encoded patterns
    url_patterns = re.findall(r'%[0-9A-Fa-f]{2}', original)
    if url_patterns:
        print(f"    Found {len(url_patterns)} URL-encoded sequences: {url_patterns[:10]}")
    
    # Check asterisk positions
    orig_asterisk_positions = [i for i, c in enumerate(original) if c == '*']
    decoded_asterisk_positions = [i for i, c in enumerate(decoded) if c == '*']
    
    if orig_asterisk_positions != decoded_asterisk_positions:
        print("    *** ASTERISK POSITIONS CHANGED AFTER URL DECODING ***")

def analyze_css_normalization(content):
    """Analyze CSS-specific normalization"""
    print("  CSS Normalization Analysis:")
    
    # Test CSS comment normalization
    comment_normalized = normalize_css_comments(content)
    if comment_normalized != content:
        print("    *** CSS COMMENT NORMALIZATION REVEALS DIFFERENCES ***")
        analyze_asterisk_position_changes(content, comment_normalized, "CSS Comments")
    
    # Test CSS whitespace normalization
    whitespace_normalized = normalize_css_whitespace(content)
    if whitespace_normalized != content:
        print("    *** CSS WHITESPACE NORMALIZATION REVEALS DIFFERENCES ***")
        analyze_asterisk_position_changes(content, whitespace_normalized, "CSS Whitespace")
    
    # Test CSS case normalization
    case_normalized = normalize_css_case(content)
    if case_normalized != content:
        print("    *** CSS CASE NORMALIZATION REVEALS DIFFERENCES ***")
        analyze_asterisk_position_changes(content, case_normalized, "CSS Case")
    
    # Test CSS escape sequence normalization
    escape_normalized = normalize_css_escapes(content)
    if escape_normalized != content:
        print("    *** CSS ESCAPE SEQUENCE NORMALIZATION REVEALS DIFFERENCES ***")
        analyze_asterisk_position_changes(content, escape_normalized, "CSS Escapes")

def normalize_css_comments(css):
    """Normalize CSS comments"""
    # Remove comments
    without_comments = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    return without_comments

def normalize_css_whitespace(css):
    """Normalize CSS whitespace"""
    # Normalize multiple spaces to single space
    normalized = re.sub(r'\s+', ' ', css)
    # Trim whitespace around tokens
    normalized = re.sub(r'\s*([{}:;,])\s*', r'\1', normalized)
    return normalized

def normalize_css_case(css):
    """Normalize CSS case for identifiers"""
    # Convert selectors and property names to lowercase
    lines = css.split('\n')
    normalized_lines = []
    
    for line in lines:
        # Convert property names to lowercase
        line = re.sub(r'([a-zA-Z-]+)(\s*:)', lambda m: m.group(1).lower() + m.group(2), line)
        # Convert selectors to lowercase (except for attribute values)
        line = re.sub(r'^([a-zA-Z-]+)', lambda m: m.group(1).lower(), line)
        normalized_lines.append(line)
    
    return '\n'.join(normalized_lines)

def normalize_css_escapes(css):
    """Normalize CSS escape sequences"""
    # Replace CSS escapes with actual characters
    def replace_escape(match):
        escape_code = match.group(1)
        if escape_code.startswith('\\'):
            try:
                if escape_code.startswith('\\x'):
                    # Hex escape
                    code_point = int(escape_code[2:], 16)
                elif escape_code.startswith('\\u'):
                    # Unicode escape
                    code_point = int(escape_code[2:], 16)
                else:
                    # Decimal escape
                    code_point = int(escape_code[1:])
                return chr(code_point)
            except:
                return match.group(0)
        return match.group(0)
    
    normalized = re.sub(r'(\\[xu]?[0-9A-Fa-f]+)', replace_escape, css)
    return normalized

def analyze_asterisk_position_changes(original, modified, normalization_type):
    """Analyze how asterisk positions change"""
    orig_positions = [i for i, c in enumerate(original) if c == '*']
    mod_positions = [i for i, c in enumerate(modified) if c == '*']
    
    print(f"      {normalization_type} Asterisk Analysis:")
    print(f"        Original asterisks: {len(orig_positions)}")
    print(f"        Modified asterisks: {len(mod_positions)}")
    
    if orig_positions != mod_positions:
        print(f"        *** POSITION CHANGES DETECTED ***")
        
        # Find position differences
        if len(orig_positions) == len(mod_positions):
            position_shifts = [mod_positions[i] - orig_positions[i] for i in range(len(orig_positions))]
            significant_shifts = [shift for shift in position_shifts if abs(shift) > 0]
            
            if significant_shifts:
                print(f"        Position shifts: {significant_shifts[:10]}")
                
                # Check for mathematical patterns in shifts
                if is_fibonacci_pattern(significant_shifts):
                    print(f"        *** FIBONACCI PATTERN IN POSITION SHIFTS ***")
                if is_prime_pattern(significant_shifts):
                    print(f"        *** PRIME PATTERN IN POSITION SHIFTS ***")

def is_fibonacci_pattern(numbers):
    """Check if numbers follow Fibonacci pattern"""
    if len(numbers) < 3:
        return False
    
    fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    
    for num in numbers[:5]:
        if num in fib_sequence:
            return True
    
    return False

def is_prime_pattern(numbers):
    """Check if numbers are prime"""
    for num in numbers[:5]:
        if is_prime(abs(num)):
            return True
    return False

def analyze_parser_behaviors(content):
    """Analyze how different CSS parsers might behave"""
    print("  Parser Behavior Analysis:")
    
    # Test different line ending treatments
    print("    Line Ending Normalization:")
    lf_content = content.replace('\r\n', '\n').replace('\r', '\n')
    crlf_content = content.replace('\n', '\r\n').replace('\r', '\r\n')
    
    analyze_asterisk_position_changes(content, lf_content, "LF Normalization")
    analyze_asterisk_position_changes(content, crlf_content, "CRLF Normalization")
    
    # Test BOM handling
    print("    BOM Handling:")
    with_bom = '\ufeff' + content
    analyze_asterisk_position_changes(content, with_bom, "BOM Addition")
    
    # Test tab/space normalization
    print("    Tab/Space Normalization:")
    tab_normalized = content.replace('    ', '\t').replace('   ', '\t').replace('  ', '\t')
    space_normalized = content.replace('\t', '    ')
    
    analyze_asterisk_position_changes(content, tab_normalized, "Tab Normalization")
    analyze_asterisk_position_changes(content, space_normalized, "Space Normalization")
    
    # Test encoding variations
    print("    Encoding Variations:")
    try:
        # Test UTF-8 vs Latin-1
        latin1_content = content.encode('latin-1', errors='ignore').decode('latin-1')
        analyze_asterisk_position_changes(content, latin1_content, "Latin-1 Encoding")
        
        # Test Windows-1252
        win1252_content = content.encode('windows-1252', errors='ignore').decode('windows-1252')
        analyze_asterisk_position_changes(content, win1252_content, "Windows-1252 Encoding")
    except:
        pass

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main():
    print("CSS NORMALIZATION CYBERWEAPON ANALYZER")
    print("=" * 50)
    
    analyze_normalization_variants()
    
    print("\n=== NORMALIZATION ANALYSIS COMPLETE ===")
    print("If any asterisk position changes were detected,")
    print("this indicates the cyberweapon exploits normalization differences!")

if __name__ == "__main__":
    main()
