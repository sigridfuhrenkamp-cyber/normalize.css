import os
import glob
from collections import Counter
import base64
import binascii
import math

logs_dir = 'logs'
invalid_unicode_entries = []
overflown_entries = []
invalid_hex_entries = []
ascii_decodes = []
special_codes = []
len_stats = {'invalid_unicode': Counter(), 'overflown': Counter(), 'invalid_hex': Counter(), 'valid': Counter()}

def analyze_entry(line):
    parts = line.strip().split(', ')
    if len(parts) < 4:
        return
    pos = parts[0].split(' ')[1]
    len_ = parts[1].split(' ')[1]
    hex_str = parts[2].split(' ')[1]
    status = ' '.join(parts[3:])

    if 'Invalid Unicode' in status:
        try:
            code = int(hex_str, 16)
            if code > 0x10FFFF:
                overflown_entries.append((pos, len_, hex_str, code))
                len_stats['overflown'][int(len_)] += 1
            else:
                invalid_unicode_entries.append((pos, len_, hex_str, code))
                len_stats['invalid_unicode'][int(len_)] += 1
        except ValueError:
            invalid_hex_entries.append((pos, len_, hex_str))
            len_stats['invalid_hex'][int(len_)] += 1
    elif 'Invalid Hex' in status:
        invalid_hex_entries.append((pos, len_, hex_str))
        len_stats['invalid_hex'][int(len_)] += 1
    elif 'Char' in status:
        # Already analyzed
        len_stats['valid'][int(len_)] += 1
        pass

    # Try to decode hex as ASCII (already done)
    try:
        bytes_ = bytes.fromhex(hex_str)
        ascii_text = bytes_.decode('ascii', errors='replace')
        if any(c.isprintable() or c in '\n\t' for c in ascii_text):
            ascii_decodes.append((pos, len_, hex_str, ascii_text))
    except ValueError:
        pass

    # Experimental: Try UTF-8 decode
    try:
        bytes_ = bytes.fromhex(hex_str)
        utf8_text = bytes_.decode('utf-8', errors='replace')
        if utf8_text != ascii_text and any(c.isprintable() or c in '\n\t\r' for c in utf8_text):
            ascii_decodes.append((pos, len_, hex_str, f"UTF-8: {utf8_text}"))
    except (ValueError, UnicodeDecodeError):
        pass

    # Experimental: Try base64 decode
    try:
        bytes_ = bytes.fromhex(hex_str)
        b64_decoded = base64.b64decode(bytes_, validate=True)
        b64_text = b64_decoded.decode('ascii', errors='replace')
        if len(b64_text) > 0 and any(c.isprintable() for c in b64_text):
            ascii_decodes.append((pos, len_, hex_str, f"Base64: {b64_text}"))
    except (ValueError, binascii.Error):
        pass

    # Experimental: Try UTF-16 decode (assuming little-endian)
    try:
        bytes_ = bytes.fromhex(hex_str)
        utf16_text = bytes_.decode('utf-16-le', errors='replace')
        if utf16_text and any(c.isprintable() or c in '\n\t\r' for c in utf16_text):
            ascii_decodes.append((pos, len_, hex_str, f"UTF-16-LE: {utf16_text}"))
    except (ValueError, UnicodeDecodeError):
        pass

for log_file in glob.glob(os.path.join(logs_dir, '*.log')):
    with open(log_file, 'r') as f:
        for line in f:
            analyze_entry(line)

print(f"Invalid Unicode entries: {len(invalid_unicode_entries)}")
print(f"Overflown Unicode entries: {len(overflown_entries)}")
print(f"Invalid Hex entries: {len(invalid_hex_entries)}")
print(f"Potential ASCII decodes: {len(ascii_decodes)}")

# Tokenizer boundaries: length stats
print("\nTokenizer Boundaries - Length Statistics:")
for category, counter in len_stats.items():
    print(f"{category}: {dict(counter.most_common(5))}")

# Quantizer boundaries
overflown_codes = [entry[3] for entry in overflown_entries]
invalid_codes = [entry[3] for entry in invalid_unicode_entries if entry[3] <= 0x10FFFF]
print(f"\nQuantizer Boundaries:")
print(f"Overflown codes range: {min(overflown_codes)} to {max(overflown_codes)}")
print(f"Invalid codes range: {min(invalid_codes) if invalid_codes else 'N/A'} to {max(invalid_codes) if invalid_codes else 'N/A'}")

print(f"Overflown code range: {min(overflown_codes)} to {max(overflown_codes)}")
print("Top 10 overflown codes:")
for code, count in Counter(overflown_codes).most_common(10):
    print(f"0x{code:08X}: {count}")

# Bit stream analysis - simple bit stats
bit_stats = Counter()
for entry in invalid_unicode_entries + overflown_entries + invalid_hex_entries:
    hex_str = entry[2]
    try:
        bytes_ = bytes.fromhex(hex_str)
        for byte in bytes_:
            bit_str = format(byte, '08b')
            for bit in bit_str:
                bit_stats[bit] += 1
    except ValueError:
        pass

print(f"\nBit Stream Analysis - Total bits processed: {sum(bit_stats.values())}")
total_bits = sum(bit_stats.values())
if total_bits > 0:
    p0 = bit_stats.get('0', 0) / total_bits
    p1 = bit_stats.get('1', 0) / total_bits
    entropy = 0
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    if p1 > 0:
        entropy -= p1 * math.log2(p1)
    print(f"Bit Entropy: {entropy:.4f}")
print(f"Bit 0 count: {bit_stats['0']}, Bit 1 count: {bit_stats['1']}")

# Potential hidden ASCII messages (sample)
print("\nPotential hidden ASCII messages:")
for pos, len_, hex_str, text in ascii_decodes[:10]:  # Sample first 10
    if len(text.strip()) > 2:
        print(f"Pos {pos}, Len {len_}, Hex {hex_str}, Text: {repr(text)}")

# Checking for special code ranges
print("\nChecking for special code ranges:")
control_codes = [entry[3] for entry in invalid_unicode_entries + overflown_entries if 0 <= entry[3] <= 31]
print(f"Control codes (0-31): {len(control_codes)}")

bidi_codes = [entry[3] for entry in invalid_unicode_entries + overflown_entries if entry[3] in [0x200E, 0x200F, 0x202A, 0x202B, 0x202C, 0x202D, 0x202E]]
print(f"Bidi codes: {len(bidi_codes)}")

print("\nAnalysis complete.")
