#!/usr/bin/env python3
"""
CSS ECOSYSTEM DEEP INVESTIGATION ANALYZER
Comprehensive analysis of all upstream related projects in CSS normalization ecosystem
"""

import os
import json
import re
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional

class CSSEcosystemDeepInvestigator:
    def __init__(self):
        # Comprehensive list of CSS normalization ecosystem projects
        self.css_ecosystem_projects = {
            # Core normalization libraries
            'normalize.css': {
                'url': 'https://github.com/necolas/normalize.css.git',
                'category': 'core_normalization',
                'description': 'Modern, HTML5-ready alternative to CSS resets'
            },
            'sanitize.css': {
                'url': 'https://github.com/csstools/sanitize.css.git',
                'category': 'core_normalization', 
                'description': 'CSS normalization and opinionated reset'
            },
            'modern-normalize': {
                'url': 'https://github.com/sindresorhus/modern-normalize.git',
                'category': 'core_normalization',
                'description': 'Modern alternative to CSS resets'
            },
            'ress': {
                'url': 'https://github.com/filipelinhares/ress.git',
                'category': 'core_normalization',
                'description': 'Modern CSS reset'
            },
            
            # CSS reset alternatives
            'css-reset': {
                'url': 'https://github.com/twbs/css-reset.git',
                'category': 'css_reset',
                'description': 'CSS reset from Bootstrap team'
            },
            'reset-css': {
                'url': 'https://github.com/eric-meyers-reset-css.git',
                'category': 'css_reset',
                'description': 'Eric Meyer\'s CSS Reset'
            },
            'meyer-reset': {
                'url': 'https://github.com/h5bp/html5-boilerplate.git',
                'category': 'css_reset',
                'description': 'HTML5 Boilerplate reset styles'
            },
            
            # PostCSS normalization
            'postcss-normalize': {
                'url': 'https://github.com/postcss/postcss-normalize.git',
                'category': 'postcss_tools',
                'description': 'PostCSS plugin for normalize.css'
            },
            'postcss-reset': {
                'url': 'https://github.com/jonathantneal/postcss-reset.git',
                'category': 'postcss_tools',
                'description': 'PostCSS plugin for CSS reset'
            },
            'cssnano': {
                'url': 'https://github.com/cssnano/cssnano.git',
                'category': 'postcss_tools',
                'description': 'CSS minification and optimization'
            },
            
            # Build tools and bundlers
            'autoprefixer': {
                'url': 'https://github.com/postcss/autoprefixer.git',
                'category': 'build_tools',
                'description': 'PostCSS plugin to parse CSS and add vendor prefixes'
            },
            'postcss': {
                'url': 'https://github.com/postcss/postcss.git',
                'category': 'build_tools',
                'description': 'Tool for transforming CSS with JavaScript'
            },
            
            # Browser compatibility
            'browserslist': {
                'url': 'https://github.com/browserslist/browserslist.git',
                'category': 'browser_compatibility',
                'description': 'Share target browsers between different front-end tools'
            },
            'caniuse': {
                'url': 'https://github.com/Fyrd/caniuse.git',
                'category': 'browser_compatibility',
                'description': 'Browser support tables for modern web technologies'
            },
            
            # CSS frameworks and utilities
            'tailwindcss': {
                'url': 'https://github.com/tailwindlabs/tailwindcss.git',
                'category': 'css_frameworks',
                'description': 'Utility-first CSS framework'
            },
            'bootstrap': {
                'url': 'https://github.com/twbs/bootstrap.git',
                'category': 'css_frameworks',
                'description': 'The most popular HTML, CSS, and JS framework'
            },
            'foundation': {
                'url': 'https://github.com/foundation/foundation-sites.git',
                'category': 'css_frameworks',
                'description': 'The most advanced responsive front-end framework'
            },
            
            # CSS preprocessing tools
            'sass': {
                'url': 'https://github.com/sass/dart-sass.git',
                'category': 'preprocessing',
                'description': 'Dart Sass is the primary implementation of Sass'
            },
            'less': {
                'url': 'https://github.com/less/less.js.git',
                'category': 'preprocessing',
                'description': 'Leaner CSS, sometimes called dynamic CSS'
            },
            'stylus': {
                'url': 'https://github.com/stylus/stylus.git',
                'category': 'preprocessing',
                'description': 'Expressive, robust, feature-rich CSS language built for Node.js'
            }
        }

        # Enhanced attack indicators for deep investigation
        self.attack_indicators = {
            'c2_patterns': [
                r'beacon', r'ping', r'pong', r'heartbeat', r'callback', r'control',
                r'c2', r'command', r'botnet', r'backdoor', r'payload', r'zombie',
                r'asterisk', r'start', r'end', r'position', r'coordinate', r'matrix',
                r'grid', r'anchor', r'sync', r'trigger', r'activate', r'deactivate'
            ],
            'timing_patterns': [
                r'same.day', r'concurrent', r'coordinated', r'synchronized',
                r'simultaneous', r'parallel', r'together', r'unison'
            ],
            'author_patterns': [
                r'unknown', r'anonymous', r'system', r'bot', r'automated',
                r'ghost', r'shadow', r'phantom', r'nobody', r'contributor'
            ],
            'file_patterns': [
                r'\.tmp$', r'\.bak$', r'\.old$', r'\.cache$', r'\.hidden$',
                r'test\.css', r'build\.css', r'compile\.css', r'payload\.css',
                r'c2\.css', r'beacon\.css', r'command\.css'
            ],
            'suspicious_words': [
                r'exploit', r'vulnerability', r'backdoor', r'trojan', r'malware',
                r'weapon', r'attack', r'breach', r'compromise', r'injection'
            ]
        }

    def investigate_ecosystem(self) -> Dict[str, Any]:
        """Comprehensive ecosystem investigation"""
        print("🔍 INITIATING COMPREHENSIVE CSS ECOSYSTEM DEEP INVESTIGATION...")
        
        results = {
            'ecosystem_overview': {},
            'project_analysis': {},
            'cross_project_correlation': {},
            'suspicious_activity': {},
            'attack_evidence': {},
            'ecosystem_health': {},
            'conclusion': {}
        }

        # Clone and analyze all projects
        print("🔍 Cloning and analyzing all CSS ecosystem projects...")
        results['project_analysis'] = self.analyze_all_projects()

        # Cross-project correlation analysis
        print("🔍 Performing cross-project correlation analysis...")
        results['cross_project_correlation'] = self.correlate_all_projects(results['project_analysis'])

        # Suspicious activity detection
        print("🔍 Detecting suspicious activity patterns...")
        results['suspicious_activity'] = self.detect_suspicious_activity(results)

        # Attack evidence analysis
        print("🔍 Analyzing attack evidence...")
        results['attack_evidence'] = self.analyze_attack_evidence(results)

        # Ecosystem health assessment
        print("🔍 Assessing ecosystem health...")
        results['ecosystem_health'] = self.assess_ecosystem_health(results)

        # Generate conclusion
        results['conclusion'] = self.generate_ecosystem_conclusion(results)

        return results

    def analyze_all_projects(self) -> Dict[str, Any]:
        """Analyze all projects in the CSS ecosystem"""
        analysis = {}
        
        for project_name, project_info in self.css_ecosystem_projects.items():
            print(f"🔍 Analyzing {project_name}...")
            
            try:
                # Clone repository
                repo_path = self.clone_repository(project_name, project_info['url'])
                if repo_path:
                    # Analyze repository
                    project_analysis = self.analyze_repository(project_name, repo_path, project_info)
                    analysis[project_name] = project_analysis
                else:
                    analysis[project_name] = {'error': f'Failed to clone {project_name}'}
                    
            except Exception as e:
                analysis[project_name] = {'error': str(e)}

        return analysis

    def clone_repository(self, name: str, url: str) -> Optional[str]:
        """Clone a repository"""
        repo_path = f"{name}-upstream"
        
        try:
            # Remove existing directory if exists
            if os.path.exists(repo_path):
                import shutil
                shutil.rmtree(repo_path)
            
            # Clone repository
            result = subprocess.run([
                'git', 'clone', url, repo_path
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return repo_path
            else:
                return None
                
        except Exception as e:
            print(f"Error cloning {name}: {e}")
            return None

    def analyze_repository(self, name: str, path: str, info: Dict) -> Dict[str, Any]:
        """Analyze a single repository"""
        if not os.path.exists(path):
            return {'error': f'Repository not found: {path}'}

        # Get commit history
        commits = self.get_commit_history(path)
        
        analysis = {
            'project_info': info,
            'name': name,
            'path': path,
            'total_commits': len(commits),
            'commits': commits,
            'author_analysis': self.analyze_authors(commits),
            'timing_analysis': self.analyze_timing(commits),
            'message_analysis': self.analyze_commit_messages(commits),
            'file_analysis': self.analyze_file_changes(commits, path),
            'attack_indicators': self.detect_attack_indicators(commits),
            'suspicious_patterns': self.detect_suspicious_patterns(commits),
            'security_assessment': self.assess_repository_security(commits)
        }

        return analysis

    def get_commit_history(self, repo_path: str) -> List[Dict[str, Any]]:
        """Get detailed commit history"""
        try:
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
                    if 'files' in current_commit:
                        current_commit['files'].append(line.strip())
                elif line and '\t' not in line and not line.startswith(' '):
                    if 'files' in current_commit and current_commit['files']:
                        current_commit['files'][-1] += ' ' + line

            if current_commit:
                commits.append(current_commit)

            return commits

        except Exception as e:
            return []

    def analyze_authors(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze author patterns"""
        authors = [commit['author'] for commit in commits]
        email_domains = []
        
        for email in authors:
            if '@' in email:
                domain = email.split('@')[1]
                email_domains.append(domain)

        suspicious_authors = []
        for author in set(authors):
            for pattern in self.attack_indicators['author_patterns']:
                if re.search(pattern, author, re.IGNORECASE):
                    suspicious_authors.append(author)
                    break

        return {
            'total_authors': len(set(authors)),
            'author_frequency': Counter(authors),
            'email_domains': Counter(email_domains),
            'suspicious_authors': suspicious_authors,
            'author_anomalies': self.detect_author_anomalies(authors)
        }

    def detect_author_anomalies(self, authors: List[str]) -> List[Dict[str, Any]]:
        """Detect author anomalies"""
        anomalies = []
        
        # Check for single-author dominance
        author_counts = Counter(authors)
        if len(author_counts) > 0:
            top_author = author_counts.most_common(1)[0]
            if top_author[1] > len(authors) * 0.8:  # 80% of commits
                anomalies.append({
                    'type': 'author_dominance',
                    'author': top_author[0],
                    'percentage': top_author[1] / len(authors) * 100
                })
        
        return anomalies

    def analyze_timing(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze timing patterns"""
        dates = []
        for commit in commits:
            try:
                date_str = commit['date'].split()[0]
                dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
            except:
                continue

        if not dates:
            return {'error': 'No valid dates found'}

        date_frequency = Counter([date.strftime('%Y-%m-%d') for date in dates])
        hour_frequency = Counter([date.hour for date in dates])
        weekday_frequency = Counter([date.weekday() for date in dates])
        
        # Look for suspicious patterns
        same_day_commits = [date for date, count in date_frequency.items() if count > 10]
        unusual_hours = [hour for hour, count in hour_frequency.items() if count > 20]
        weekend_activity = [day for day, count in weekday_frequency.items() if day >= 5 and count > 5]

        return {
            'date_range': f"{min(dates).date()} to {max(dates).date()}",
            'total_days': len(set([date.date() for date in dates])),
            'same_day_commits': same_day_commits,
            'unusual_hours': unusual_hours,
            'weekend_activity': weekend_activity,
            'date_frequency': dict(date_frequency),
            'hour_frequency': dict(hour_frequency),
            'weekday_frequency': dict(weekday_frequency),
            'timing_anomalies': self.detect_timing_anomalies(dates)
        }

    def detect_timing_anomalies(self, dates: List[datetime]) -> List[Dict[str, Any]]:
        """Detect timing anomalies"""
        anomalies = []
        
        # Check for burst activity
        date_counts = Counter([date.date() for date in dates])
        for date, count in date_counts.items():
            if count > 20:  # More than 20 commits in a day
                anomalies.append({
                    'type': 'burst_activity',
                    'date': str(date),
                    'commits': count
                })
        
        return anomalies

    def analyze_commit_messages(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze commit message patterns"""
        messages = [commit['message'] for commit in commits]
        
        suspicious_messages = []
        for i, message in enumerate(messages):
            message_lower = message.lower()
            
            # Check all attack indicator patterns
            for category, patterns in self.attack_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, message_lower):
                        suspicious_messages.append({
                            'index': i,
                            'message': message,
                            'pattern': pattern,
                            'category': category,
                            'risk': 'HIGH' if category == 'c2_patterns' else 'MEDIUM'
                        })
                        break

        return {
            'total_messages': len(messages),
            'suspicious_messages': suspicious_messages,
            'message_length_stats': {
                'avg_length': sum(len(m) for m in messages) / len(messages),
                'max_length': max(len(m) for m in messages),
                'min_length': min(len(m) for m in messages)
            },
            'message_anomalies': self.detect_message_anomalies(messages)
        }

    def detect_message_anomalies(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Detect message anomalies"""
        anomalies = []
        
        # Check for very short messages (potential stealth)
        short_messages = [msg for msg in messages if len(msg.strip()) < 10]
        if len(short_messages) > len(messages) * 0.3:  # 30% short messages
            anomalies.append({
                'type': 'excessive_short_messages',
                'count': len(short_messages),
                'percentage': len(short_messages) / len(messages) * 100
            })
        
        return anomalies

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
            'suspicious_files': suspicious_files,
            'file_anomalies': self.detect_file_anomalies(all_files)
        }

    def detect_file_anomalies(self, files: List[str]) -> List[Dict[str, Any]]:
        """Detect file anomalies"""
        anomalies = []
        
        # Check for excessive file changes
        file_counts = Counter(files)
        if len(file_counts) > 0:
            top_file = file_counts.most_common(1)[0]
            if top_file[1] > len(files) * 0.5:  # 50% of changes to one file
                anomalies.append({
                    'type': 'file_dominance',
                    'file': top_file[0],
                    'percentage': top_file[1] / len(files) * 100
                })
        
        return anomalies

    def detect_attack_indicators(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect specific attack indicators"""
        indicators = {
            'c2_commits': [],
            'coordinate_commits': [],
            'timing_commits': [],
            'suspicious_author_commits': [],
            'attack_vectors': []
        }

        for commit in commits:
            message = commit['message'].lower()
            
            # C2 patterns
            for pattern in self.attack_indicators['c2_patterns']:
                if re.search(pattern, message):
                    indicators['c2_commits'].append({
                        'hash': commit['hash'],
                        'message': commit['message'],
                        'date': commit['date'],
                        'pattern': pattern
                    })

            # Coordinate patterns
            if any(word in message for word in ['coordinate', 'position', 'matrix', 'grid']):
                indicators['coordinate_commits'].append({
                    'hash': commit['hash'],
                    'message': commit['message'],
                    'date': commit['date']
                })

            # Timing patterns
            if any(word in message for word in ['timing', 'schedule', 'sync', 'concurrent']):
                indicators['timing_commits'].append({
                    'hash': commit['hash'],
                    'message': commit['message'],
                    'date': commit['date']
                })

            # Suspicious authors
            for pattern in self.attack_indicators['author_patterns']:
                if re.search(pattern, commit['author'], re.IGNORECASE):
                    indicators['suspicious_author_commits'].append({
                        'hash': commit['hash'],
                        'author': commit['author'],
                        'message': commit['message'],
                        'date': commit['date']
                    })

        return indicators

    def detect_suspicious_patterns(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect suspicious patterns"""
        patterns = {
            'burst_commits': [],
            'unusual_timing': [],
            'coordinated_patterns': [],
            'stealth_patterns': []
        }

        # Detect burst commits (many commits in short time)
        if len(commits) > 0:
            dates = [datetime.strptime(commit['date'].split()[0], '%Y-%m-%d') for commit in commits]
            date_counts = Counter([date.date() for date in dates])
            
            for date, count in date_counts.items():
                if count > 15:  # More than 15 commits in a day
                    patterns['burst_commits'].append({
                        'date': str(date),
                        'count': count,
                        'severity': 'HIGH' if count > 30 else 'MEDIUM'
                    })

        return patterns

    def assess_repository_security(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess repository security"""
        risk_factors = []
        risk_score = 0

        # Check for C2 patterns
        c2_count = 0
        for commit in commits:
            message = commit['message'].lower()
            for pattern in self.attack_indicators['c2_patterns']:
                if re.search(pattern, message):
                    c2_count += 1
                    break

        if c2_count > 0:
            risk_factors.append(f"c2_patterns_found_{c2_count}")
            risk_score += c2_count * 10

        # Check for suspicious authors
        suspicious_authors = 0
        for commit in commits:
            for pattern in self.attack_indicators['author_patterns']:
                if re.search(pattern, commit['author'], re.IGNORECASE):
                    suspicious_authors += 1
                    break

        if suspicious_authors > 0:
            risk_factors.append(f"suspicious_authors_{suspicious_authors}")
            risk_score += suspicious_authors * 5

        # Determine risk level
        if risk_score >= 50:
            risk_level = 'CRITICAL'
        elif risk_score >= 30:
            risk_level = 'HIGH'
        elif risk_score >= 15:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'c2_patterns_found': c2_count,
            'suspicious_authors': suspicious_authors,
            'total_commits_analyzed': len(commits)
        }

    def correlate_all_projects(self, project_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Correlate findings across all projects"""
        correlation = {
            'same_authors': set(),
            'same_dates': {},
            'coordinated_attacks': [],
            'cross_project_patterns': {},
            'ecosystem_suspicious_activity': {}
        }

        # Get all authors and dates
        all_authors = {}
        all_dates = defaultdict(list)
        
        for project_name, analysis in project_analysis.items():
            if 'error' not in analysis:
                # Authors
                authors = analysis['author_analysis']['author_frequency']
                for author, count in authors.items():
                    if author not in all_authors:
                        all_authors[author] = {}
                    all_authors[author][project_name] = count
                
                # Dates
                dates = analysis['timing_analysis'].get('date_frequency', {})
                for date, count in dates.items():
                    all_dates[date].append({
                        'repo': project_name,
                        'count': count
                    })

        # Find overlapping authors
        for author, repos in all_authors.items():
            if len(repos) > 1:
                correlation['same_authors'].add(author)

        # Find same-day commits across projects
        for date, repos in all_dates.items():
            if len(repos) > 1:
                total_commits = sum(repo['count'] for repo in repos)
                if total_commits > 10:  # Suspicious threshold
                    correlation['same_dates'][date] = {
                        'repositories': repos,
                        'total_commits': total_commits,
                        'suspicious': total_commits > 20
                    }

        # Look for coordinated attacks
        for date, info in correlation['same_dates'].items():
            if info['suspicious']:
                correlation['coordinated_attacks'].append({
                    'date': date,
                    'repositories': info['repositories'],
                    'total_commits': info['total_commits'],
                    'severity': 'HIGH' if info['total_commits'] > 30 else 'MEDIUM'
                })

        correlation['same_authors'] = list(correlation['same_authors'])

        return correlation

    def detect_suspicious_activity(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Detect suspicious activity across ecosystem"""
        suspicious = {
            'high_risk_projects': [],
            'medium_risk_projects': [],
            'coordinated_attacks': [],
            'c2_patterns': [],
            'suspicious_authors': [],
            'timing_anomalies': []
        }

        project_analysis = results.get('project_analysis', {})
        correlation = results.get('cross_project_correlation', {})

        # Identify high-risk projects
        for project_name, analysis in project_analysis.items():
            if 'error' not in analysis:
                security = analysis.get('security_assessment', {})
                risk_level = security.get('risk_level', 'LOW')
                
                if risk_level in ['HIGH', 'CRITICAL']:
                    suspicious['high_risk_projects'].append({
                        'project': project_name,
                        'risk_level': risk_level,
                        'risk_score': security.get('risk_score', 0),
                        'risk_factors': security.get('risk_factors', [])
                    })
                elif risk_level == 'MEDIUM':
                    suspicious['medium_risk_projects'].append({
                        'project': project_name,
                        'risk_level': risk_level,
                        'risk_score': security.get('risk_score', 0)
                    })

        # Add coordinated attacks
        suspicious['coordinated_attacks'] = correlation.get('coordinated_attacks', [])

        return suspicious

    def analyze_attack_evidence(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze attack evidence"""
        evidence = {
            'total_projects_analyzed': 0,
            'compromised_projects': 0,
            'c2_patterns_found': 0,
            'coordinated_attacks': 0,
            'attack_vectors': [],
            'compromise_assessment': 'UNKNOWN'
        }

        project_analysis = results.get('project_analysis', {})
        suspicious = results.get('suspicious_activity', {})

        # Count projects
        evidence['total_projects_analyzed'] = len(project_analysis)
        evidence['compromised_projects'] = len(suspicious.get('high_risk_projects', []))
        evidence['coordinated_attacks'] = len(suspicious.get('coordinated_attacks', []))

        # Count C2 patterns
        for project_name, analysis in project_analysis.items():
            if 'error' not in analysis:
                security = analysis.get('security_assessment', {})
                evidence['c2_patterns_found'] += security.get('c2_patterns_found', 0)

        # Determine compromise assessment
        compromised_ratio = evidence['compromised_projects'] / evidence['total_projects_analyzed']
        if compromised_ratio >= 0.5:
            evidence['compromise_assessment'] = 'CRITICAL'
        elif compromised_ratio >= 0.3:
            evidence['compromise_assessment'] = 'HIGH'
        elif compromised_ratio >= 0.1:
            evidence['compromise_assessment'] = 'MEDIUM'
        else:
            evidence['compromise_assessment'] = 'LOW'

        return evidence

    def assess_ecosystem_health(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall ecosystem health"""
        health = {
            'overall_health': 'UNKNOWN',
            'risk_distribution': {},
            'attack_vectors': [],
            'recommendations': []
        }

        evidence = results.get('attack_evidence', {})
        suspicious = results.get('suspicious_activity', {})

        # Risk distribution
        health['risk_distribution'] = {
            'total_projects': evidence['total_projects_analyzed'],
            'compromised': evidence['compromised_projects'],
            'medium_risk': len(suspicious.get('medium_risk_projects', [])),
            'safe': evidence['total_projects_analyzed'] - evidence['compromised_projects'] - len(suspicious.get('medium_risk_projects', []))
        }

        # Determine overall health
        compromised_ratio = evidence['compromised_projects'] / evidence['total_projects_analyzed']
        if compromised_ratio >= 0.5:
            health['overall_health'] = 'CRITICAL'
            health['recommendations'].append('CRITICAL: Ecosystem-wide compromise detected')
        elif compromised_ratio >= 0.3:
            health['overall_health'] = 'HIGH_RISK'
            health['recommendations'].append('HIGH: Significant ecosystem compromise')
        elif compromised_ratio >= 0.1:
            health['overall_health'] = 'MEDIUM_RISK'
            health['recommendations'].append('MEDIUM: Partial ecosystem compromise')
        else:
            health['overall_health'] = 'LOW_RISK'
            health['recommendations'].append('LOW: Minimal ecosystem impact')

        return health

    def generate_ecosystem_conclusion(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final ecosystem conclusion"""
        conclusion = {
            'overall_assessment': 'UNKNOWN',
            'threat_level': 'UNKNOWN',
            'ecosystem_compromised': False,
            'attack_vectors': [],
            'immediate_actions': [],
            'evidence_strength': 'WEAK'
        }

        health = results.get('ecosystem_health', {})
        evidence = results.get('attack_evidence', {})

        # Determine overall assessment
        overall_health = health.get('overall_health', 'UNKNOWN')
        conclusion['overall_assessment'] = overall_health
        
        if overall_health in ['CRITICAL', 'HIGH_RISK']:
            conclusion['threat_level'] = 'CRITICAL'
            conclusion['ecosystem_compromised'] = True
            conclusion['evidence_strength'] = 'STRONG'
            conclusion['attack_vectors'] = [
                'Coordinated supply chain attacks',
                'C2 communication patterns',
                'Cross-project coordination',
                'Ecosystem-wide compromise'
            ]
            conclusion['immediate_actions'] = [
                'CRITICAL: Immediate ecosystem-wide investigation required',
                'Audit all projects in compromised ecosystem',
                'Implement ecosystem-wide security monitoring',
                'Coordinate emergency response across all affected projects'
            ]
        elif overall_health == 'MEDIUM_RISK':
            conclusion['threat_level'] = 'MEDIUM'
            conclusion['evidence_strength'] = 'MODERATE'
            conclusion['immediate_actions'] = [
                'Monitor suspicious activity across ecosystem',
                'Review project security practices',
                'Implement enhanced monitoring'
            ]
        else:
            conclusion['threat_level'] = 'LOW'
            conclusion['evidence_strength'] = 'WEAK'
            conclusion['immediate_actions'] = [
                'Continue standard monitoring',
                'Maintain security best practices'
            ]

        return conclusion

def main():
    """Main investigation function"""
    print("🔍 COMPREHENSIVE CSS ECOSYSTEM DEEP INVESTIGATION")
    print("=" * 70)

    investigator = CSSEcosystemDeepInvestigator()
    results = investigator.investigate_ecosystem()

    # Save results
    with open('CSS_ECOSYSTEM_DEEP_INVESTIGATION.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print("✅ INVESTIGATION COMPLETE")
    print(f"📊 Results saved to: CSS_ECOSYSTEM_DEEP_INVESTIGATION.json")

    # Print key findings
    conclusion = results.get('conclusion', {})
    print(f"\n🎯 ECOSYSTEM CONCLUSION:")
    print(f"  Overall Assessment: {conclusion.get('overall_assessment', 'UNKNOWN')}")
    print(f"  Threat Level: {conclusion.get('threat_level', 'UNKNOWN')}")
    print(f"  Ecosystem Compromised: {conclusion.get('ecosystem_compromised', False)}")
    print(f"  Evidence Strength: {conclusion.get('evidence_strength', 'UNKNOWN')}")

    evidence = results.get('attack_evidence', {})
    print(f"\n🚨 ECOSYSTEM STATISTICS:")
    print(f"  Total Projects Analyzed: {evidence.get('total_projects_analyzed', 0)}")
    print(f"  Compromised Projects: {evidence.get('compromised_projects', 0)}")
    print(f"  C2 Patterns Found: {evidence.get('c2_patterns_found', 0)}")
    print(f"  Coordinated Attacks: {evidence.get('coordinated_attacks', 0)}")

    suspicious = results.get('suspicious_activity', {})
    high_risk = suspicious.get('high_risk_projects', [])
    print(f"\n🔥 HIGH RISK PROJECTS: {len(high_risk)}")
    for project in high_risk[:5]:  # Show top 5
        print(f"  - {project['project']}: {project['risk_level']} (Score: {project['risk_score']})")

    print("\n🔬 COMPREHENSIVE CSS ECOSYSTEM INVESTIGATION COMPLETED")

if __name__ == "__main__":
    main()
