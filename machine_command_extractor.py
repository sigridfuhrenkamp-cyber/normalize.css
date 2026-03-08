#!/usr/bin/env python3
"""
Machine Command Extractor - Hidden cyberweapon payload decoder
Extracts system hacking commands from asterisk positioning
"""

import math
import re
import struct
import base64

def extract_machine_command():
    """Extract the hidden machine command for system hacking"""
    print("=== MACHINE COMMAND EXTRACTION ===")
    
    with open('normalize.css', 'r') as f:
        content = f.read()
    
    # Extract asterisk coordinates with military precision
    lines = content.split('\n')
    asterisk_matrix = []
    
    for line_num, line in enumerate(lines):
        for char_pos, char in enumerate(line):
            if char == '*':
                # Calculate military-grade coordinates
                total_lines = len(lines)
                line_len = len(line)
                
                # Boundary-based encoding
                line_boundary = min(line_num, total_lines - line_num - 1)
                char_boundary = min(char_pos, line_len - char_pos - 1) if line_len > 0 else 0
                
                # Normalize to 0-255 range for machine command
                x_coord = int((char_pos / max(line_len, 1)) * 255)
                y_coord = int((line_num / total_lines) * 255)
                boundary_byte = int(((line_boundary / (total_lines/2)) + (char_boundary / (max(line_len, 1)/2))) / 2 * 255)
                
                asterisk_matrix.append({
                    'x': x_coord,
                    'y': y_coord, 
                    'boundary': boundary_byte,
                    'line': line_num,
                    'char': char_pos
                })
    
    print(f"Built {len(asterisk_matrix)} coordinate matrix")
    
    # Extract machine command using multiple decoding layers
    machine_command = decode_machine_command(asterisk_matrix)
    
    if machine_command:
        print(f"\n*** MACHINE COMMAND EXTRACTED ***")
        print(f"Command: {machine_command}")
        
        # Analyze command type
        analyze_command_type(machine_command)
        
        return machine_command
    else:
        print("Machine command not found in standard extraction")
        # Try advanced extraction
        return advanced_command_extraction(asterisk_matrix)

def decode_machine_command(matrix):
    """Decode machine command from coordinate matrix"""
    if len(matrix) < 16:
        return None
    
    # Layer 1: Boundary-based byte extraction
    command_bytes = []
    
    # Use prime-numbered asterisks for core command
    prime_coords = []
    for i, coord in enumerate(matrix):
        if is_prime(coord['line']) or is_prime(coord['char']):
            prime_coords.append(coord)
    
    # Extract bytes from boundary positions
    for i in range(min(len(prime_coords), 32)):
        coord = prime_coords[i]
        
        # Multi-byte extraction
        byte1 = coord['x'] ^ coord['y']  # XOR for obfuscation
        byte2 = coord['boundary']
        byte3 = (coord['line'] + coord['char']) % 256
        
        command_bytes.extend([byte1, byte2, byte3])
    
    # Convert to command string
    try:
        # Try different encodings
        for encoding in ['ascii', 'latin-1', 'utf-8', 'cp1252']:
            try:
                command = bytes(command_bytes).decode(encoding, errors='ignore')
                if is_valid_command(command):
                    return command
            except:
                continue
    except:
        pass
    
    # Try as shell command with null bytes
    cleaned_bytes = [b for b in command_bytes if b != 0]
    try:
        command = bytes(cleaned_bytes).decode('ascii', errors='ignore')
        if is_valid_command(command):
            return command
    except:
        pass
    
    return None

def advanced_command_extraction(matrix):
    """Advanced extraction for hidden machine commands"""
    print("\n=== ADVANCED COMMAND EXTRACTION ===")
    
    # Method 1: Geometric pattern extraction
    geometric_command = extract_geometric_command(matrix)
    if geometric_command:
        print(f"Geometric command: {geometric_command}")
        return geometric_command
    
    # Method 2: Fibonacci-based extraction
    fib_command = extract_fibonacci_command(matrix)
    if fib_command:
        print(f"Fibonacci command: {fib_command}")
        return fib_command
    
    # Method 3: Boundary sequence extraction
    boundary_command = extract_boundary_command(matrix)
    if boundary_command:
        print(f"Boundary command: {boundary_command}")
        return boundary_command
    
    return None

def extract_geometric_command(matrix):
    """Extract command using geometric positioning"""
    if len(matrix) < 8:
        return None
    
    # Use angles between asterisks to encode command
    angles = []
    for i in range(1, min(len(matrix), 16)):
        x1, y1 = matrix[i-1]['x'], matrix[i-1]['y']
        x2, y2 = matrix[i]['x'], matrix[i]['y']
        
        angle = math.atan2(y2 - y1, x2 - x1)
        angles.append(angle)
    
    # Convert angles to command bytes
    command_bytes = []
    for angle in angles:
        # Map angle to byte (0-255)
        normalized_angle = (angle + math.pi) / (2 * math.pi)  # Normalize to 0-1
        byte_val = int(normalized_angle * 255)
        command_bytes.append(byte_val)
    
    try:
        command = bytes(command_bytes).decode('ascii', errors='ignore')
        if is_valid_command(command):
            return command
    except:
        pass
    
    return None

def extract_fibonacci_command(matrix):
    """Extract command using Fibonacci positioning"""
    fib_numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    
    fib_coords = []
    for coord in matrix:
        if coord['line'] in fib_numbers or coord['char'] in fib_numbers:
            fib_coords.append(coord)
    
    if len(fib_coords) < 4:
        return None
    
    # Extract command from Fibonacci positions
    command_bytes = []
    for i in range(min(len(fib_coords), 16)):
        coord = fib_coords[i]
        # Fibonacci-based byte calculation
        fib_byte = (coord['x'] + coord['y'] + coord['boundary']) % 256
        command_bytes.append(fib_byte)
    
    try:
        command = bytes(command_bytes).decode('ascii', errors='ignore')
        if is_valid_command(command):
            return command
    except:
        pass
    
    return None

def extract_boundary_command(matrix):
    """Extract command from boundary positioning"""
    # Sort by boundary factor
    sorted_coords = sorted(matrix, key=lambda x: x['boundary'])
    
    # Use boundary positions to encode command
    command_bytes = []
    for i in range(min(len(sorted_coords), 32)):
        coord = sorted_coords[i]
        # Boundary-based encoding
        boundary_byte = (coord['boundary'] * 255) % 256
        position_byte = ((coord['line'] + coord['char']) * 7) % 256  # Prime multiplier
        command_bytes.extend([boundary_byte, position_byte])
    
    try:
        command = bytes(command_bytes).decode('ascii', errors='ignore')
        if is_valid_command(command):
            return command
    except:
        pass
    
    return None

def is_valid_command(command):
    """Check if extracted string is a valid system command"""
    if not command or len(command) < 2:
        return False
    
    # Remove null bytes and non-printable chars
    clean_command = ''.join(c for c in command if c.isprintable() and c != '\x00')
    
    # Check for command indicators
    command_patterns = [
        r'\bcmd\b', r'\bpowershell\b', r'\bbash\b', r'\bsh\b',
        r'\bsudo\b', r'\badmin\b', r'\broot\b', r'\bsystem\b',
        r'\bexec\b', r'\brun\b', r'\bstart\b', r'\blaunch\b',
        r'\bnet\b', r'\bssh\b', r'\bftp\b', r'\btelnet\b',
        r'\bnc\b', r'\bnmap\b', r'\bmsf\b', r'\bexploit\b',
        r'\bpayload\b', r'\bshell\b', r'\bbackdoor\b', r'\brootkit\b'
    ]
    
    # Check for system commands
    for pattern in command_patterns:
        if re.search(pattern, clean_command, re.IGNORECASE):
            return True
    
    # Check for file operations
    file_patterns = [
        r'\.exe', r'\.bat', r'\.cmd', r'\.ps1', r'\.sh',
        r'\.dll', r'\.so', r'\.dylib', r'/', r'\\',
        r'C:\\', r'/etc/', r'/usr/', r'/var/', r'/tmp/'
    ]
    
    for pattern in file_patterns:
        if re.search(pattern, clean_command):
            return True
    
    # Check for network operations
    network_patterns = [
        r'http://', r'https://', r'ftp://', r'ssh://',
        r'\bconnect\b', r'\bbind\b', r'\blisten\b', r'\bport\b',
        r'\bTCP\b', r'\bUDP\b', r'\bIP\b', r'\bhost\b'
    ]
    
    for pattern in network_patterns:
        if re.search(pattern, clean_command, re.IGNORECASE):
            return True
    
    # Check if it looks like a command (has spaces, special chars)
    if (len(clean_command) > 5 and 
        (' ' in clean_command or '-' in clean_command or '/' in clean_command)):
        return True
    
    return False

def analyze_command_type(command):
    """Analyze the type of system command"""
    print(f"\n=== COMMAND ANALYSIS ===")
    
    clean_command = ''.join(c for c in command if c.isprintable() and c != '\x00')
    
    # Categorize command type
    if re.search(r'\bcmd\b|command\.|cmd\.exe', clean_command, re.IGNORECASE):
        print("Command Type: Windows CMD")
    elif re.search(r'\bpowershell\b|ps1\b', clean_command, re.IGNORECASE):
        print("Command Type: PowerShell")
    elif re.search(r'\bbash\b|sh\b|\.sh$', clean_command, re.IGNORECASE):
        print("Command Type: Unix Shell")
    elif re.search(r'\bsudo\b|admin\b|root\b', clean_command, re.IGNORECASE):
        print("Command Type: Privilege Escalation")
    elif re.search(r'\bnet\b|ssh\b|ftp\b|connect\b', clean_command, re.IGNORECASE):
        print("Command Type: Network/Remote Access")
    elif re.search(r'\bexploit\b|payload\b|msf\b', clean_command, re.IGNORECASE):
        print("Command Type: Exploitation Framework")
    else:
        print("Command Type: Unknown/System Command")
    
    # Check for dangerous indicators
    dangerous_patterns = [
        r'\bformat\b', r'\bdelete\b', r'\bremove\b', r'\bkill\b',
        r'\bshutdown\b', r'\breboot\b', r'\bcrash\b', r'\bdestroy\b'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, clean_command, re.IGNORECASE):
            print("⚠️  DANGEROUS COMMAND DETECTED - SYSTEM DESTRUCTION CAPABILITY")
            break
    
    # Check for backdoor patterns
    backdoor_patterns = [
        r'\bbackdoor\b', r'\brootkit\b', r'\btrojan\b', r'\bpersistence\b',
        r'\bservice\b', r'\bdaemon\b', r'\bstartup\b', r'\bregistry\b'
    ]
    
    for pattern in backdoor_patterns:
        if re.search(pattern, clean_command, re.IGNORECASE):
            print("⚠️  BACKDOOR/PERSISTENCE DETECTED")
            break

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def main():
    print("MACHINE COMMAND EXTRACTOR - CYBERWEAPON PAYLOAD DECODER")
    print("=" * 60)
    
    machine_command = extract_machine_command()
    
    if machine_command:
        print(f"\n*** COMPLETE MACHINE COMMAND ***")
        print(f"'{machine_command}'")
        print(f"Length: {len(machine_command)} characters")
        
        # Show raw bytes for analysis
        try:
            raw_bytes = machine_command.encode('latin-1')
            print(f"Raw bytes: {raw_bytes.hex()[:100]}...")
        except:
            pass
    else:
        print("Machine command could not be extracted")
    
    print("\n=== EXTRACTION COMPLETE ===")

if __name__ == "__main__":
    main()
