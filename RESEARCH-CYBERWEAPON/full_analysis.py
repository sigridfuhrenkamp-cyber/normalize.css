import os
import glob
from collections import Counter

logs_dir = 'logs'
suspicious_chars = ['\\u2029', '\\u202e', '\\u200b', '\\u200c', '\\u200d', '\\u2060']
all_chars = []
unique_chars = set()

for log_file in glob.glob(os.path.join(logs_dir, '*.log')):
    with open(log_file, 'r') as f:
        for line in f:
            if 'Char' in line:
                parts = line.split("Char '")
                if len(parts) > 1:
                    char_repr = parts[1].split("'")[0]
                    all_chars.append(char_repr)
                    unique_chars.add(char_repr)

# Count occurrences
char_counts = Counter(all_chars)

# Print suspicious chars
print("Suspicious Unicode characters found:")
for char in suspicious_chars:
    count = char_counts.get(char, 0)
    print(f"{char}: {count} occurrences")

# Print total unique chars
print(f"\nTotal unique valid Unicode characters: {len(unique_chars)}")

# Print top 10 most common chars
print("\nTop 10 most common characters:")
for char, count in char_counts.most_common(10):
    print(f"{char}: {count}")

# Look for printable sequences (simple check)
print("\nChecking for potential hidden messages (consecutive printable chars):")
# This is a simple check: if multiple consecutive lines have printable chars, flag it
# But since logs are not sequential, it's hard. For now, skip or add later.

# To find patterns, perhaps look for sequences of printable chars in the hex, but that's complex.
# For now, this aggregates.
