#!/usr/bin/env python3
"""
REMOTE CSS PROJECT C2 ANALYZER
Analyzes remote CSS normalization projects for C2 patterns
"""

import urllib.request
import urllib.error
import json
import hashlib
from typing import Dict, Any
import re

class RemoteCSSC2Analyzer:
    def __init__(self):
        self.projects = {
            'sanitize.css': {
                'url': 'https://raw.githubusercontent.com/csstools/sanitize.css/main/sanitize.css',
                'description': 'CSS normalization and opinionated reset'
            },
            'modern-normalize': {
                'url': 'https://raw.githubusercontent.com/sindresorhus/modern-normalize/main/modern-normalize.css',
                'description': 'Modern alternative to CSS resets'
            },
            'ress': {
                'url': 'https://raw.githubusercontent.com/filipelinhares/ress/master/ress.css',
                'description': 'Modern CSS reset'
            },
            'normalize.css': {
                'url': 'https://raw.githubusercontent.com/necolas/normalize.css/master/normalize.css',
                'description': 'Modern, HTML5-ready alternative to CSS resets'
            }
        }

        self.c2_patterns = {
            'beacon_indicators': ['beacon', 'heartbeat', 'ping', 'pong', 'checkin', 'poll'],
            'c2_commands': ['command', 'control', 'c2', 'master', 'slave', 'zombie'],
            'network_patterns': ['connect', 'socket', 'bind', 'listen', 'callback'],
            'timing_patterns': ['setTimeout', 'setInterval', 'delay', 'cron', 'schedule']
        }

    def analyze_all_projects(self) -> Dict[str, Any]:
        """Analyze all remote CSS projects for C2 patterns"""
        results = {}

        for project_name, project_info in self.projects.items():
            print(f"🔍 Analyzing {project_name}...")
            try:
                results[project_name] = self.analyze_project(project_name, project_info)
            except Exception as e:
                results[project_name] = {'error': str(e)}

        # Cross-project comparison
        results['comparison'] = self.compare_projects(results)

        return results

    def analyze_project(self, name: str, info: Dict) -> Dict[str, Any]:
        """Analyze a single remote CSS project"""
        try:
            with urllib.request.urlopen(info['url'], timeout=10) as response:
                css_content = response.read().decode('utf-8')

            return {
                'info': info,
                'file_analysis': self.analyze_css_content(css_content),
                'c2_analysis': self.analyze_c2_patterns(css_content),
                'steganography': self.analyze_steganography(css_content),
                'encoding_analysis': self.analyze_encodings(css_content),
                'security_assessment': self.assess_security(css_content)
            }

        except Exception as e:
            return {'error': str(e), 'url': info['url']}

    def analyze_css_content(self, content: str) -> Dict[str, Any]:
        """Analyze basic CSS content"""
        return {
            'size': len(content),
            'lines': len(content.split('\n')),
            'selectors': len(re.findall(r'[^{}]*\{', content)),
            'properties': len(re.findall(r'[a-zA-Z-]+:', content)),
            'comments': len(re.findall(r'/\*.*?\*/', content, re.DOTALL)),
            'asterisks': content.count('*'),
            'vendor_prefixes': len(re.findall(r'-[a-z]+-', content))
        }

    def analyze_c2_patterns(self, content: str) -> Dict[str, Any]:
        """Analyze C2 communication patterns"""
        findings = {}

        for category, patterns in self.c2_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, content, re.IGNORECASE)
                if found:
                    matches.extend(found)

            if matches:
                findings[category] = {
                    'count': len(matches),
                    'patterns': list(set(matches)),
                    'positions': [m.start() for m in re.finditer('|'.join(patterns), content, re.IGNORECASE)]
                }

        return findings

    def analyze_steganography(self, content: str) -> Dict[str, Any]:
        """Analyze steganography techniques"""
        return {
            'invisible_chars': re.findall(r'[\u2000-\u200F\u2028-\u202F\u205F\u3000\u200B-\u200D\uFEFF]', content),
            'whitespace_patterns': re.findall(r'[ \t]{5,}', content),
            'color_steg': re.findall(r'#[0-9A-Fa-f]{6}', content),
            'suspicious_comments': [c for c in re.findall(r'/\*.*?\*/', content, re.DOTALL) if len(c) > 200]
        }

    def analyze_encodings(self, content: str) -> Dict[str, Any]:
        """Analyze encoding patterns"""
        return {
            'base64_patterns': re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', content),
            'hex_patterns': re.findall(r'[0-9A-Fa-f]{16,}', content),
            'unicode_escapes': re.findall(r'\\[uU][0-9A-Fa-f]{4,8}', content),
            'html_entities': re.findall(r'&#[0-9]+;', content)
        }

    def assess_security(self, content: str) -> Dict[str, Any]:
        """Assess security implications"""
        risk_factors = []

        # Check for dangerous constructs
        if re.search(r'expression\s*\(', content, re.IGNORECASE):
            risk_factors.append('css_expressions')
        if re.search(r'javascript:', content, re.IGNORECASE):
            risk_factors.append('javascript_urls')
        if re.search(r'behavior\s*:', content, re.IGNORECASE):
            risk_factors.append('behavior_bindings')

        # Check for excessive asterisks
        asterisk_count = content.count('*')
        if asterisk_count > 50:
            risk_factors.append(f'high_asterisk_count_{asterisk_count}')

        # Check for C2 patterns
        c2_found = []
        for patterns in self.c2_patterns.values():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    c2_found.append(pattern)

        risk_level = 'LOW'
        if risk_factors:
            risk_level = 'MEDIUM'
        if c2_found:
            risk_level = 'HIGH'

        return {
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'c2_indicators': c2_found,
            'recommendations': self.generate_recommendations(risk_level, risk_factors)
        }

    def compare_projects(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare findings across projects"""
        comparison = {
            'risk_levels': {},
            'c2_findings': {},
            'common_patterns': {},
            'unique_anomalies': {}
        }

        for project_name, project_results in results.items():
            if project_name != 'comparison' and 'error' not in project_results:
                security = project_results.get('security_assessment', {})
                comparison['risk_levels'][project_name] = security.get('risk_level', 'UNKNOWN')

                c2_analysis = project_results.get('c2_analysis', {})
                if c2_analysis:
                    comparison['c2_findings'][project_name] = c2_analysis

        return comparison

    def generate_recommendations(self, risk_level: str, risk_factors: list) -> list:
        """Generate security recommendations"""
        recommendations = []

        if risk_level == 'HIGH':
            recommendations.append('CRITICAL: Contains C2 communication patterns - immediate investigation required')
        elif risk_level == 'MEDIUM':
            recommendations.append('WARNING: Contains potentially suspicious patterns - review recommended')
        else:
            recommendations.append('LOW RISK: No obvious security issues detected')

        for factor in risk_factors:
            if 'asterisk' in factor:
                recommendations.append('Review high asterisk count - may indicate steganographic encoding')
            if 'css_expressions' in factor:
                recommendations.append('CRITICAL: Contains CSS expressions - security vulnerability')
            if 'javascript_urls' in factor:
                recommendations.append('WARNING: Contains javascript: URLs - potential XSS vector')

        return recommendations

def main():
    """Main analysis function"""
    print("🌐 REMOTE CSS PROJECT C2 ANALYSIS")
    print("=" * 50)

    analyzer = RemoteCSSC2Analyzer()
    results = analyzer.analyze_all_projects()

    # Save results
    with open('REMOTE_CSS_PROJECTS_C2_ANALYSIS.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print("✅ ANALYSIS COMPLETE")
    print(f"📊 Results saved to: REMOTE_CSS_PROJECTS_C2_ANALYSIS.json")

    # Print summary
    comparison = results.get('comparison', {})
    print(f"\n🔒 RISK LEVELS ACROSS PROJECTS:")
    for project, risk in comparison.get('risk_levels', {}).items():
        print(f"  {project}: {risk}")

    print(f"\n🎯 C2 PATTERNS FOUND:")
    c2_findings = comparison.get('c2_findings', {})
    if c2_findings:
        for project, findings in c2_findings.items():
            print(f"  {project}: {len(findings)} categories")
    else:
        print("  No C2 patterns detected in any project")

    print("\n🔬 REMOTE ANALYSIS COMPLETED")

if __name__ == "__main__":
    main()
