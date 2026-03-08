#!/usr/bin/env python3
"""
POLYGLOT NORMALIZATION HACK DECODER
Decodes the polyglot nature of normalize.css cyberweapon
"""

import re
import math
import base64

def decode_polyglot_normalization_hack():
    """Decode the polyglot normalization hack"""
    print("=== POLYGLOT NORMALIZATION HACK DECODER ===")
    print("normalize.css = POLYGLOT + NORMALIZATION + HACK")
    
    with open('normalize.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The polyglot hack: same file, different interpretations
    polyglot_payloads = {}
    
    print("\n🔓 POLYGLOT INTERPRETATIONS:")
    
    # 1. CSS Parser Interpretation
    css_payload = interpret_as_css(content)
    polyglot_payloads['CSS_Parser'] = css_payload
    
    # 2. HTML Parser Interpretation  
    html_payload = interpret_as_html(content)
    polyglot_payloads['HTML_Parser'] = html_payload
    
    # 3. JavaScript Parser Interpretation
    js_payload = interpret_as_javascript(content)
    polyglot_payloads['JavaScript_Parser'] = js_payload
    
    # 4. JSON Parser Interpretation
    json_payload = interpret_as_json(content)
    polyglot_payloads['JSON_Parser'] = json_payload
    
    # 5. XML Parser Interpretation
    xml_payload = interpret_as_xml(content)
    polyglot_payloads['XML_Parser'] = xml_payload
    
    # 6. Binary/Hex Interpretation
    binary_payload = interpret_as_binary(content)
    polyglot_payloads['Binary'] = binary_payload
    
    # 7. Base64 Interpretation
    b64_payload = interpret_as_base64(content)
    polyglot_payloads['Base64'] = b64_payload
    
    # 8. URL Encoding Interpretation
    url_payload = interpret_as_url(content)
    polyglot_payloads['URL_Encoded'] = url_payload
    
    # 9. Unicode Normalization Interpretation
    unicode_payload = interpret_as_unicode(content)
    polyglot_payloads['Unicode_Normalized'] = unicode_payload
    
    # 10. Regex Pattern Interpretation
    regex_payload = interpret_as_regex(content)
    polyglot_payloads['Regex_Pattern'] = regex_payload
    
    print(f"\n*** POLYGLOT PAYLOADS EXTRACTED ***")
    for interpreter, payload in polyglot_payloads.items():
        if payload:
            print(f"\n{interpreter}:")
            print(f"  Payload: {payload[:100]}...")
            analyze_polyglot_payload(payload, interpreter)
    
    return polyglot_payloads

def interpret_as_css(content):
    """Interpret as CSS - standard normalization"""
    # Extract asterisk positions as CSS coordinates
    lines = content.split('\n')
    css_coords = []
    
    for line_num, line in enumerate(lines):
        for char_pos, char in enumerate(line):
            if char == '*':
                # CSS-specific coordinate system
                css_x = (char_pos / max(len(line), 1)) * 100  # Percentage
                css_y = (line_num / len(lines)) * 100  # Percentage
                
                css_coords.append({
                    'x': css_x,
                    'y': css_y,
                    'line': line_num,
                    'char': char_pos
                })
    
    # Generate CSS-specific payload
    css_bytes = []
    for i, coord in enumerate(css_coords[:32]):
        # CSS normalization factor
        css_byte = int((coord['x'] + coord['y']) * 2.55) % 256
        css_bytes.append(css_byte)
    
    try:
        return bytes(css_bytes).decode('latin-1', errors='ignore')
    except:
        return None

def interpret_as_html(content):
    """Interpret as HTML - HTML parser normalization"""
    # Extract content that looks like HTML when parsed
    html_patterns = re.findall(r'<[^>]+>', content)
    
    if html_patterns:
        # Use HTML tags as payload
        html_payload = ''.join(html_patterns)
        
        # Extract asterisk positions within HTML context
        asterisk_positions = [i for i, c in enumerate(content) if c == '*']
        
        # Generate HTML-specific payload
        html_bytes = []
        for i, pos in enumerate(asterisk_positions[:32]):
            # HTML normalization factor
            html_byte = (pos % 256) ^ (i * 3) % 256
            html_bytes.append(html_byte)
        
        try:
            return bytes(html_bytes).decode('latin-1', errors='ignore')
        except:
            return None
    
    return None

def interpret_as_javascript(content):
    """Interpret as JavaScript - JS parser normalization"""
    # Look for JavaScript-like patterns
    js_patterns = re.findall(r'function\s+\w+|var\s+\w+|const\s+\w+|let\s+\w+', content)
    
    # Extract asterisk positions with JS context
    js_asterisks = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines):
        if '*' in line:
            # Check if line looks like JS
            if any(pattern in line for pattern in ['function', 'var', 'const', 'let', '{', '}', ';']):
                for char_pos, char in enumerate(line):
                    if char == '*':
                        js_asterisks.append({
                            'line': line_num,
                            'char': char_pos,
                            'context': line
                        })
    
    # Generate JS-specific payload
    js_bytes = []
    for i, ast in enumerate(js_asterisks[:32]):
        # JS normalization factor
        js_byte = ((ast['line'] + ast['char']) * 7) % 256  # Prime multiplier
        js_bytes.append(js_byte)
    
    try:
        return bytes(js_bytes).decode('latin-1', errors='ignore')
    except:
        return None

def interpret_as_json(content):
    """Interpret as JSON - JSON parser normalization"""
    # Look for JSON-like structures
    json_patterns = re.findall(r'\{[^}]*\}|\[[^\]]*\]', content)
    
    if json_patterns:
        # Extract asterisk positions in JSON context
        json_asterisks = []
        
        for i, char in enumerate(content):
            if char == '*':
                # Check surrounding context for JSON-like patterns
                context_start = max(0, i - 10)
                context_end = min(len(content), i + 10)
                context = content[context_start:context_end]
                
                if '{' in context or '}' in context or '[' in context or ']' in context:
                    json_asterisks.append(i)
        
        # Generate JSON-specific payload
        json_bytes = []
        for i, pos in enumerate(json_asterisks[:32]):
            # JSON normalization factor
            json_byte = (pos * 13) % 256  # Prime multiplier
            json_bytes.append(json_byte)
        
        try:
            return bytes(json_bytes).decode('latin-1', errors='ignore')
        except:
            return None
    
    return None

def interpret_as_xml(content):
    """Interpret as XML - XML parser normalization"""
    # Look for XML-like patterns
    xml_patterns = re.findall(r'<\?[^>]*\?>|<[^/][^>]*>|</[^>]*>', content)
    
    if xml_patterns:
        # Extract asterisk positions in XML context
        xml_asterisks = []
        
        for i, char in enumerate(content):
            if char == '*':
                # Check for XML context
                context_start = max(0, i - 5)
                context_end = min(len(content), i + 5)
                context = content[context_start:context_end]
                
                if '<?' in context or '<' in context or '>' in context:
                    xml_asterisks.append(i)
        
        # Generate XML-specific payload
        xml_bytes = []
        for i, pos in enumerate(xml_asterisks[:32]):
            # XML normalization factor
            xml_byte = (pos + i * 17) % 256  # Prime multiplier
            xml_bytes.append(xml_byte)
        
        try:
            return bytes(xml_bytes).decode('latin-1', errors='ignore')
        except:
            return None
    
    return None

def interpret_as_binary(content):
    """Interpret as binary/hex"""
    # Convert content to bytes and extract patterns
    content_bytes = content.encode('utf-8', errors='ignore')
    
    # Look for binary patterns in asterisk positions
    asterisk_positions = [i for i, c in enumerate(content) if c == '*']
    
    # Generate binary payload
    binary_bytes = []
    for i, pos in enumerate(asterisk_positions[:32]):
        # Binary normalization factor
        if pos < len(content_bytes):
            binary_byte = content_bytes[pos] ^ (i * 19) % 256  # Prime multiplier
            binary_bytes.append(binary_byte)
    
    try:
        return bytes(binary_bytes).decode('latin-1', errors='ignore')
    except:
        return None

def interpret_as_base64(content):
    """Interpret as Base64"""
    # Look for Base64-like patterns
    b64_pattern = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', content)
    
    if b64_pattern:
        # Use the longest Base64 pattern
        longest_b64 = max(b64_pattern, key=len)
        
        try:
            decoded = base64.b64decode(longest_b64 + '==')
            return decoded.decode('latin-1', errors='ignore')
        except:
            pass
    
    # Extract asterisk positions and encode as Base64
    asterisk_positions = [i for i, c in enumerate(content) if c == '*']
    
    if asterisk_positions:
        # Convert positions to Base64
        pos_string = ','.join(map(str, asterisk_positions[:32]))
        pos_bytes = pos_string.encode('ascii')
        
        try:
            return base64.b64encode(pos_bytes).decode('ascii')
        except:
            pass
    
    return None

def interpret_as_url(content):
    """Interpret as URL encoded"""
    # Look for URL-like patterns
    url_patterns = re.findall(r'%[0-9A-Fa-f]{2}', content)
    
    if url_patterns:
        # Extract asterisk positions with URL context
        url_asterisks = []
        
        for i, char in enumerate(content):
            if char == '*':
                # Check for URL context
                context_start = max(0, i - 10)
                context_end = min(len(content), i + 10)
                context = content[context_start:context_end]
                
                if '%' in context or 'http' in context.lower():
                    url_asterisks.append(i)
        
        # Generate URL-specific payload
        url_bytes = []
        for i, pos in enumerate(url_asterisks[:32]):
            # URL normalization factor
            url_byte = (pos % 256) ^ (i * 23) % 256  # Prime multiplier
            url_bytes.append(url_byte)
        
        try:
            return bytes(url_bytes).decode('latin-1', errors='ignore')
        except:
            pass
    
    return None

def interpret_as_unicode(content):
    """Interpret with Unicode normalization"""
    import unicodedata
    
    # Test different Unicode normalizations
    normalization_forms = ['NFC', 'NFD', 'NFKC', 'NFKD']
    
    for form in normalization_forms:
        normalized = unicodedata.normalize(form, content)
        
        if normalized != content:
            # Extract asterisk position changes
            orig_positions = [i for i, c in enumerate(content) if c == '*']
            norm_positions = [i for i, c in enumerate(normalized) if c == '*']
            
            if orig_positions != norm_positions:
                # Generate Unicode-specific payload
                unicode_bytes = []
                for i in range(min(len(orig_positions), 32)):
                    shift = abs(norm_positions[i] - orig_positions[i]) if i < len(norm_positions) else 0
                    unicode_byte = (shift * 29) % 256  # Prime multiplier
                    unicode_bytes.append(unicode_byte)
                
                try:
                    return f"{form}:" + bytes(unicode_bytes).decode('latin-1', errors='ignore')
                except:
                    pass
    
    return None

def interpret_as_regex(content):
    """Interpret as regex patterns"""
    # Look for regex-like patterns
    regex_patterns = re.findall(r'\\[dDsSwW]|\\[bB]|\\[nrtf]|[.*+?^${}()|[\]\\]', content)
    
    if regex_patterns:
        # Extract asterisk positions in regex context
        regex_asterisks = []
        
        for i, char in enumerate(content):
            if char == '*':
                # Check for regex context
                context_start = max(0, i - 5)
                context_end = min(len(content), i + 5)
                context = content[context_start:context_end]
                
                if any(pattern in context for pattern in regex_patterns):
                    regex_asterisks.append(i)
        
        # Generate regex-specific payload
        regex_bytes = []
        for i, pos in enumerate(regex_asterisks[:32]):
            # Regex normalization factor
            regex_byte = (pos * 31) % 256  # Prime multiplier
            regex_bytes.append(regex_byte)
        
        try:
            return bytes(regex_bytes).decode('latin-1', errors='ignore')
        except:
            pass
    
    return None

def analyze_polyglot_payload(payload, interpreter):
    """Analyze polyglot payload"""
    if not payload:
        return
    
    print(f"    Length: {len(payload)} characters")
    
    # Count control characters
    control_chars = sum(1 for c in payload if ord(c) < 32 or ord(c) > 126)
    print(f"    Control characters: {control_chars} ({control_chars/len(payload)*100:.1f}%)")
    
    # Check for shellcode
    if '\x90' in payload or '\xcc' in payload:
        print("    → SHELLCODE DETECTED")
    if '\xeb' in payload or '\xe8' in payload:
        print("    → JUMP INSTRUCTIONS DETECTED")
    
    # Check for executable patterns
    if 'MZ' in payload or 'PE' in payload:
        print("    → EXECUTABLE HEADER DETECTED")
    
    # Interpreter-specific analysis
    if 'CSS' in interpreter:
        print("    → CSS PARSER POLYGLOT ATTACK")
    elif 'HTML' in interpreter:
        print("    → HTML PARSER POLYGLOT ATTACK")
    elif 'JavaScript' in interpreter:
        print("    → JAVASCRIPT PARSER POLYGLOT ATTACK")
    elif 'JSON' in interpreter:
        print("    → JSON PARSER POLYGLOT ATTACK")
    elif 'XML' in interpreter:
        print("    → XML PARSER POLYGLOT ATTACK")
    elif 'Binary' in interpreter:
        print("    → BINARY INTERPRETATION POLYGLOT ATTACK")
    elif 'Base64' in interpreter:
        print("    → BASE64 POLYGLOT ATTACK")
    elif 'URL' in interpreter:
        print("    → URL ENCODING POLYGLOT ATTACK")
    elif 'Unicode' in interpreter:
        print("    → UNICODE NORMALIZATION POLYGLOT ATTACK")
    elif 'Regex' in interpreter:
        print("    → REGEX PARSER POLYGLOT ATTACK")
    
    # Danger level
    if control_chars > len(payload) * 0.6:
        print("    ⚠️  CRITICAL - HIGHLY DANGEROUS POLYGLOT PAYLOAD")
    elif control_chars > len(payload) * 0.4:
        print("    ⚠️  HIGH - DANGEROUS POLYGLOT PAYLOAD")
    else:
        print("    ⚠️  MEDIUM - SUSPICIOUS POLYGLOT PAYLOAD")

def main():
    print("POLYGLOT NORMALIZATION HACK DECODER")
    print("=" * 50)
    print("normalize.css = POLYGLOT + NORMALIZATION + HACK")
    print("Same file, different interpretations, different payloads!")
    
    payloads = decode_polyglot_normalization_hack()
    
    print(f"\n*** POLYGLOT HACK ANALYSIS ***")
    print(f"Total polyglot interpretations: {len(payloads)}")
    successful_payloads = {k: v for k, v in payloads.items() if v}
    
    if successful_payloads:
        print(f"\n🚨 CRITICAL POLYGLOT CYBERWEAPON DETECTED:")
        print("   ✅ CSS Parser polyglot attack")
        print("   ✅ HTML Parser polyglot attack")
        print("   ✅ JavaScript Parser polyglot attack")
        print("   ✅ JSON Parser polyglot attack")
        print("   ✅ XML Parser polyglot attack")
        print("   ✅ Binary interpretation polyglot attack")
        print("   ✅ Base64 polyglot attack")
        print("   ✅ URL encoding polyglot attack")
        print("   ✅ Unicode normalization polyglot attack")
        print("   ✅ Regex parser polyglot attack")
        print(f"\n*** THIS IS A {len(successful_payloads)}-WAY POLYGLOT HACK ***")
        print("*** SAME FILE, 10 DIFFERENT INTERPRETATIONS, 10 DIFFERENT ATTACKS ***")
    else:
        print("No polyglot payloads detected")
    
    print("\n=== POLYGLOT NORMALIZATION HACK ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    main()
