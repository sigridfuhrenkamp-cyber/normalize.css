#!/usr/bin/env python3
"""
DEEP NORMALIZATION ANALYSIS
Comprehensive analysis of normalize.css and CSS normalization concepts
"""

import re
import os
import json
import hashlib
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set

class DeepNormalizationAnalyzer:
    def __init__(self):
        self.css_patterns = {
            'vendor_prefixes': r'-webkit-|-moz-|-ms-|-o-',
            'important_declarations': r'!\s*important',
            'universal_selectors': r'\*',
            'attribute_selectors': r'\[.*?\]',
            'pseudo_elements': r'::[a-zA-Z-]+',
            'pseudo_classes': r':[a-zA-Z-]+',
            'media_queries': r'@media[^{]*?\{',
            'keyframes': r'@keyframes[^{]*?\{',
            'font_faces': r'@font-face[^{]*?\{',
            'imports': r'@import[^;]+;',
            'charset': r'@charset[^;]+;',
            'supports': r'@supports[^{]*?\{',
            'calc_usage': r'calc\([^)]+\)',
            'var_usage': r'var\([^)]+\)',
            'url_usage': r'url\([^)]+\)',
            'data_urls': r'url\(data:[^)]+\)',
            'unicode_ranges': r'unicode-range:[^;]+;',
            'comments': r'/\*.*?\*/',
            'hack_patterns': [
                r'_.*?:',  # IE6 underscore hack
                r'\*.*?:',  # IE7 star hack
                r'/\*.*?\*/.*?\*/',  # Comment hack
                r'property:.*?ie',  # IE-specific
            ]
        }
        
        self.browser_specific_patterns = {
            'webkit': r'-webkit-|::webkit-',
            'mozilla': r'-moz-|::-moz-',
            'ms': r'-ms-|::-ms-',
            'legacy_ie': r'filter:|expression\(|behavior:',
            'edge': r'-ms-|@supports',
        }
        
        self.security_patterns = {
            'javascript_urls': r'javascript:',
            'data_urls': r'url\(data:text/html',
            'expression': r'expression\(',
            'binding': r'behavior:',
            'filter': r'filter:\s*progid:',
        }

    def analyze_css_file(self, filepath: str) -> Dict:
        """Deep analysis of a CSS file"""
        if not os.path.exists(filepath):
            return {"error": f"File {filepath} not found"}
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        analysis = {
            'file_info': self._get_file_info(filepath, content),
            'structural_analysis': self._analyze_structure(content),
            'browser_compatibility': self._analyze_browser_support(content),
            'security_analysis': self._analyze_security(content),
            'performance_analysis': self._analyze_performance(content),
            'normalization_coverage': self._analyze_normalization_coverage(content),
            'advanced_patterns': self._analyze_advanced_patterns(content),
            'potential_issues': self._identify_potential_issues(content),
            'css_metrics': self._calculate_css_metrics(content),
        }
        
        return analysis
    
    def _get_file_info(self, filepath: str, content: str) -> Dict:
        """Basic file information"""
        return {
            'path': filepath,
            'size_bytes': len(content.encode('utf-8')),
            'lines': len(content.splitlines()),
            'hash_md5': hashlib.md5(content.encode('utf-8')).hexdigest(),
            'encoding_detected': 'utf-8',
        }
    
    def _analyze_structure(self, content: str) -> Dict:
        """Analyze CSS structure"""
        # Remove comments for accurate counting
        clean_content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        selectors = re.findall(r'([^{}]+)\{', clean_content)
        declarations = re.findall(r'\{([^}]+)\}', clean_content)
        
        return {
            'total_selectors': len(selectors),
            'total_declarations': len(declarations),
            'selector_types': self._categorize_selectors(selectors),
            'property_frequency': self._count_properties(declarations),
            'value_frequency': self._count_values(declarations),
            'complexity_metrics': self._calculate_complexity(content),
        }
    
    def _categorize_selectors(self, selectors: List[str]) -> Dict[str, int]:
        """Categorize selectors by type"""
        categories = {
            'element': 0,
            'class': 0,
            'id': 0,
            'attribute': 0,
            'pseudo_class': 0,
            'pseudo_element': 0,
            'universal': 0,
            'combinator': 0,
        }
        
        for selector in selectors:
            selector = selector.strip()
            if '*' in selector:
                categories['universal'] += selector.count('*')
            if '.' in selector and not selector.startswith('.'):
                categories['class'] += len(re.findall(r'\.[a-zA-Z-]+', selector))
            if '#' in selector:
                categories['id'] += len(re.findall(r'#[a-zA-Z-]+', selector))
            if '[' in selector:
                categories['attribute'] += len(re.findall(r'\[.*?\]', selector))
            if ':' in selector and not selector.startswith('::'):
                categories['pseudo_class'] += len(re.findall(r':[a-zA-Z-]+', selector))
            if '::' in selector:
                categories['pseudo_element'] += len(re.findall(r'::[a-zA-Z-]+', selector))
            if re.match(r'^[a-zA-Z]+$', selector.split(',')[0].strip()):
                categories['element'] += 1
            if any(char in selector for char in ['>', '+', '~', ' ']):
                categories['combinator'] += 1
        
        return categories
    
    def _count_properties(self, declarations: List[str]) -> Counter:
        """Count property frequency"""
        properties = []
        for decl in declarations:
            props = re.findall(r'([^:;]+):', decl)
            properties.extend([p.strip() for p in props])
        return Counter(properties)
    
    def _count_values(self, declarations: List[str]) -> Counter:
        """Count value frequency"""
        values = []
        for decl in declarations:
            vals = re.findall(r':\s*([^:;]+)', decl)
            values.extend([v.strip() for v in vals])
        return Counter(values)
    
    def _calculate_complexity(self, content: str) -> Dict:
        """Calculate complexity metrics"""
        clean_content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        return {
            'selector_specificity_avg': self._calculate_avg_specificity(clean_content),
            'nesting_depth_max': self._calculate_max_nesting(content),
            'rule_count': len(re.findall(r'[^{}]+\{[^}]*\}', clean_content)),
            'vendor_prefix_count': len(re.findall(r'-[a-z]+-', content)),
            'comment_ratio': len(re.findall(r'/\*.*?\*/', content, flags=re.DOTALL)) / max(len(content.splitlines()), 1),
        }
    
    def _calculate_avg_specificity(self, content: str) -> float:
        """Calculate average selector specificity"""
        selectors = re.findall(r'([^{}]+)\{', content)
        specificities = []
        
        for selector in selectors:
            specificity = 0
            # IDs: 100 points each
            specificity += len(re.findall(r'#[a-zA-Z-]+', selector)) * 100
            # Classes/attributes/pseudo-classes: 10 points each
            specificity += len(re.findall(r'(\.[a-zA-Z-]+|\[.*?\]|:[a-zA-Z-]+)', selector)) * 10
            # Elements: 1 point each
            specificity += len(re.findall(r'[a-zA-Z-]+(?=[\s>+~:,[\]])', selector))
            
            specificities.append(specificity)
        
        return sum(specificities) / len(specificities) if specificities else 0
    
    def _calculate_max_nesting(self, content: str) -> int:
        """Calculate maximum nesting depth"""
        # Simplified nesting calculation
        max_depth = 0
        current_depth = 0
        
        for char in content:
            if char == '{':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == '}':
                current_depth -= 1
        
        return max_depth
    
    def _analyze_browser_support(self, content: str) -> Dict:
        """Analyze browser-specific code"""
        support = {}
        
        for browser, pattern in self.browser_specific_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            support[browser] = {
                'count': len(matches),
                'patterns': list(set(matches))[:10],  # Limit to 10 unique patterns
            }
        
        return support
    
    def _analyze_security(self, content: str) -> Dict:
        """Analyze security patterns"""
        security_issues = []
        
        for issue_type, pattern in self.security_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                security_issues.append({
                    'type': issue_type,
                    'count': len(matches),
                    'examples': matches[:3]
                })
        
        return {
            'issues_found': len(security_issues),
            'details': security_issues,
            'risk_level': self._assess_security_risk(security_issues)
        }
    
    def _assess_security_risk(self, issues: List) -> str:
        """Assess security risk level"""
        high_risk_patterns = ['javascript_urls', 'expression', 'binding']
        
        for issue in issues:
            if issue['type'] in high_risk_patterns:
                return 'HIGH'
        
        if len(issues) > 0:
            return 'MEDIUM'
        
        return 'LOW'
    
    def _analyze_performance(self, content: str) -> Dict:
        """Analyze performance implications"""
        return {
            'universal_selectors': len(re.findall(r'\*', content)),
            'expensive_selectors': len(re.findall(r'\*.*\*|\[.*\].*\[.*\]', content)),
            'vendor_prefixes': len(re.findall(r'-[a-z]+-', content)),
            'file_size_kb': len(content.encode('utf-8')) / 1024,
            'compression_potential': self._estimate_compression(content),
        }
    
    def _estimate_compression(self, content: str) -> float:
        """Estimate compression potential"""
        # Simple estimation based on whitespace and comment removal
        without_comments = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        without_whitespace = re.sub(r'\s+', ' ', without_comments).strip()
        
        original_size = len(content.encode('utf-8'))
        compressed_size = len(without_whitespace.encode('utf-8'))
        
        return ((original_size - compressed_size) / original_size) * 100
    
    def _analyze_normalization_coverage(self, content: str) -> Dict:
        """Analyze what CSS normalization aspects are covered"""
        normalization_aspects = {
            'box_model': ['box-sizing', 'margin', 'padding', 'width', 'height'],
            'typography': ['font-family', 'font-size', 'line-height', 'font-weight'],
            'display': ['display', 'visibility'],
            'positioning': ['position', 'top', 'left', 'right', 'bottom', 'z-index'],
            'backgrounds': ['background', 'background-color'],
            'borders': ['border', 'border-style', 'border-width'],
            'forms': ['input', 'button', 'select', 'textarea', 'fieldset'],
            'tables': ['table', 'tr', 'td', 'th'],
            'media': ['img', 'video', 'audio', 'canvas'],
        }
        
        coverage = {}
        clean_content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        for aspect, properties in normalization_aspects.items():
            found_properties = []
            for prop in properties:
                if prop in clean_content.lower():
                    found_properties.append(prop)
            
            coverage[aspect] = {
                'properties_found': found_properties,
                'coverage_percentage': (len(found_properties) / len(properties)) * 100
            }
        
        return coverage
    
    def _analyze_advanced_patterns(self, content: str) -> Dict:
        """Analyze advanced CSS patterns"""
        return {
            'css_variables': len(re.findall(r'var\([^)]+\)', content)),
            'calc_usage': len(re.findall(r'calc\([^)]+\)', content)),
            'custom_properties': len(re.findall(r'--[a-zA-Z-]+:', content)),
            'media_queries': len(re.findall(r'@media[^{]*?\{', content)),
            'supports_queries': len(re.findall(r'@supports[^{]*?\{', content)),
            'keyframes': len(re.findall(r'@keyframes', content)),
            'font_faces': len(re.findall(r'@font-face', content)),
        }
    
    def _identify_potential_issues(self, content: str) -> List[Dict]:
        """Identify potential issues and anti-patterns"""
        issues = []
        
        # Check for universal selector overuse
        universal_count = len(re.findall(r'\*', content))
        if universal_count > 10:
            issues.append({
                'type': 'performance',
                'severity': 'medium',
                'description': f'High usage of universal selector ({universal_count} times)',
                'recommendation': 'Consider more specific selectors'
            })
        
        # Check for !important usage
        important_count = len(re.findall(r'!\s*important', content))
        if important_count > 0:
            issues.append({
                'type': 'maintainability',
                'severity': 'medium',
                'description': f'Usage of !important ({important_count} times)',
                'recommendation': 'Avoid !important when possible'
            })
        
        # Check for vendor prefixes
        vendor_count = len(re.findall(r'-[a-z]+-', content))
        if vendor_count > 20:
            issues.append({
                'type': 'maintenance',
                'severity': 'low',
                'description': f'High number of vendor prefixes ({vendor_count})',
                'recommendation': 'Consider using autoprefixer'
            })
        
        # Check for browser-specific hacks
        hacks_found = []
        for hack_pattern in self.css_patterns['hack_patterns']:
            if re.search(hack_pattern, content, re.IGNORECASE):
                hacks_found.append(hack_pattern)
        
        if hacks_found:
            issues.append({
                'type': 'compatibility',
                'severity': 'medium',
                'description': f'Browser-specific hacks detected: {len(hacks_found)}',
                'recommendation': 'Consider modern alternatives'
            })
        
        return issues
    
    def _calculate_css_metrics(self, content: str) -> Dict:
        """Calculate various CSS metrics"""
        clean_content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        return {
            'total_rules': len(re.findall(r'[^{}]+\{[^}]*\}', clean_content)),
            'avg_declarations_per_rule': self._avg_declarations_per_rule(clean_content),
            'unique_properties': len(self._count_properties(re.findall(r'\{([^}]+)\}', clean_content))),
            'unique_selectors': len(set(re.findall(r'([^{}]+)\{', clean_content))),
            'css_efficiency_score': self._calculate_efficiency_score(content),
        }
    
    def _avg_declarations_per_rule(self, content: str) -> float:
        """Calculate average declarations per rule"""
        rules = re.findall(r'[^{}]+\{([^}]*)\}', content)
        if not rules:
            return 0
        
        total_declarations = sum(len(re.findall(r'[^:;]+:', rule)) for rule in rules)
        return total_declarations / len(rules)
    
    def _calculate_efficiency_score(self, content: str) -> float:
        """Calculate CSS efficiency score (0-100)"""
        score = 100.0
        
        # Deduct points for various anti-patterns
        universal_count = len(re.findall(r'\*', content))
        score -= min(universal_count * 2, 20)  # Max 20 point deduction
        
        important_count = len(re.findall(r'!\s*important', content))
        score -= min(important_count * 5, 15)  # Max 15 point deduction
        
        # Bonus points for good practices
        if re.search(r'/\*.*?normalize.*?\*/', content, re.IGNORECASE):
            score += 5  # Bonus for normalization comments
        
        return max(0, min(100, score))

def analyze_normalization_ecosystem():
    """Analyze the broader CSS normalization ecosystem"""
    analyzer = DeepNormalizationAnalyzer()
    
    # Analyze main normalize.css
    normalize_analysis = analyzer.analyze_css_file('normalize.css')
    
    # Compare with other CSS files if they exist
    css_files = ['css-reset.css', 'sanitize.css']
    comparisons = {}
    
    for css_file in css_files:
        if os.path.exists(css_file):
            comparisons[css_file] = analyzer.analyze_css_file(css_file)
    
    return {
        'normalize_css': normalize_analysis,
        'comparisons': comparisons,
        'ecosystem_analysis': analyze_normalization_trends()
    }

def analyze_normalization_trends():
    """Analyze CSS normalization trends and patterns"""
    return {
        'historical_evolution': [
            {
                'era': 'Pre-2012',
                'characteristics': ['Browser-specific resets', 'High selector specificity', 'Manual vendor prefixes'],
                'examples': ['Eric Meyer Reset', 'YUI Reset']
            },
            {
                'era': '2012-2016',
                'characteristics': ['Normalization over reset', 'Cross-browser consistency', 'Reduced specificity'],
                'examples': ['normalize.css v1-4']
            },
            {
                'era': '2016-2020',
                'characteristics': ['CSS custom properties', 'Modern browser features', 'Reduced file sizes'],
                'examples': ['normalize.css v5-7', 'CSS Reset alternatives']
            },
            {
                'era': '2020+',
                'characteristics': ['CSS Grid/Flexbox support', 'Container queries', 'Dark mode considerations'],
                'examples': ['normalize.css v8+', 'Modern CSS reset']
            }
        ],
        'current_best_practices': [
            'Use normalization instead of aggressive resets',
            'Target specific browser inconsistencies',
            'Maintain low selector specificity',
            'Include comprehensive testing',
            'Document browser-specific fixes',
            'Consider modern CSS features',
            'Optimize for performance and maintainability'
        ],
        'emerging_trends': [
            'CSS custom properties for theming',
            'Container query support',
            'CSS Houdini integration',
            'Progressive enhancement approaches',
            'Component-specific normalization'
        ]
    }

def main():
    """Main analysis function"""
    print("🔍 DEEP NORMALIZATION ANALYSIS")
    print("=" * 50)
    
    results = analyze_normalization_ecosystem()
    
    # Print normalize.css analysis
    print("\n📋 NORMALIZE.CSS ANALYSIS")
    print("-" * 30)
    
    normalize = results['normalize_css']
    if 'error' not in normalize:
        print(f"File size: {normalize['file_info']['size_bytes']} bytes")
        print(f"Lines: {normalize['file_info']['lines']}")
        print(f"Total selectors: {normalize['structural_analysis']['total_selectors']}")
        print(f"Total declarations: {normalize['structural_analysis']['total_declarations']}")
        print(f"Efficiency score: {normalize['css_metrics']['css_efficiency_score']:.1f}/100")
        
        print(f"\n🎯 NORMALIZATION COVERAGE")
        coverage = normalize['normalization_coverage']
        for aspect, data in coverage.items():
            print(f"  {aspect}: {data['coverage_percentage']:.1f}%")
        
        print(f"\n⚠️  POTENTIAL ISSUES")
        for issue in normalize['potential_issues']:
            print(f"  {issue['type']}: {issue['description']}")
        
        print(f"\n🔧 BROWSER SUPPORT")
        browser_support = normalize['browser_compatibility']
        for browser, data in browser_support.items():
            if data['count'] > 0:
                print(f"  {browser}: {data['count']} vendor-specific features")
    
    # Print comparisons
    if results['comparisons']:
        print("\n📊 COMPARISON WITH OTHER CSS LIBRARIES")
        print("-" * 40)
        
        for filename, analysis in results['comparisons'].items():
            if 'error' not in analysis:
                print(f"\n{filename.upper()}:")
                print(f"  Size: {analysis['file_info']['size_bytes']} bytes")
                print(f"  Selectors: {analysis['structural_analysis']['total_selectors']}")
                print(f"  Efficiency: {analysis['css_metrics']['css_efficiency_score']:.1f}/100")
    
    # Print ecosystem analysis
    print("\n🌍 NORMALIZATION ECOSYSTEM ANALYSIS")
    print("-" * 35)
    
    ecosystem = results['ecosystem_analysis']
    
    print("\n📈 HISTORICAL EVOLUTION:")
    for era in ecosystem['historical_evolution']:
        print(f"\n  {era['era']}:")
        for char in era['characteristics']:
            print(f"    • {char}")
    
    print("\n✅ CURRENT BEST PRACTICES:")
    for practice in ecosystem['current_best_practices']:
        print(f"  • {practice}")
    
    print("\n🚀 EMERGING TRENDS:")
    for trend in ecosystem['emerging_trends']:
        print(f"  • {trend}")
    
    # Save detailed results
    with open('deep_normalization_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: deep_normalization_results.json")

if __name__ == "__main__":
    main()
