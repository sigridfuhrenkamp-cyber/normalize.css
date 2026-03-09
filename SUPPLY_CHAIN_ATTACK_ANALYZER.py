#!/usr/bin/env python3
"""
SUPPLY CHAIN ATTACK FORENSIC ANALYZER
Deep analysis of commit histories for supply chain attack evidence
"""

import os
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import subprocess
from typing import Dict, List, Any, Optional

class SupplyChainAttackAnalyzer:
    def __init__(self):
        self.repositories = {
            'normalize.css': 'normalize-css-upstream',
            'sanitize.css': 'sanitize-css-upstream'
        }
        
        self.attack_indicators = {
            'suspicious_patterns': [
                r'beacon', r'ping', r'pong', r'callback', r'control',
                r'c2', r'command', r'botnet', r'backdoor', r'payload',
                r'asterisk', r'start', r'end', r'position', r'coordinate'
            ],
            'timing_patterns': [
                r'same.day', r'concurrent', r'coordinated', r'synchronized'
            ],
            'author_patterns': [
                r'unknown', r'anonymous', r'system', r'bot', r'automated'
            ],
            'file_patterns': [
                r'\.tmp$', r'\.bak$', r'\.old$', r'\.cache$',
                r'test\.css', r'build\.css', r'compile\.css'
            ]
        }

    def analyze_supply_chain_attacks(self) -> Dict[str, Any]:
        """Comprehensive supply chain attack analysis"""
        print("🔍 INITIATING SUPPLY CHAIN ATTACK FORENSIC ANALYSIS...")
        
        results = {
            'repository_analysis': {},
            'commit_patterns': {},
            'author_analysis': {},
            'timing_analysis': {},
            'file_analysis': {},
            'cross_repo_correlation': {},
            'attack_evidence': {},
            'conclusion': {}
        }

        # Analyze each repository
        for repo_name, repo_path in self.repositories.items():
            print(f"🔍 Analyzing {repo_name} repository...")
            results['repository_analysis'][repo_name] = self.analyze_repository(repo_name, repo_path)

        # Cross-repository correlation
        results['cross_repo_correlation'] = self.correlate_repositories(results['repository_analysis'])
        
        # Attack evidence analysis
        results['attack_evidence'] = self.identify_attack_evidence(results)
        
        # Generate conclusion
        results['conclusion'] = self.generate_conclusion(results)

        return results

    def analyze_repository(self, name: str, path: str) -> Dict[str, Any]:
        """Analyze a single repository for attack patterns"""
        if not os.path.exists(path):
            return {'error': f'Repository not found: {path}'}

        # Get commit history
        commits = self.get_commit_history(path)
        
        analysis = {
            'name': name,
            'path': path,
            'total_commits': len(commits),
            'commits': commits,
            'suspicious_commits': [],
            'author_patterns': self.analyze_authors(commits),
            'timing_patterns': self.analyze_timing(commits),
            'message_patterns': self.analyze_commit_messages(commits),
            'file_patterns': self.analyze_file_changes(commits, path),
            'attack_indicators': self.detect_attack_indicators(commits)
        }

        return analysis

    def get_commit_history(self, repo_path: str) -> List[Dict[str, Any]]:
        """Get detailed commit history"""
        try:
            # Get commit details
            result = subprocess.run([
                'git', 'log', '--pretty=format:%H|%ae|%ad|%s',
                '--date=iso', '--name-only', '--numstat'
            ], cwd=repo_path, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                return []

            lines = result.stdout.strip().split('\n')
            commits = []
            current_commit = {}
            
            for line in lines:
                if '|' in line and len(line.split('|')) == 4:
                    # New commit
                    if current_commit:
                        commits.append(current_commit)
                    
                    parts = line.split('|')
                    current_commit = {
                        'hash': parts[0],
                        'author': parts[1],
                        'date': parts[2],
                        'message': parts[3],
                        'files': []
                    }
                elif line.startswith('\t'):
                    # File change
                    if 'files' in current_commit:
                        current_commit['files'].append(line.strip())
                elif line and '\t' not in line and not line.startswith(' '):
                    # File change line (additions/deletions)
                    if 'files' in current_commit and current_commit['files']:
                        current_commit['files'][-1] += ' ' + line

            # Add last commit
            if current_commit:
                commits.append(current_commit)

            return commits

        except Exception as e:
            print(f"Error getting commit history: {e}")
            return []

    def analyze_authors(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze author patterns"""
        authors = [commit['author'] for commit in commits]
        email_domains = []
        
        for email in authors:
            if '@' in email:
                domain = email.split('@')[1]
                email_domains.append(domain)

        return {
            'total_authors': len(set(authors)),
            'author_frequency': Counter(authors),
            'email_domains': Counter(email_domains),
            'suspicious_authors': [author for author in set(authors) 
                                 if any(pattern in author.lower() for pattern in 
                                      ['bot', 'system', 'automated', 'unknown', 'anonymous'])]
        }

    def analyze_timing(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze timing patterns"""
        dates = []
        for commit in commits:
            try:
                date_str = commit['date'].split()[0]  # Get date part
                dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
            except:
                continue

        if not dates:
            return {'error': 'No valid dates found'}

        # Analyze patterns
        date_frequency = Counter([date.strftime('%Y-%m-%d') for date in dates])
        hour_frequency = Counter([date.hour for date in dates])
        
        # Look for suspicious patterns
        same_day_commits = [date for date, count in date_frequency.items() if count > 5]
        unusual_hours = [hour for hour, count in hour_frequency.items() if count > 10]

        return {
            'date_range': f"{min(dates).date()} to {max(dates).date()}",
            'total_days': len(set([date.date() for date in dates])),
            'same_day_commits': same_day_commits,
            'unusual_hours': unusual_hours,
            'date_frequency': dict(date_frequency),
            'hour_frequency': dict(hour_frequency)
        }

    def analyze_commit_messages(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze commit message patterns"""
        messages = [commit['message'] for commit in commits]
        
        suspicious_messages = []
        for message in messages:
            for pattern in self.attack_indicators['suspicious_patterns']:
                if re.search(pattern, message, re.IGNORECASE):
                    suspicious_messages.append({
                        'message': message,
                        'pattern': pattern,
                        'risk': 'HIGH'
                    })

        return {
            'total_messages': len(messages),
            'suspicious_messages': suspicious_messages,
            'message_length_stats': {
                'avg_length': sum(len(m) for m in messages) / len(messages),
                'max_length': max(len(m) for m in messages),
                'min_length': min(len(m) for m in messages)
            }
        }

    def analyze_file_changes(self, commits: List[Dict[str, Any]], repo_path: str) -> Dict[str, Any]:
        """Analyze file change patterns"""
        all_files = []
        suspicious_files = []
        
        for commit in commits:
            for file_change in commit.get('files', []):
                if file_change:
                    parts = file_change.split()
                    if len(parts) >= 2:
                        filename = parts[-1]
                        all_files.append(filename)
                        
                        # Check for suspicious file patterns
                        for pattern in self.attack_indicators['file_patterns']:
                            if re.search(pattern, filename):
                                suspicious_files.append({
                                    'file': filename,
                                    'pattern': pattern,
                                    'commit': commit['hash']
                                })

        return {
            'total_files_changed': len(all_files),
            'unique_files': len(set(all_files)),
            'file_frequency': Counter(all_files),
            'suspicious_files': suspicious_files
        }

    def detect_attack_indicators(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect specific attack indicators"""
        indicators = {
            'asterisk_commits': [],
            'coordinate_commits': [],
            'timing_anomalies': [],
            'author_anomalies': [],
            'message_anomalies': []
        }

        for commit in commits:
            message = commit['message'].lower()
            
            # Asterisk positioning indicators
            if any(word in message for word in ['asterisk', 'position', 'coordinate']):
                indicators['asterisk_commits'].append({
                    'hash': commit['hash'],
                    'message': commit['message'],
                    'date': commit['date']
                })

            # Coordinate system indicators
            if any(word in message for word in ['coordinate', 'position', 'matrix', 'grid']):
                indicators['coordinate_commits'].append({
                    'hash': commit['hash'],
                    'message': commit['message'],
                    'date': commit['date']
                })

        return indicators

    def correlate_repositories(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Correlate findings across repositories"""
        correlation = {
            'same_authors': set(),
            'same_dates': {},
            'similar_patterns': {},
            'coordinated_attacks': []
        }

        # Get all authors and dates
        all_authors = {}
        all_dates = defaultdict(list)
        
        for repo_name, analysis in repo_analysis.items():
            if 'error' not in analysis:
                # Authors
                authors = analysis['author_patterns']['author_frequency']
                for author, count in authors.items():
                    if author not in all_authors:
                        all_authors[author] = {}
                    all_authors[author][repo_name] = count
                
                # Dates
                dates = analysis['timing_patterns'].get('date_frequency', {})
                for date, count in dates.items():
                    all_dates[date].append({
                        'repo': repo_name,
                        'count': count
                    })

        # Find overlapping authors
        for author, repos in all_authors.items():
            if len(repos) > 1:
                correlation['same_authors'].add(author)

        # Find same-day commits
        for date, repos in all_dates.items():
            if len(repos) > 1:
                correlation['same_dates'][date] = repos

        # Look for coordinated attacks
        for date, repos in correlation['same_dates'].items():
            if len(repos) >= 2:
                total_commits = sum(repo['count'] for repo in repos)
                if total_commits > 5:  # Suspicious activity threshold
                    correlation['coordinated_attacks'].append({
                        'date': date,
                        'repositories': repos,
                        'total_commits': total_commits
                    })

        correlation['same_authors'] = list(correlation['same_authors'])

        return correlation

    def identify_attack_evidence(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Identify conclusive attack evidence"""
        evidence = {
            'high_risk_indicators': [],
            'medium_risk_indicators': [],
            'low_risk_indicators': [],
            'attack_vectors': [],
            'compromise_assessment': 'UNKNOWN'
        }

        repo_analysis = results.get('repository_analysis', {})
        correlation = results.get('cross_repo_correlation', {})

        # High risk indicators
        for repo_name, analysis in repo_analysis.items():
            if 'error' not in analysis:
                # Suspicious commits
                suspicious = analysis.get('message_patterns', {}).get('suspicious_messages', [])
                if suspicious:
                    evidence['high_risk_indicators'].append({
                        'repo': repo_name,
                        'type': 'suspicious_commit_messages',
                        'count': len(suspicious),
                        'examples': suspicious[:3]
                    })

                # Attack indicators
                indicators = analysis.get('attack_indicators', {})
                if indicators.get('asterisk_commits'):
                    evidence['high_risk_indicators'].append({
                        'repo': repo_name,
                        'type': 'asterisk_positioning_commits',
                        'count': len(indicators['asterisk_commits']),
                        'examples': indicators['asterisk_commits'][:3]
                    })

        # Coordinated attacks
        coordinated = correlation.get('coordinated_attacks', [])
        if coordinated:
            evidence['high_risk_indicators'].append({
                'type': 'coordinated_repository_attacks',
                'count': len(coordinated),
                'examples': coordinated[:3]
            })

        # Determine compromise assessment
        high_risk_count = len(evidence['high_risk_indicators'])
        if high_risk_count >= 3:
            evidence['compromise_assessment'] = 'HIGH'
        elif high_risk_count >= 1:
            evidence['compromise_assessment'] = 'MEDIUM'
        else:
            evidence['compromise_assessment'] = 'LOW'

        return evidence

    def generate_conclusion(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final conclusion"""
        evidence = results.get('attack_evidence', {})
        correlation = results.get('cross_repo_correlation', {})
        
        conclusion = {
            'overall_risk': evidence.get('compromise_assessment', 'UNKNOWN'),
            'attack_confirmed': False,
            'attack_vectors': [],
            'recommendations': [],
            'evidence_strength': 'WEAK'
        }

        # Check for conclusive evidence
        high_risk = evidence.get('high_risk_indicators', [])
        coordinated = correlation.get('coordinated_attacks', [])

        if len(high_risk) >= 2 or len(coordinated) >= 1:
            conclusion['attack_confirmed'] = True
            conclusion['evidence_strength'] = 'STRONG'
            conclusion['attack_vectors'] = [
                'Coordinated supply chain compromise',
                'Asterisk positioning attacks',
                'Cross-repository coordination'
            ]
            conclusion['recommendations'] = [
                'CRITICAL: Immediate investigation required',
                'Audit all affected repositories',
                'Implement supply chain security measures',
                'Monitor for additional coordinated attacks'
            ]
        elif len(high_risk) >= 1:
            conclusion['evidence_strength'] = 'MODERATE'
            conclusion['recommendations'] = [
                'Monitor suspicious activity',
                'Review commit history for patterns',
                'Implement additional security checks'
            ]
        else:
            conclusion['recommendations'] = [
                'Continue monitoring',
                'Maintain standard security practices'
            ]

        return conclusion

def main():
    """Main analysis function"""
    print("🔍 SUPPLY CHAIN ATTACK FORENSIC ANALYSIS")
    print("=" * 60)

    analyzer = SupplyChainAttackAnalyzer()
    results = analyzer.analyze_supply_chain_attacks()

    # Save results
    with open('SUPPLY_CHAIN_ATTACK_ANALYSIS.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print("✅ ANALYSIS COMPLETE")
    print(f"📊 Results saved to: SUPPLY_CHAIN_ATTACK_ANALYSIS.json")

    # Print key findings
    conclusion = results.get('conclusion', {})
    print(f"\n🎯 CONCLUSION:")
    print(f"  Overall Risk: {conclusion.get('overall_risk', 'UNKNOWN')}")
    print(f"  Attack Confirmed: {conclusion.get('attack_confirmed', False)}")
    print(f"  Evidence Strength: {conclusion.get('evidence_strength', 'UNKNOWN')}")

    evidence = results.get('attack_evidence', {})
    high_risk = evidence.get('high_risk_indicators', [])
    print(f"\n🚨 HIGH RISK INDICATORS: {len(high_risk)}")

    correlation = results.get('cross_repo_correlation', {})
    coordinated = correlation.get('coordinated_attacks', [])
    print(f"🔗 COORDINATED ATTACKS: {len(coordinated)}")

    print("\n🔬 SUPPLY CHAIN FORENSIC ANALYSIS COMPLETED")

if __name__ == "__main__":
    main()
