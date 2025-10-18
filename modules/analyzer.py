"""Analyzer Module - Analysis and detection functions
Contains language detection, region detection, and exclusive games detection

Copyright (C) 2025 Myrient ROM Manager Contributors
This file is licensed under the GNU General Public License v3.0
See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""

import re
from collections import defaultdict
from .utils import Colors, convert_bytes_to_readable


def analyze_available_languages_and_regions(files):
    """
    Analyzes all files to detect available languages and regions
    Returns detailed statistics for user selection
    """
    print(f"\n{Colors.CYAN}🔍 Analyzing {len(files)} files to detect available languages and regions...{Colors.END}")
    
    # Language patterns (by language codes)
    language_stats = defaultdict(int)
    region_stats = defaultdict(int)
    language_examples = defaultdict(list)
    region_examples = defaultdict(list)
    
    # Define language patterns to detect
    language_patterns = {
        'Es': [r'\(Es\)', r'\(.*Es.*\)', r'Spain'],
        'En': [r'\(En\)', r'\(.*En.*\)', r'USA', r'UK', r'Australia'],
        'Fr': [r'\(Fr\)', r'\(.*Fr.*\)', r'France'],
        'De': [r'\(De\)', r'\(.*De.*\)', r'Germany'],
        'It': [r'\(It\)', r'\(.*It.*\)', r'Italy'],
        'Jp': [r'\(Jp\)', r'\(.*Jp.*\)', r'Japan'],
        'Pt': [r'\(Pt\)', r'\(.*Pt.*\)', r'Portugal', r'Brazil'],
        'Nl': [r'\(Nl\)', r'\(.*Nl.*\)', r'Netherlands'],
        'Ru': [r'\(Ru\)', r'\(.*Ru.*\)', r'Russia'],
        'Ko': [r'\(Ko\)', r'\(.*Ko.*\)', r'Korea'],
        'Zh': [r'\(Zh\)', r'\(.*Zh.*\)', r'China']
    }
    
    # Define SIMPLIFIED geographical regions (continents only)
    region_patterns = {
        'Europe': [r'\(Europe\)', r'\(.*Europe.*\)', r'Spain', r'France', r'Germany', r'Italy', r'UK', r'Netherlands', r'Poland', r'Russia', r'Scandinavia'],
        'Americas': [r'\(USA\)', r'\(.*USA.*\)', r'Brazil', r'America'],
        'Asia': [r'\(Asia\)', r'\(.*Asia.*\)', r'Japan', r'China', r'Korea'],
        'Oceania': [r'\(Australia\)', r'\(.*Australia.*\)', r'Oceania'],
        'World': [r'\(World\)', r'\(.*World.*\)', r'Global']
    }
    
    for file_info in files:
        filename = file_info['name']
        
        # Count languages
        for language_code, patterns in language_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    language_stats[language_code] += 1
                    if len(language_examples[language_code]) < 3:
                        language_examples[language_code].append(filename)
                    break
        
        # Count geographical regions (SIMPLIFIED)
        for continent, patterns in region_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    region_stats[continent] += 1
                    if len(region_examples[continent]) < 3:
                        region_examples[continent].append(filename)
                    break
    
    return {
        'languages': dict(language_stats),
        'regions': dict(region_stats),
        'language_examples': dict(language_examples),
        'region_examples': dict(region_examples),
        'total_files': len(files)
    }


def extract_key_words(title):
    """Extracts key identifying words from a game title for duplicate detection"""
    # Remove disc information temporarily to focus on game title
    title_without_disc = re.sub(r'\(Disc \d+\)', '', title, flags=re.IGNORECASE)
    title_without_disc = re.sub(r'Disc \d+', '', title_without_disc, flags=re.IGNORECASE)
    
    # Remove common parenthetical information (languages, regions, etc.)
    title_clean = re.sub(r'\([^)]*\)', '', title_without_disc)
    
    # Remove common separators and normalize
    title_clean = re.sub(r'[-_.:,]', ' ', title_clean)
    title_clean = re.sub(r'\s+', ' ', title_clean).strip()
    
    # Split into words
    words = title_clean.split()
    
    # Filter out common words that don't help identify games
    common_words = {
        'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by',
        'el', 'la', 'los', 'las', 'de', 'del', 'y', 'o', 'en', 'con', 'por', 'para',
        'le', 'la', 'les', 'de', 'du', 'et', 'ou', 'en', 'avec', 'pour', 'par',
        'der', 'die', 'das', 'den', 'und', 'oder', 'von', 'mit', 'für', 'auf',
        'il', 'la', 'lo', 'gli', 'le', 'di', 'e', 'o', 'con', 'per', 'da'
    }
    
    # Keep words that are 3+ characters and not common words
    key_words = []
    for word in words:
        word_clean = word.lower().strip()
        if len(word_clean) >= 2 and word_clean not in common_words:
            # Keep numbers and meaningful words
            if word_clean.isdigit() or word_clean.isalpha():
                key_words.append(word_clean)
    
    return key_words


def extract_disc_info(filename):
    """Extracts disc information from filename"""
    disc_match = re.search(r'\(Disc (\d+)\)', filename, re.IGNORECASE)
    if disc_match:
        return int(disc_match.group(1))
    
    disc_match = re.search(r'Disc (\d+)', filename, re.IGNORECASE)
    if disc_match:
        return int(disc_match.group(1))
    
    return None


def detect_european_countries(files, language_code):
    """Detects specific European countries available for a given language"""
    european_countries = defaultdict(int)
    
    # Define European country patterns
    country_patterns = {
        'Spain': [r'Spain', r'\(Es\)'],
        'France': [r'France', r'\(Fr\)'],
        'Germany': [r'Germany', r'\(De\)'],
        'Italy': [r'Italy', r'\(It\)'],
        'UK': [r'UK', r'United Kingdom', r'\(En\).*Europe'],
        'Netherlands': [r'Netherlands', r'\(Nl\)'],
        'Poland': [r'Poland', r'\(Pl\)'],
        'Russia': [r'Russia', r'\(Ru\)'],
        'Europe (Multi)': [r'\(Europe\)', r'\([A-Z][a-z](?:,[A-Z][a-z])+\).*Europe']
    }
    
    for file_info in files:
        filename = file_info['name']
        
        # Check if file contains the specified language
        if language_code:
            lang_patterns = [
                fr'\({language_code}\)',
                fr'\([^)]*{language_code}[^)]*\)',
            ]
            # For Spanish, also check for Spain
            if language_code == 'Es':
                lang_patterns.append(r'Spain')
            
            if not any(re.search(pattern, filename, re.IGNORECASE) for pattern in lang_patterns):
                continue
        
        # Check which European countries match
        for country, patterns in country_patterns.items():
            if any(re.search(pattern, filename, re.IGNORECASE) for pattern in patterns):
                european_countries[country] += 1
                break
    
    return dict(european_countries)
