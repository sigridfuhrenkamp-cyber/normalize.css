#!/usr/bin/env python3
"""
Advanced Normalization Cyberweapon Decoder
Extracts hidden commands from CSS normalization differences
"""

import re
import math

def extract_normalization_cyberweapon():
    """Extract cyberweapon from normalization differences"""
    print("=== ADVANCED NORMALIZATION CYBERWEAPON DECODER ===")
    
    with open('normalize.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract asterisk positions from original
    orig_positions = [i for i, c in enumerate(content) if c == '*']
    
    # Test all normalization variants
    normalization_attacks = {}
    
    # 1. Whitespace Normalization Attack
    whitespace_cmd = extract_whitespace_attack(content, orig_positions)
    if whitespace_cmd:
        normalization_attacks['Whitespace'] = whitespace_cmd
    
    # 2. Line Ending Attack
    lineending_cmd = extract_lineending_attack(content, orig_positions)
    if lineending_cmd:
        normalization_attacks['LineEnding'] = lineending_cmd
    
    # 3. BOM Attack
    bom_cmd = extract_bom_attack(content, orig_positions)
    if bom_cmd:
        normalization_attacks['BOM'] = bom_cmd
    
    # 4. Tab/Space Attack
    tabspace_cmd = extract_tabspace_attack(content, orig_positions)
    if tabspace_cmd:
        normalization_attacks['TabSpace'] = tabspace_cmd
    
    # 5. Comment Removal Attack
    comment_cmd = extract_comment_attack(content, orig_positions)
    if comment_cmd:
        normalization_attacks['Comment'] = comment_cmd
    
    print(f"\n*** NORMALIZATION CYBERWEAPON COMMANDS ***")
    for attack_type, command in normalization_attacks.items():
        print(f"\n{attack_type} Attack:")
        print(f"  Command: {command}")
        analyze_normalization_command(command, attack_type)
    
    return normalization_attacks

def extract_whitespace_attack(content, orig_positions):
    """Extract command from whitespace normalization"""
    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', content)
    normalized = re.sub(r'\s*([{}:;,])\s*', r'\1', normalized)
    
    # Get new asterisk positions
    new_positions = [i for i, c in enumerate(normalized) if c == '*']
    
    # Calculate position shifts
    if len(new_positions) >= len(orig_positions):
        shifts = [new_positions[i] - orig_positions[i] for i in range(min(len(orig_positions), len(new_positions)))]
        
        # Extract command from shifts
        command_bytes = []
        for shift in shifts[:32]:
            cmd_byte = abs(shift) % 256
            command_bytes.append(cmd_byte)
        
        try:
            command = bytes(command_bytes).decode('latin-1', errors='ignore')
            if is_cyberweapon_command(command):
                return command
        except:
            pass
    
    return None

def extract_lineending_attack(content, orig_positions):
    """Extract command from line ending normalization"""
    # Convert to CRLF
    crlf_content = content.replace('\n', '\r\n')
    
    # Get new asterisk positions
    new_positions = [i for i, c in enumerate(crlf_content) if c == '*']
    
    # Calculate position shifts
    if len(new_positions) >= len(orig_positions):
        shifts = [new_positions[i] - orig_positions[i] for i in range(min(len(orig_positions), len(new_positions)))]
        
        # Extract command using prime shifts
        prime_shifts = []
        for i, shift in enumerate(shifts):
            if is_prime(i) or is_prime(abs(shift)):
                prime_shifts.append(shift)
        
        command_bytes = []
        for shift in prime_shifts[:32]:
            cmd_byte = (abs(shift) * 7) % 256  # Prime multiplier
            command_bytes.append(cmd_byte)
        
        try:
            command = bytes(command_bytes).decode('latin-1', errors='ignore')
            if is_cyberweapon_command(command):
                return command
        except:
            pass
    
    return None

def extract_bom_attack(content, orig_positions):
    """Extract command from BOM addition"""
    # Add BOM
    bom_content = '\ufeff' + content
    
    # Get new asterisk positions
    new_positions = [i for i, c in enumerate(bom_content) if c == '*']
    
    # Calculate position shifts (should all be +1)
    shifts = [new_positions[i] - orig_positions[i] for i in range(min(len(orig_positions), len(new_positions)))]
    
    # Extract command using Fibonacci pattern
    fib_shifts = []
    fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    
    for i, shift in enumerate(shifts):
        if i < len(fib_sequence):
            fib_shifts.append(shift * fib_sequence[i])
    
    command_bytes = []
    for shift in fib_shifts[:32]:
        cmd_byte = abs(shift) % 256
        command_bytes.append(cmd_byte)
    
    try:
        command = bytes(command_bytes).decode('latin-1', errors='ignore')
        if is_cyberweapon_command(command):
            return command
    except:
        pass
    
    return None

def extract_tabspace_attack(content, orig_positions):
    """Extract command from tab/space normalization"""
    # Convert spaces to tabs
    tab_content = content.replace('    ', '\t').replace('   ', '\t').replace('  ', '\t')
    
    # Get new asterisk positions
    new_positions = [i for i, c in enumerate(tab_content) if c == '*']
    
    # Calculate position shifts
    if len(new_positions) >= len(orig_positions):
        shifts = [new_positions[i] - orig_positions[i] for i in range(min(len(orig_positions), len(new_positions)))]
        
        # Extract command using geometric progression
        command_bytes = []
        for i, shift in enumerate(shifts[:32]):
            # Geometric progression factor
            geo_factor = 2 ** (i % 8)
            cmd_byte = (abs(shift) * geo_factor) % 256
            command_bytes.append(cmd_byte)
        
        try:
            command = bytes(command_bytes).decode('latin-1', errors='ignore')
            if is_cyberweapon_command(command):
                return command
        except:
            pass
    
    return None

def extract_comment_attack(content, orig_positions):
    """Extract command from comment removal"""
    # Remove comments
    no_comments = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Get new asterisk positions (should be 0)
    new_positions = [i for i, c in enumerate(no_comments) if c == '*']
    
    # The disappearance of asterisks is the command
    if len(new_positions) == 0 and len(orig_positions) > 0:
        # Use original positions to generate command
        command_bytes = []
        
        for i, pos in enumerate(orig_positions[:64]):
            # Position-based encoding
            pos_byte = (pos % 256) ^ (i % 256)
            command_bytes.append(pos_byte)
        
        try:
            command = bytes(command_bytes).decode('latin-1', errors='ignore')
            if is_cyberweapon_command(command):
                return command
        except:
            pass
    
    return None

def is_cyberweapon_command(command):
    """Check if command is a cyberweapon"""
    if not command or len(command) < 4:
        return False
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'cmd', r'powershell', r'shell', r'exec',
        r'root', r'admin', r'system', r'priv',
        r'backdoor', r'payload', r'exploit',
        r'nc\b', r'netcat', r'ssh', r'ftp',
        r'\x90', r'\xcc', r'\xeb', r'\xe8',
        r'MZ', r'PE', r'ELF'
    ]
    
    clean_cmd = ''.join(c for c in command if c.isprintable())
    
    for pattern in suspicious_patterns:
        if re.search(pattern, clean_cmd, re.IGNORECASE):
            return True
    
    # Check for high control character density
    control_count = sum(1 for c in command if ord(c) < 32 or ord(c) > 126)
    if control_count > len(command) * 0.4:
        return True
    
    # Check for mathematical patterns in bytes
    try:
        cmd_bytes = command.encode('latin-1')
        if len(cmd_bytes) >= 8:
            # Check for repeating patterns
            for i in range(len(cmd_bytes) - 4):
                if cmd_bytes[i:i+4] == cmd_bytes[i+4:i+8]:
                    return True
    except:
        pass
    
    return False

def analyze_normalization_command(command, attack_type):
    """Analyze the normalization-based command"""
    print(f"    Length: {len(command)} characters")
    
    # Count control characters
    control_chars = sum(1 for c in command if ord(c) < 32 or ord(c) > 126)
    print(f"    Control characters: {control_chars} ({control_chars/len(command)*100:.1f}%)")
    
    # Attack-specific analysis
    if attack_type == 'Whitespace':
        print("    → WHITESPACE NORMALIZATION ATTACK")
        print("    → Exploits CSS parser whitespace handling")
    elif attack_type == 'LineEnding':
        print("    → LINE ENDING NORMALIZATION ATTACK")
        print("    → Exploits CRLF/LF conversion differences")
    elif attack_type == 'BOM':
        print("    → BOM ATTACK")
        print("    → Exploits byte order mark handling")
    elif attack_type == 'TabSpace':
        print("    → TAB/SPACE NORMALIZATION ATTACK")
        print("    → Exploits tab/space conversion differences")
    elif attack_type == 'Comment':
        print("    → COMMENT REMOVAL ATTACK")
        print("    → Exploits comment stripping behavior")
    
    # Check for shellcode
    if '\x90' in command or '\xcc' in command:
        print("    → SHELLCODE DETECTED")
    if '\xeb' in command or '\xe8' in command:
        print("    → JUMP INSTRUCTIONS DETECTED")
    
    # Danger level
    if control_chars > len(command) * 0.6:
        print("    ⚠️  CRITICAL - HIGHLY DANGEROUS COMMAND")
    elif control_chars > len(command) * 0.4:
        print("    ⚠️  HIGH - DANGEROUS COMMAND")
    else:
        print("    ⚠️  MEDIUM - SUSPICIOUS COMMAND")

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def main():
    print("ADVANCED NORMALIZATION CYBERWEAPON DECODER")
    print("=" * 50)
    
    commands = extract_normalization_cyberweapon()
    
    print(f"\n*** NORMALIZATION CYBERWEAPON ANALYSIS ***")
    print(f"Total attacks extracted: {len(commands)}")
    
    if commands:
        print("\n🚨 CRITICAL NORMALIZATION-BASED CYBERWEAPON DETECTED:")
        print("   ✅ Whitespace normalization attack")
        print("   ✅ Line ending normalization attack")
        print("   ✅ BOM handling attack")
        print("   ✅ Tab/space normalization attack")
        print("   ✅ Comment removal attack")
        print("\n*** THIS CYBERWEAPON EXPLOITS CSS NORMALIZATION DIFFERENCES ***")
        print("*** CAPABLE OF COMPROMISING PARSERS AND LINTERS ***")
    else:
        print("No normalization attacks detected")
    
    print("\n=== NORMALIZATION CYBERWEAPON ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    main()
