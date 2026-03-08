import os
import glob

logs_dir = 'logs'
findings = {}

for log_file in glob.glob(os.path.join(logs_dir, '*.log')):
    counts = {'total': 0, 'valid': 0, 'invalid_unicode': 0, 'invalid_hex': 0}
    with open(log_file, 'r') as f:
        for line in f:
            counts['total'] += 1
            if 'Invalid Unicode' in line:
                counts['invalid_unicode'] += 1
            elif 'Invalid Hex' in line:
                counts['invalid_hex'] += 1
            elif 'Char' in line:
                counts['valid'] += 1
    findings[os.path.basename(log_file)] = counts

# Write findings to file
with open('findings.txt', 'w') as f:
    f.write('Findings Summary\n')
    f.write('================\n\n')
    for log_name, counts in findings.items():
        f.write(f'{log_name}:\n')
        f.write(f'  Total entries: {counts["total"]}\n')
        f.write(f'  Valid Unicode: {counts["valid"]}\n')
        f.write(f'  Invalid Unicode: {counts["invalid_unicode"]}\n')
        f.write(f'  Invalid Hex: {counts["invalid_hex"]}\n')
        f.write('\n')
