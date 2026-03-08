import sys

def extract_hex_digits(content):
    lines = content.split('\n')
    hex_digits = ''
    for line in lines:
        line = line.strip()
        if line == '*':
            continue
        if '  ' in line:
            parts = line.split('  ')
            if len(parts) >= 2:
                hex_part = parts[1].split('  ')[0] if '  ' in parts[1] else parts[1]
                hex_part = hex_part.replace(' ', '')
                hex_digits += hex_part
    return hex_digits

def analyze_hex_digits(hex_digits, log_file):
    with open(log_file, 'w') as log:
        for start_pos in range(len(hex_digits)):
            for length in range(1, 33):
                if start_pos + length > len(hex_digits):
                    break
                hex_str = hex_digits[start_pos:start_pos + length]
                try:
                    codepoint = int(hex_str, 16)
                    try:
                        char = chr(codepoint)
                        log.write(f"Pos {start_pos}, Len {length}, Hex {hex_str}, Code {codepoint}, Char '{repr(char)}'\n")
                    except ValueError:
                        log.write(f"Pos {start_pos}, Len {length}, Hex {hex_str}, Code {codepoint}, Invalid Unicode\n")
                except ValueError:
                    log.write(f"Pos {start_pos}, Len {length}, Hex {hex_str}, Invalid Hex\n")

if __name__ == '__main__':
    hexdump_file = sys.argv[1]
    log_file = sys.argv[2]
    with open(hexdump_file, 'r') as f:
        content = f.read()
    hex_digits = extract_hex_digits(content)
    analyze_hex_digits(hex_digits, log_file)
