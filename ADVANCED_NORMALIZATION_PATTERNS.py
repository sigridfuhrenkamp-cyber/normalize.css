#!/usr/bin/env python3
"""
ADVANCED NORMALIZATION PATTERNS ANALYSIS
Deep dive into CSS normalization patterns, browser-specific fixes, and emerging trends
"""

import re
import os
import json
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional

class AdvancedNormalizationAnalyzer:
    def __init__(self):
        self.browser_bugs = {
            'ios_orientation': {
                'pattern': r'-webkit-text-size-adjust',
                'description': 'Prevent iOS orientation change font scaling',
                'browsers': ['iOS Safari'],
                'impact': 'high'
            },
            'firefox_focus': {
                'pattern': r'-moz-focusring|::-moz-focus-inner',
                'description': 'Firefox focus ring restoration',
                'browsers': ['Firefox'],
                'impact': 'medium'
            },
            'ie_overflow': {
                'pattern': r'overflow:\s*visible',
                'description': 'IE 10+ overflow handling',
                'browsers': ['IE 10+', 'Edge'],
                'impact': 'medium'
            },
            'chrome_text_decoration': {
                'pattern': r'text-decoration:\s*underline.*dotted',
                'description': 'Chrome text decoration inheritance',
                'browsers': ['Chrome', 'Edge'],
                'impact': 'low'
            }
        }
        
        self.modern_css_features = {
            'css_variables': r'var\(--[a-zA-Z0-9-]+\)',
            'custom_properties': r'--[a-zA-Z0-9-]+:',
            'container_queries': r'@container',
            'css_layers': r'@layer',
            'cascade_layers': r'@layer',
            'scope_rules': r'@scope',
            'css_nesting': r'&[a-zA-Z-]',
            'math_functions': r'calc\(|min\(|max\(|clamp\(',
            'logical_properties': r'margin-inline|padding-block|inset-',
            'color_functions': r'hsl\(|hwb\(|lab\(|lch\(',
        }
        
        self.accessibility_patterns = {
            'reduced_motion': r'prefers-reduced-motion',
            'dark_mode': r'prefers-color-scheme:\s*dark',
            'high_contrast': r'prefers-contrast',
            'focus_visible': r':focus-visible',
            'forced_colors': r'forced-colors',
        }
        
        self.performance_patterns = {
            'expensive_selectors': r'\*.*\*|\[.*\].*\[.*\]|:not\([^)]+\)',
            'universal_selectors': r'\*',
            'attribute_selectors': r'\[.*?\]',
            'complex_pseudo_classes': r':not\(|:has\(|:where\(|:is\(',
            'deep_selectors': r'\s+\s+\s+',
        }

    def analyze_normalization_patterns(self, filepath: str) -> Dict:
        """Comprehensive analysis of normalization patterns"""
        if not os.path.exists(filepath):
            return {"error": f"File {filepath} not found"}
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        analysis = {
            'browser_bug_analysis': self._analyze_browser_bugs(content),
            'modern_css_integration': self._analyze_modern_css(content),
            'accessibility_considerations': self._analyze_accessibility(content),
            'performance_impact': self._analyze_performance_patterns(content),
            'normalization_strategy': self._analyze_normalization_strategy(content),
            'browser_specific_optimizations': self._analyze_browser_optimizations(content),
            'future_readiness': self._analyze_future_readiness(content),
            'code_quality_metrics': self._analyze_code_quality(content),
        }
        
        return analysis
    
    def _analyze_browser_bugs(self, content: str) -> Dict:
        """Analyze browser-specific bug fixes"""
        bug_fixes = {}
        
        for bug_name, bug_info in self.browser_bugs.items():
            matches = re.findall(bug_info['pattern'], content, re.IGNORECASE)
            bug_fixes[bug_name] = {
                'description': bug_info['description'],
                'browsers_affected': bug_info['browsers'],
                'impact_level': bug_info['impact'],
                'instances_found': len(matches),
                'code_snippets': matches[:3] if matches else [],
                'pattern_matches': bool(matches)
            }
        
        # Calculate overall browser compatibility score
        total_bugs = len(self.browser_bugs)
        addressed_bugs = sum(1 for fix in bug_fixes.values() if fix['instances_found'] > 0)
        compatibility_score = (addressed_bugs / total_bugs) * 100
        
        return {
            'bug_fixes': bug_fixes,
            'compatibility_score': compatibility_score,
            'total_bugs_addressed': addressed_bugs,
            'critical_fixes': len([f for f in bug_fixes.values() if f['impact_level'] == 'high' and f['instances_found'] > 0])
        }
    
    def _analyze_modern_css(self, content: str) -> Dict:
        """Analyze modern CSS feature integration"""
        modern_features = {}
        
        for feature_name, pattern in self.modern_css_features.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            modern_features[feature_name] = {
                'instances': len(matches),
                'examples': matches[:2] if matches else [],
                'adoption_level': self._assess_adoption_level(feature_name, len(matches))
            }
        
        # Calculate modernization score
        total_features = len(self.modern_css_features)
        adopted_features = sum(1 for f in modern_features.values() if f['instances'] > 0)
        modernization_score = (adopted_features / total_features) * 100
        
        return {
            'features': modern_features,
            'modernization_score': modernization_score,
            'adopted_features': adopted_features,
            'cutting_edge_features': len([f for f in modern_features.values() if f['adoption_level'] == 'cutting_edge'])
        }
    
    def _assess_adoption_level(self, feature: str, instances: int) -> str:
        """Assess CSS feature adoption level"""
        if instances == 0:
            return 'not_adopted'
        elif feature in ['css_variables', 'custom_properties', 'math_functions']:
            return 'widely_adopted'
        elif feature in ['container_queries', 'css_layers', 'scope_rules']:
            return 'cutting_edge'
        else:
            return 'emerging'
    
    def _analyze_accessibility(self, content: str) -> Dict:
        """Analyze accessibility considerations"""
        accessibility_features = {}
        
        for feature_name, pattern in self.accessibility_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            accessibility_features[feature_name] = {
                'instances': len(matches),
                'examples': matches[:2] if matches else [],
                'importance': self._assess_accessibility_importance(feature_name)
            }
        
        # Calculate accessibility score
        total_features = len(self.accessibility_patterns)
        implemented_features = sum(1 for f in accessibility_features.values() if f['instances'] > 0)
        accessibility_score = (implemented_features / total_features) * 100
        
        return {
            'features': accessibility_features,
            'accessibility_score': accessibility_score,
            'implemented_features': implemented_features,
            'critical_features': len([f for f in accessibility_features.values() if f['importance'] == 'critical' and f['instances'] > 0])
        }
    
    def _assess_accessibility_importance(self, feature: str) -> str:
        """Assess accessibility feature importance"""
        critical_features = ['reduced_motion', 'focus_visible']
        high_features = ['dark_mode', 'high_contrast']
        
        if feature in critical_features:
            return 'critical'
        elif feature in high_features:
            return 'high'
        else:
            return 'medium'
    
    def _analyze_performance_patterns(self, content: str) -> Dict:
        """Analyze performance-impacting patterns"""
        performance_issues = {}
        
        for pattern_name, pattern in self.performance_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            performance_issues[pattern_name] = {
                'instances': len(matches),
                'performance_impact': self._assess_performance_impact(pattern_name, len(matches)),
                'examples': matches[:3] if matches else []
            }
        
        # Calculate performance score
        performance_score = 100
        for issue in performance_issues.values():
            if issue['performance_impact'] == 'high':
                performance_score -= 20
            elif issue['performance_impact'] == 'medium':
                performance_score -= 10
            elif issue['performance_impact'] == 'low':
                performance_score -= 5
        
        performance_score = max(0, performance_score)
        
        return {
            'patterns': performance_issues,
            'performance_score': performance_score,
            'critical_issues': len([i for i in performance_issues.values() if i['performance_impact'] == 'high']),
            'optimization_opportunities': len([i for i in performance_issues.values() if i['instances'] > 0])
        }
    
    def _assess_performance_impact(self, pattern: str, instances: int) -> str:
        """Assess performance impact level"""
        high_impact_patterns = ['universal_selectors', 'expensive_selectors']
        medium_impact_patterns = ['complex_pseudo_classes', 'deep_selectors']
        
        if pattern in high_impact_patterns:
            if instances > 50:
                return 'high'
            elif instances > 10:
                return 'medium'
            else:
                return 'low'
        elif pattern in medium_impact_patterns:
            if instances > 20:
                return 'medium'
            else:
                return 'low'
        else:
            return 'low'
    
    def _analyze_normalization_strategy(self, content: str) -> Dict:
        """Analyze the overall normalization strategy"""
        # Remove comments for analysis
        clean_content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Analyze strategy patterns
        strategies = {
            'reset_approach': self._detect_reset_approach(clean_content),
            'targeted_fixes': self._detect_targeted_fixes(clean_content),
            'progressive_enhancement': self._detect_progressive_enhancement(clean_content),
            'browser_specificity': self._detect_browser_specificity(clean_content),
        }
        
        return {
            'strategies': strategies,
            'overall_approach': self._determine_overall_approach(strategies),
            'strategy_effectiveness': self._evaluate_strategy_effectiveness(content)
        }
    
    def _detect_reset_approach(self, content: str) -> Dict:
        """Detect reset vs normalization approach"""
        universal_selectors = len(re.findall(r'\*', content))
        margin_zero_declarations = len(re.findall(r'margin:\s*0', content))
        padding_zero_declarations = len(re.findall(r'padding:\s*0', content))
        
        if universal_selectors > 100:
            approach = 'aggressive_reset'
        elif universal_selectors > 20:
            approach = 'moderate_reset'
        else:
            approach = 'targeted_normalization'
        
        return {
            'approach': approach,
            'universal_selectors': universal_selectors,
            'zero_declarations': margin_zero_declarations + padding_zero_declarations,
            'aggressiveness': 'high' if approach == 'aggressive_reset' else 'medium' if approach == 'moderate_reset' else 'low'
        }
    
    def _detect_targeted_fixes(self, content: str) -> Dict:
        """Detect targeted browser fixes"""
        vendor_prefixes = len(re.findall(r'-[a-z]+-', content))
        browser_hacks = len(re.findall(r'/\*.*?hack.*?\*/', content, re.IGNORECASE))
        
        return {
            'vendor_prefixes': vendor_prefixes,
            'browser_hacks': browser_hacks,
            'targeted_approach': vendor_prefixes > 0 or browser_hacks > 0
        }
    
    def _detect_progressive_enhancement(self, content: str) -> Dict:
        """Detect progressive enhancement patterns"""
        feature_queries = len(re.findall(r'@supports|@media', content))
        fallback_patterns = len(re.findall(r'fallback|alternative', content, re.IGNORECASE))
        
        return {
            'feature_queries': feature_queries,
            'fallback_patterns': fallback_patterns,
            'progressive_enhancement': feature_queries > 0
        }
    
    def _detect_browser_specificity(self, content: str) -> Dict:
        """Detect browser-specific code patterns"""
        webkit_patterns = len(re.findall(r'-webkit-', content))
        mozilla_patterns = len(re.findall(r'-moz-', content))
        ms_patterns = len(re.findall(r'-ms-', content))
        
        return {
            'webkit_specific': webkit_patterns,
            'mozilla_specific': mozilla_patterns,
            'ms_specific': ms_patterns,
            'total_browser_specific': webkit_patterns + mozilla_patterns + ms_patterns
        }
    
    def _determine_overall_approach(self, strategies: Dict) -> str:
        """Determine the overall normalization approach"""
        reset_approach = strategies['reset_approach']['approach']
        targeted_fixes = strategies['targeted_fixes']['targeted_approach']
        progressive_enhancement = strategies['progressive_enhancement']['progressive_enhancement']
        
        if reset_approach == 'targeted_normalization' and targeted_fixes:
            return 'modern_normalization'
        elif reset_approach == 'moderate_reset' and targeted_fixes:
            return 'hybrid_approach'
        elif reset_approach == 'aggressive_reset':
            return 'traditional_reset'
        else:
            return 'minimal_normalization'
    
    def _evaluate_strategy_effectiveness(self, content: str) -> Dict:
        """Evaluate the effectiveness of the normalization strategy"""
        # Count different types of normalizations
        element_normalizations = len(re.findall(r'[a-z]+\s*\{[^}]*\}', content))
        form_normalizations = len(re.findall(r'(button|input|select|textarea)', content))
        typography_normalizations = len(re.findall(r'(font|line-height|text-)', content))
        
        return {
            'element_normalizations': element_normalizations,
            'form_normalizations': form_normalizations,
            'typography_normalizations': typography_normalizations,
            'comprehensive_coverage': element_normalizations > 20 and form_normalizations > 5
        }
    
    def _analyze_browser_optimizations(self, content: str) -> Dict:
        """Analyze browser-specific optimizations"""
        optimizations = {}
        
        # WebKit optimizations
        webkit_optimizations = {
            'text_size_adjust': r'-webkit-text-size-adjust',
            'appearance': r'-webkit-appearance',
            'inner_spin_button': r'-webkit-inner-spin-button',
            'outer_spin_button': r'-webkit-outer-spin-button',
            'search_decoration': r'-webkit-search-decoration',
            'file_upload_button': r'-webkit-file-upload-button',
        }
        
        # Mozilla optimizations
        mozilla_optimizations = {
            'focus_inner': r'::-moz-focus-inner',
            'focusring': r':-moz-focusring',
        }
        
        # Microsoft optimizations
        ms_optimizations = {
            'text_size_adjust': r'-ms-text-size-adjust',
        }
        
        for browser, opts in [('webkit', webkit_optimizations), ('mozilla', mozilla_optimizations), ('ms', ms_optimizations)]:
            optimizations[browser] = {}
            for opt_name, pattern in opts.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                optimizations[browser][opt_name] = {
                    'instances': len(matches),
                    'present': len(matches) > 0
                }
        
        return optimizations
    
    def _analyze_future_readiness(self, content: str) -> Dict:
        """Analyze future-readiness of the CSS"""
        future_features = {
            'css_variables_support': len(re.findall(r'var\(', content)) > 0,
            'container_queries_ready': len(re.findall(r'@container', content)) > 0,
            'css_layers_support': len(re.findall(r'@layer', content)) > 0,
            'modern_layout_support': len(re.findall(r'(grid|flexbox|flex)', content, re.IGNORECASE)) > 0,
            'logical_properties': len(re.findall(r'(margin-inline|padding-block|inset)', content)) > 0,
            'color_functions': len(re.findall(r'(hsl|hwb|lab|lch)\(', content)) > 0,
        }
        
        readiness_score = sum(future_features.values()) / len(future_features) * 100
        
        return {
            'future_features': future_features,
            'readiness_score': readiness_score,
            'cutting_edge_adoption': len([f for f, present in future_features.items() if present]) >= 3
        }
    
    def _analyze_code_quality(self, content: str) -> Dict:
        """Analyze code quality metrics"""
        # Comment analysis
        comments = re.findall(r'/\*(.*?)\*/', content, re.DOTALL)
        documented_rules = len([c for c in comments if any(word in c.lower() for word in ['correct', 'fix', 'prevent', 'remove'])])
        
        # Code organization
        sections = re.findall(r'/\*\s*([^*]+)\s*\*/', content)
        section_count = len(sections)
        
        # Consistency metrics
        property_consistency = self._check_property_consistency(content)
        
        return {
            'documentation_quality': {
                'total_comments': len(comments),
                'documented_rules': documented_rules,
                'documentation_ratio': documented_rules / max(len(re.findall(r'\{[^}]*\}', content)), 1)
            },
            'code_organization': {
                'sections': section_count,
                'structured_approach': section_count > 5
            },
            'consistency_metrics': property_consistency,
            'maintainability_score': self._calculate_maintainability_score(content)
        }
    
    def _check_property_consistency(self, content: str) -> Dict:
        """Check property naming and value consistency"""
        # Check for consistent property ordering
        rules = re.findall(r'\{([^}]+)\}', content)
        property_orders = []
        
        for rule in rules:
            properties = re.findall(r'([^:;]+):', rule)
            property_orders.append(properties)
        
        # Check for consistent naming conventions
        kebab_case_properties = len(re.findall(r'[a-z]+-[a-z-]+:', content))
        camel_case_properties = len(re.findall(r'[a-z][A-Z][a-zA-Z]*:', content))
        
        return {
            'kebab_case_usage': kebab_case_properties,
            'camel_case_usage': camel_case_properties,
            'naming_consistency': camel_case_properties == 0,  # Should be all kebab-case
            'property_ordering_consistency': len(set(tuple(order) for order in property_orders)) == 1
        }
    
    def _calculate_maintainability_score(self, content: str) -> int:
        """Calculate maintainability score (0-100)"""
        score = 100
        
        # Deduct for complexity
        universal_selectors = len(re.findall(r'\*', content))
        score -= min(universal_selectors // 10, 20)
        
        # Deduct for lack of documentation
        comments = re.findall(r'/\*.*?\*/', content, flags=re.DOTALL)
        if len(comments) < 10:
            score -= 10
        
        # Deduct for browser-specific code
        vendor_prefixes = len(re.findall(r'-[a-z]+-', content))
        score -= min(vendor_prefixes // 5, 15)
        
        return max(0, score)

def analyze_comprehensive_normalization():
    """Comprehensive normalization analysis"""
    analyzer = AdvancedNormalizationAnalyzer()
    
    print("🔬 ADVANCED NORMALIZATION PATTERNS ANALYSIS")
    print("=" * 60)
    
    # Analyze normalize.css
    if os.path.exists('normalize.css'):
        results = analyzer.analyze_normalization_patterns('normalize.css')
        
        print("\n🐛 BROWSER BUG FIXES ANALYSIS")
        print("-" * 35)
        bug_analysis = results['browser_bug_analysis']
        print(f"Compatibility Score: {bug_analysis['compatibility_score']:.1f}%")
        print(f"Bugs Addressed: {bug_analysis['total_bugs_addressed']}/{len(analyzer.browser_bugs)}")
        print(f"Critical Fixes: {bug_analysis['critical_fixes']}")
        
        for bug_name, bug_info in bug_analysis['bug_fixes'].items():
            if bug_info['instances_found'] > 0:
                print(f"  ✓ {bug_name}: {bug_info['description']} ({bug_info['instances_found']} instances)")
        
        print(f"\n🚀 MODERN CSS INTEGRATION")
        print("-" * 30)
        modern_analysis = results['modern_css_integration']
        print(f"Modernization Score: {modern_analysis['modernization_score']:.1f}%")
        print(f"Features Adopted: {modern_analysis['adopted_features']}/{len(analyzer.modern_css_features)}")
        print(f"Cutting Edge Features: {modern_analysis['cutting_edge_features']}")
        
        for feature_name, feature_info in modern_analysis['features'].items():
            if feature_info['instances'] > 0:
                print(f"  ✓ {feature_name}: {feature_info['instances']} instances ({feature_info['adoption_level']})")
        
        print(f"\n♿ ACCESSIBILITY CONSIDERATIONS")
        print("-" * 32)
        accessibility_analysis = results['accessibility_considerations']
        print(f"Accessibility Score: {accessibility_analysis['accessibility_score']:.1f}%")
        print(f"Features Implemented: {accessibility_analysis['implemented_features']}/{len(analyzer.accessibility_patterns)}")
        print(f"Critical Features: {accessibility_analysis['critical_features']}")
        
        for feature_name, feature_info in accessibility_analysis['features'].items():
            if feature_info['instances'] > 0:
                print(f"  ✓ {feature_name}: {feature_info['instances']} instances ({feature_info['importance']})")
        
        print(f"\n⚡ PERFORMANCE ANALYSIS")
        print("-" * 22)
        performance_analysis = results['performance_impact']
        print(f"Performance Score: {performance_analysis['performance_score']}/100")
        print(f"Critical Issues: {performance_analysis['critical_issues']}")
        print(f"Optimization Opportunities: {performance_analysis['optimization_opportunities']}")
        
        for pattern_name, pattern_info in performance_analysis['patterns'].items():
            if pattern_info['instances'] > 0:
                print(f"  ⚠ {pattern_name}: {pattern_info['instances']} instances ({pattern_info['performance_impact']} impact)")
        
        print(f"\n📋 NORMALIZATION STRATEGY")
        print("-" * 28)
        strategy_analysis = results['normalization_strategy']
        print(f"Overall Approach: {strategy_analysis['overall_approach']}")
        
        for strategy_name, strategy_info in strategy_analysis['strategies'].items():
            print(f"  {strategy_name}: {strategy_info}")
        
        print(f"\n🔧 BROWSER OPTIMIZATIONS")
        print("-" * 25)
        optimizations = results['browser_specific_optimizations']
        for browser, browser_opts in optimizations.items():
            present_opts = [name for name, info in browser_opts.items() if info['present']]
            if present_opts:
                print(f"  {browser.upper()}: {', '.join(present_opts)}")
        
        print(f"\n🔮 FUTURE READINESS")
        print("-" * 20)
        future_analysis = results['future_readiness']
        print(f"Readiness Score: {future_analysis['readiness_score']:.1f}%")
        print(f"Cutting Edge Adoption: {future_analysis['cutting_edge_adoption']}")
        
        for feature, present in future_analysis['future_features'].items():
            status = "✓" if present else "✗"
            print(f"  {status} {feature}")
        
        print(f"\n📊 CODE QUALITY METRICS")
        print("-" * 28)
        if 'code_quality' in results:
            quality_analysis = results['code_quality']
            print(f"Maintainability Score: {quality_analysis['maintainability_score']}/100")
            print(f"Documentation Quality: {quality_analysis['documentation_quality']['documented_rules']} documented rules")
            print(f"Code Organization: {quality_analysis['code_organization']['sections']} sections")
            print(f"Naming Consistency: {quality_analysis['consistency_metrics']['naming_consistency']}")
        else:
            print("Code quality analysis not available")
        
        # Save detailed results
        with open('advanced_normalization_patterns.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: advanced_normalization_patterns.json")
    
    else:
        print("❌ normalize.css not found in current directory")

if __name__ == "__main__":
    analyze_comprehensive_normalization()
