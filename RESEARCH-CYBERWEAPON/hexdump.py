import sys

def hexdump(data, squeeze=True):
    lines = []
    prev_hex_ascii = None
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        line = f'{i:08x}  {hex_part:<48}  |{ascii_part}|'
        current_hex_ascii = line[10:]  # the hex and ascii part
        if squeeze and prev_hex_ascii and prev_hex_ascii == current_hex_ascii:
            if lines and lines[-1] != '*':
                lines.append('*')
        else:
            lines.append(line)
        prev_hex_ascii = current_hex_ascii
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    file_path = sys.argv[1]
    output_squeezed = sys.argv[2]
    output_unsqueezed = sys.argv[3]
    with open(file_path, 'rb') as f:
        data = f.read()
    squeezed = hexdump(data, squeeze=True)
    unsqueezed = hexdump(data, squeeze=False)
    with open(output_squeezed, 'w') as f:
        f.write(squeezed)
    with open(output_unsqueezed, 'w') as f:
        f.write(unsqueezed)
