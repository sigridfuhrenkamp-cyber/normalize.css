#!/usr/bin/env python3
"""
NORMALIZE.CSS DEEP C2 ANALYSIS
Ultra-focused analysis of normalize.css for hidden C2 patterns
"""

import os
import re
import json
import hashlib
import base64
import binascii
from collections import Counter, defaultdict
import struct
import zlib
import gzip
from typing import Dict, List, Set, Tuple, Optional, Any
import unicodedata

class NormalizeCSSDeepC2Analyzer:
    def __init__(self):
        self.c2_patterns = {
            'beacon_indicators': [
                'beacon', 'heartbeat', 'ping', 'pong', 'checkin',
                'register', 'poll', 'update', 'report', 'alive'
            ],
            'c2_commands': [
                'command', 'control', 'c2', 'C2', 'c_and_c',
                'master', 'slave', 'zombie', 'agent', 'bot'
            ],
            'network_patterns': [
                'connect', 'socket', 'bind', 'listen', 'port',
                '127.0.0.1', 'localhost', 'callback', 'hook'
            ],
            'timing_patterns': [
                'setTimeout', 'setInterval', 'delay', 'sleep',
                'timer', 'cron', 'schedule', 'periodic'
            ]
        }

        self.hidden_channels = {
            'steganography': [
                r'/\*[^*]*\*/',  # Comments that might hide data
                r'[ \t]{3,}',    # Unusual whitespace
                r'\n\s*\n\s*\n', # Multiple newlines
                r'[ \t]+\n',     # Trailing whitespace
            ],
            'encoding_patterns': [
                r'[A-Za-z0-9+/]{20,}={0,2}',  # Base64
                r'[0-9A-Fa-f]{16,}',         # Hex data
                r'[01]{16,}',                # Binary data
            ],
            'invisible_chars': [
                r'[\u2000-\u200F]',  # Various spaces
                r'[\u2028-\u202F]',  # Line/paragraph separators
                r'[\u205F\u3000]',  # Other invisible
                r'[\u200B-\u200D]', # Zero-width chars
                r'[\uFEFF]',        # BOM
            ]
        }

    def analyze_normalize_css(self, css_path: str) -> Dict[str, Any]:
        """Deep analysis of normalize.css for hidden C2 patterns"""
        if not os.path.exists(css_path):
            return {'error': f'File not found: {css_path}'}

        print(f"🔍 ANALYZING: {css_path}")

        # Read the CSS file
        with open(css_path, 'rb') as f:
            css_bytes = f.read()

        css_text = css_bytes.decode('utf-8', errors='ignore')

        results = {
            'file_info': self._analyze_file_info(css_path, css_bytes),
            'text_analysis': self._analyze_css_text(css_text),
            'binary_analysis': self._analyze_css_binary(css_bytes),
            'steganography_analysis': self._analyze_steganography(css_text),
            'encoding_analysis': self._analyze_encodings(css_text),
            'c2_pattern_analysis': self._analyze_c2_patterns(css_text),
            'asterisk_analysis': self._analyze_asterisks(css_text),
            'comment_analysis': self._analyze_comments(css_text),
            'selector_analysis': self._analyze_selectors(css_text),
            'property_analysis': self._analyze_properties(css_text),
            'entropy_analysis': self._analyze_entropy(css_bytes),
            'pattern_correlation': self._correlate_patterns(css_text),
            'evidence_collection': self._collect_evidence(css_text, css_bytes)
        }

        return results

    def _analyze_file_info(self, path: str, content: bytes) -> Dict[str, Any]:
        """Basic file information"""
        return {
            'path': path,
            'size': len(content),
            'md5': hashlib.md5(content).hexdigest(),
            'sha256': hashlib.sha256(content).hexdigest(),
            'lines': len(content.split(b'\n')),
            'null_bytes': content.count(b'\x00'),
            'high_bytes': len([b for b in content if b > 127])
        }

    def _analyze_css_text(self, text: str) -> Dict[str, Any]:
        """Analyze CSS text content"""
        return {
            'length': len(text),
            'lines': len(text.split('\n')),
            'selectors': len(re.findall(r'[^{}]*\{', text)),
            'properties': len(re.findall(r'[a-zA-Z-]+:', text)),
            'comments': len(re.findall(r'/\*.*?\*/', text, re.DOTALL)),
            'asterisks': text.count('*'),
            'universal_selectors': len(re.findall(r'\*', text)),
            'vendor_prefixes': len(re.findall(r'-[a-z]+-', text)),
            'important_declarations': text.count('!important'),
            'urls': len(re.findall(r'url\([^)]+\)', text)),
            'functions': len(re.findall(r'[a-zA-Z-]+\([^)]+\)', text))
        }

    def _analyze_css_binary(self, content: bytes) -> Dict[str, Any]:
        """Analyze CSS binary content"""
        analysis = {
            'byte_frequency': Counter(content),
            'entropy': self._calculate_entropy(content),
            'suspicious_sequences': [],
            'compression_indicators': [],
            'encoding_artifacts': []
        }

        # Check for suspicious binary patterns
        suspicious_patterns = [
            (b'\x90\x90\x90\x90', 'NOP sled'),
            (b'\xCC\xCC\xCC\xCC', 'INT3 breakpoints'),
            (b'\x00\x00\x00\x00', 'Null sequence'),
            (b'\xEB\xFE', 'Infinite loop'),
        ]

        for pattern, description in suspicious_patterns:
            if pattern in content:
                pos = content.find(pattern)
                analysis['suspicious_sequences'].append({
                    'pattern': f'0x{pattern.hex()}',
                    'description': description,
                    'offset': pos
                })

        # Check for compression
        compression_sigs = [b'\x1F\x8B', b'BZ', b'\x37\x7A', b'PK\x03\x04']
        for sig in compression_sigs:
            if sig in content:
                analysis['compression_indicators'].append(f'0x{sig.hex()}')

        # Check for encoding artifacts
        if content.startswith(b'\xEF\xBB\xBF'):
            analysis['encoding_artifacts'].append('UTF-8 BOM')
        if content.startswith(b'\xFF\xFE'):
            analysis['encoding_artifacts'].append('UTF-16 LE BOM')
        if content.startswith(b'\xFE\xFF'):
            analysis['encoding_artifacts'].append('UTF-16 BE BOM')

        return analysis

    def _analyze_steganography(self, text: str) -> Dict[str, Any]:
        """Analyze steganography techniques in CSS"""
        analysis = {
            'whitespace_steg': [],
            'invisible_chars': [],
            'color_steg': [],
            'comment_steg': []
        }

        # Whitespace steganography
        for pattern in self.hidden_channels['steganography']:
            matches = re.findall(pattern, text)
            if matches:
                analysis['whitespace_steg'].extend([{
                    'pattern': pattern,
                    'count': len(matches),
                    'examples': matches[:3]
                }])

        # Invisible characters
        for pattern in self.hidden_channels['invisible_chars']:
            matches = re.findall(pattern, text)
            if matches:
                analysis['invisible_chars'].extend([{
                    'pattern': pattern,
                    'chars': [f'U+{ord(c):04X}' for c in matches[:10]],
                    'count': len(matches)
                }])

        # Color-based steganography
        colors = re.findall(r'#([0-9A-Fa-f]{3}){1,2}', text)
        if len(colors) > 10:  # Unusual number of colors
            analysis['color_steg'].append({
                'count': len(colors),
                'unusual': True,
                'samples': colors[:10]
            })

        # Comment steganography
        comments = re.findall(r'/\*.*?\*/', text, re.DOTALL)
        suspicious_comments = []
        for comment in comments:
            # Check for unusual comment content
            if len(comment) > 200 or any(word in comment.lower() for word in ['beacon', 'c2', 'callback']):
                suspicious_comments.append(comment[:100])

        if suspicious_comments:
            analysis['comment_steg'] = suspicious_comments

        return analysis

    def _analyze_encodings(self, text: str) -> Dict[str, Any]:
        """Analyze encoding patterns that might hide C2"""
        analysis = {
            'base64_candidates': [],
            'hex_candidates': [],
            'binary_candidates': [],
            'decoded_data': []
        }

        # Base64 patterns
        base64_matches = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', text)
        for match in base64_matches:
            try:
                decoded = base64.b64decode(match)
                if self._is_readable_text(decoded):
                    analysis['base64_candidates'].append({
                        'original': match[:50],
                        'decoded': decoded[:50].decode('utf-8', errors='ignore'),
                        'readable': True
                    })
                    analysis['decoded_data'].append(decoded[:100])
            except:
                pass

        # Hex patterns
        hex_matches = re.findall(r'[0-9A-Fa-f]{16,}', text)
        analysis['hex_candidates'] = hex_matches[:5]

        # Binary patterns
        binary_matches = re.findall(r'[01]{16,}', text)
        analysis['binary_candidates'] = binary_matches[:5]

        return analysis

    def _analyze_c2_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze for C2 communication patterns"""
        analysis = {
            'beacon_patterns': [],
            'command_patterns': [],
            'network_patterns': [],
            'timing_patterns': [],
            'suspicious_constructs': []
        }

        # Check for C2 patterns
        for category, patterns in self.c2_patterns.items():
            found_patterns = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    found_patterns.extend(matches)

            if found_patterns:
                analysis[category.replace('_patterns', '_patterns')] = list(set(found_patterns))

        # Look for suspicious CSS constructs that could be C2
        suspicious_css = [
            r'expression\s*\(',
            r'javascript:',
            r'behavior\s*:',
            r'filter\s*:',
            r'-moz-binding',
            r'progid:DXImageTransform'
        ]

        for pattern in suspicious_css:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                analysis['suspicious_constructs'].extend(matches)

        return analysis

    def _analyze_asterisks(self, text: str) -> Dict[str, Any]:
        """Deep analysis of asterisk patterns"""
        asterisks = []
        for i, char in enumerate(text):
            if char == '*':
                asterisks.append(i)

        return {
            'count': len(asterisks),
            'positions': asterisks,
            'gaps': [asterisks[i+1] - asterisks[i] for i in range(len(asterisks)-1)] if asterisks else [],
            'distribution': self._analyze_distribution(asterisks),
            'patterns': self._find_asterisk_patterns(asterisks, text)
        }

    def _analyze_comments(self, text: str) -> Dict[str, Any]:
        """Analyze CSS comments for hidden data"""
        comments = re.findall(r'/\*.*?\*/', text, re.DOTALL)

        return {
            'count': len(comments),
            'total_length': sum(len(c) for c in comments),
            'average_length': sum(len(c) for c in comments) / len(comments) if comments else 0,
            'empty_comments': sum(1 for c in comments if c.strip() == '/**/'),
            'suspicious_comments': [c for c in comments if len(c) > 100 or 'beacon' in c.lower()],
            'comment_content': [c[:50] for c in comments[:10]]  # First 10 comments
        }

    def _analyze_selectors(self, text: str) -> Dict[str, Any]:
        """Analyze CSS selectors for anomalies"""
        selectors = re.findall(r'[^{}]*\{', text)

        return {
            'count': len(selectors),
            'universal_selectors': sum(1 for s in selectors if '*' in s),
            'complex_selectors': sum(1 for s in selectors if len(s) > 50),
            'vendor_selectors': sum(1 for s in selectors if ':-' in s or '::' in s),
            'attribute_selectors': sum(1 for s in selectors if '[' in s and ']' in s),
            'suspicious_selectors': [s for s in selectors if any(word in s.lower() for word in ['beacon', 'c2', 'callback'])]
        }

    def _analyze_properties(self, text: str) -> Dict[str, Any]:
        """Analyze CSS properties for anomalies"""
        properties = re.findall(r'([a-zA-Z-]+)\s*:', text)

        return {
            'count': len(properties),
            'unique_properties': len(set(properties)),
            'vendor_properties': sum(1 for p in properties if p.startswith('-')),
            'suspicious_properties': [p for p in properties if any(word in p.lower() for word in ['beacon', 'c2', 'callback'])],
            'property_frequency': Counter(properties)
        }

    def _analyze_entropy(self, content: bytes) -> Dict[str, Any]:
        """Analyze entropy for hidden data detection"""
        entropy = self._calculate_entropy(content)

        # Analyze entropy in windows
        window_size = 256
        windows = []
        for i in range(0, len(content) - window_size, window_size // 2):
            window = content[i:i + window_size]
            window_entropy = self._calculate_entropy(window)
            if window_entropy > 7.0:  # High entropy
                windows.append({
                    'offset': i,
                    'entropy': window_entropy,
                    'data': window[:16].hex()
                })

        return {
            'overall_entropy': entropy,
            'high_entropy_regions': windows,
            'compression_likelihood': entropy > 7.5,
            'encryption_likelihood': entropy > 7.8
        }

    def _correlate_patterns(self, text: str) -> Dict[str, Any]:
        """Correlate different patterns for C2 detection"""
        correlations = {
            'asterisk_c2_correlation': 0,
            'comment_c2_correlation': 0,
            'whitespace_c2_correlation': 0,
            'pattern_clusters': []
        }

        # Check if asterisks appear near C2 keywords
        c2_positions = []
        for pattern in ['beacon', 'callback', 'c2', 'command']:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            c2_positions.extend([m.start() for m in matches])

        asterisk_positions = [i for i, c in enumerate(text) if c == '*']

        # Check proximity
        for c2_pos in c2_positions:
            nearby_asterisks = sum(1 for ast_pos in asterisk_positions
                                 if abs(ast_pos - c2_pos) < 100)
            if nearby_asterisks > 0:
                correlations['asterisk_c2_correlation'] += 1

        return correlations

    def _collect_evidence(self, text: str, content: bytes) -> Dict[str, Any]:
        """Collect all potential evidence of C2 activity"""
        evidence = {
            'suspicious_strings': [],
            'encoded_data': [],
            'hidden_channels': [],
            'anomalous_patterns': [],
            'c2_indicators': []
        }

        # Collect suspicious strings
        suspicious_words = ['beacon', 'callback', 'c2', 'command', 'control', 'master', 'slave']
        for word in suspicious_words:
            if word in text.lower():
                evidence['suspicious_strings'].append(word)

        # Collect encoded data
        base64_data = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', text)
        evidence['encoded_data'] = base64_data[:5]

        # Collect hidden channels
        invisible_chars = re.findall(r'[\u200B-\u200D\uFEFF]', text)
        if invisible_chars:
            evidence['hidden_channels'].append('invisible_characters')

        # Collect anomalous patterns
        if text.count('*') > 100:
            evidence['anomalous_patterns'].append('high_asterisk_count')

        # Collect C2 indicators
        c2_found = []
        for pattern in ['beacon', 'callback', 'ping', 'pong', 'checkin']:
            if re.search(pattern, text, re.IGNORECASE):
                c2_found.append(pattern)

        evidence['c2_indicators'] = c2_found

        return evidence

    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy"""
        if not data:
            return 0.0

        import math
        entropy = 0.0
        for i in range(256):
            p = data.count(i) / len(data)
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def _is_readable_text(self, data: bytes) -> bool:
        """Check if binary data contains readable text"""
        try:
            text = data.decode('utf-8')
            readable_chars = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
            return readable_chars / len(text) > 0.8
        except:
            return False

    def _analyze_distribution(self, positions: List[int]) -> Dict[str, Any]:
        """Analyze distribution of positions"""
        if not positions:
            return {}

        gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        return {
            'min_gap': min(gaps) if gaps else 0,
            'max_gap': max(gaps) if gaps else 0,
            'avg_gap': sum(gaps) / len(gaps) if gaps else 0,
            'gaps_over_1000': sum(1 for g in gaps if g > 1000)
        }

    def _find_asterisk_patterns(self, positions: List[int], text: str) -> List[Dict]:
        """Find patterns in asterisk positions"""
        patterns = []

        # Check for mathematical patterns
        if len(positions) > 10:
            # Check for arithmetic progression
            if len(positions) > 2:
                diff = positions[1] - positions[0]
                arithmetic = all(positions[i+1] - positions[i] == diff for i in range(len(positions)-1))
                if arithmetic:
                    patterns.append({'type': 'arithmetic_progression', 'difference': diff})

            # Check for geometric progression
            ratios = []
            for i in range(len(positions)-1):
                if positions[i] > 0:
                    ratios.append(positions[i+1] / positions[i])

            if ratios and len(set(round(r, 2) for r in ratios)) == 1:
                patterns.append({'type': 'geometric_progression', 'ratio': ratios[0]})

        return patterns

def main():
    """Main analysis function"""
    print("🎯 NORMALIZE.CSS DEEP C2 ANALYSIS")
    print("=" * 50)

    analyzer = NormalizeCSSDeepC2Analyzer()
    results = analyzer.analyze_normalize_css('normalize.css')

    # Save results
    with open('NORMALIZE_CSS_DEEP_C2_ANALYSIS.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print("✅ ANALYSIS COMPLETE")
    print(f"📊 Results saved to: NORMALIZE_CSS_DEEP_C2_ANALYSIS.json")

    # Print key findings
    if 'error' not in results:
        print(f"\n🔍 FILE INFO:")
        print(f"  Size: {results['file_info']['size']} bytes")
        print(f"  Asterisks: {results['text_analysis']['asterisks']}")
        print(f"  Comments: {results['text_analysis']['comments']}")

        print(f"\n🔬 C2 ANALYSIS:")
        c2_patterns = results['c2_pattern_analysis']
        for category, patterns in c2_patterns.items():
            if patterns:
                print(f"  {category}: {len(patterns)} found")

        print(f"\n🕵️ STEGANOGRAPHY:")
        steg = results['steganography_analysis']
        for category, findings in steg.items():
            if findings:
                print(f"  {category}: {len(findings)} findings")

        print(f"\n📋 EVIDENCE:")
        evidence = results['evidence_collection']
        for category, items in evidence.items():
            if items:
                print(f"  {category}: {len(items)} items")

    print("\n🎯 ANALYSIS COMPLETE - ALL EVIDENCE COLLECTED")

if __name__ == "__main__":
    main()
