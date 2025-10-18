#!/usr/bin/env python3
# Copyright (C) 2025 Myrient ROM Manager Contributors
# This file is licensed under the GNU General Public License v3.0
# See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""
Myrient ROM Manager - Interactive version
Main interactive program with menu, language priority selection, and enhanced preview
"""

import sys
import os
import re
import requests
import time
import zipfile
import glob
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote

# Import functions from downloadroms.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from downloadroms import (
    extract_base_title,
    extract_region,
    get_priority,
    is_valid_region,
    has_spanish_language,
    download_and_filter
)

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Prints the welcome banner"""
    banner = f"""
{Colors.CYAN}{'='*80}
{Colors.BOLD}🎮 MYRIENT ROM MANAGER - Interactive Mode 🎮{Colors.END}
{Colors.CYAN}{'='*80}{Colors.END}

{Colors.YELLOW}Welcome to the ROM downloader for Myrient platform!{Colors.END}
{Colors.BLUE}📦 Optimized for: https://myrient.erista.me/{Colors.END}

"""
    print(banner)

def print_menu():
    """Prints the main menu"""
    menu = f"""
{Colors.BOLD}🌍 SELECT PRIORITY LANGUAGE:{Colors.END}

{Colors.GREEN}1.{Colors.END} Spanish (Spain) 🇪🇸
   Priority: Spain > Europe (with Es) > Japan
   
{Colors.GREEN}2.{Colors.END} English (Europe/USA) 🇬🇧
   Priority: Europe (with En) > USA > Japan
   
{Colors.GREEN}3.{Colors.END} French (France) 🇫🇷
   Priority: France > Europe (with Fr) > Japan
   
{Colors.GREEN}4.{Colors.END} German (Germany) 🇩🇪
   Priority: Germany > Europe (with De) > Japan
   
{Colors.GREEN}5.{Colors.END} Italian (Italy) 🇮🇹
   Priority: Italy > Europe (with It) > Japan

{Colors.GREEN}6.{Colors.END} Japanese (Japan) 🇯🇵
   Priority: Japan only

{Colors.RED}0.{Colors.END} Exit

"""
    print(menu)

def get_language_config(choice):
    """Returns the language configuration based on user choice"""
    configs = {
        '1': {
            'name': 'Spanish (Spain)',
            'regions': ['Spain', 'Europe', 'Japan'],
            'language_code': 'Es',
            'priority': {'Spain': 1, 'Europe': 2, 'Japan': 3, 'Es': 4}
        },
        '2': {
            'name': 'English (Europe/USA)',
            'regions': ['Europe', 'USA', 'Japan'],
            'language_code': 'En',
            'priority': {'Europe': 1, 'USA': 2, 'Japan': 3, 'En': 4}
        },
        '3': {
            'name': 'French (France)',
            'regions': ['France', 'Europe', 'Japan'],
            'language_code': 'Fr',
            'priority': {'France': 1, 'Europe': 2, 'Japan': 3, 'Fr': 4}
        },
        '4': {
            'name': 'German (Germany)',
            'regions': ['Germany', 'Europe', 'Japan'],
            'language_code': 'De',
            'priority': {'Germany': 1, 'Europe': 2, 'Japan': 3, 'De': 4}
        },
        '5': {
            'name': 'Italian (Italy)',
            'regions': ['Italy', 'Europe', 'Japan'],
            'language_code': 'It',
            'priority': {'Italy': 1, 'Europe': 2, 'Japan': 3, 'It': 4}
        },
        '6': {
            'name': 'Japanese (Japan)',
            'regions': ['Japan'],
            'language_code': None,
            'priority': {'Japan': 1}
        }
    }
    return configs.get(choice)

def convert_bytes_to_readable(bytes_size):
    """Converts bytes to human-readable format"""
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PiB"

def extract_downloaded_files(output_dir):
    """Extract all ZIP files in the output directory"""
    print(f"\n{Colors.CYAN}📦 STARTING FILE EXTRACTION{Colors.END}")
    print("=" * 60)
    
    zip_files = list(Path(output_dir).glob("*.zip"))
    
    if not zip_files:
        print(f"{Colors.YELLOW}⚠️  No ZIP files found to extract{Colors.END}")
        return 0, 0
    
    extracted_count = 0
    error_count = 0
    
    for zip_file in zip_files:
        try:
            print(f"\n📦 Extracting: {Colors.CYAN}{zip_file.name}{Colors.END}")
            
            # Create extraction directory (same name as zip file without extension)
            extract_dir = zip_file.parent / zip_file.stem
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Get list of files in zip
                file_list = zip_ref.namelist()
                print(f"  📄 Contains {len(file_list)} files")
                
                # Extract with progress indication
                for i, file_name in enumerate(file_list, 1):
                    zip_ref.extract(file_name, extract_dir)
                    if i % 5 == 0 or i == len(file_list):  # Show progress every 5 files
                        progress = (i / len(file_list)) * 100
                        print(f"  📊 Progress: {progress:.1f}% ({i}/{len(file_list)} files)", end='\r', flush=True)
                
                print(f"\n  ✅ Successfully extracted to: {Colors.GREEN}{extract_dir.name}/{Colors.END}")
                extracted_count += 1
                
        except zipfile.BadZipFile:
            print(f"  ❌ {Colors.RED}Error: Invalid ZIP file{Colors.END}")
            error_count += 1
        except Exception as e:
            print(f"  ❌ {Colors.RED}Error extracting: {str(e)}{Colors.END}")
            error_count += 1
    
    # Summary
    print(f"\n{Colors.BOLD}📦 EXTRACTION SUMMARY:{Colors.END}")
    print("=" * 40)
    print(f"✅ Extracted: {Colors.GREEN}{extracted_count}{Colors.END}")
    print(f"❌ Errors: {Colors.RED}{error_count}{Colors.END}")
    print(f"📁 Location: {Colors.CYAN}{output_dir}{Colors.END}")
    
    return extracted_count, error_count

def fetch_directory_listing(url, include_demos=False):
    """Fetches the directory listing from Myrient URL"""
    try:
        print(f"\n{Colors.YELLOW}⏳ Fetching directory listing from Myrient...{Colors.END}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        
        files = []
        for link in links:
            href = link.get('href', '')
            if href.endswith('.zip'):
                # Decode URL-encoded filename
                decoded_name = unquote(href)
                
                # Get file size from the row
                parent_row = link.find_parent('tr')
                size_text = "0"
                if parent_row:
                    cells = parent_row.find_all('td')
                    if len(cells) >= 2:
                        size_text = cells[1].get_text(strip=True)
                
                # Convert size to bytes
                size_bytes = parse_size(size_text)
                
                # Include or exclude demos (check both original and decoded)
                if not include_demos and ('(Demo)' in href or '(Demo)' in decoded_name):
                    continue
                
                full_url = urljoin(url, href)
                files.append({
                    'name': decoded_name,  # Use decoded name for processing
                    'url': full_url,      # Keep original URL for downloading
                    'size': size_bytes,
                    'size_text': size_text
                })
        
        return files
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}❌ Error fetching URL: {e}{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        return None

def parse_size(size_text):
    """Parses size text to bytes"""
    if not size_text or size_text == '-':
        return 0
    
    # Remove commas and extract number and unit
    size_text = size_text.strip().replace(',', '')
    match = re.match(r'([\d.]+)\s*([KMGT]?i?B?)', size_text, re.IGNORECASE)
    
    if not match:
        return 0
    
    number = float(match.group(1))
    unit = match.group(2).upper()
    
    units = {
        'B': 1,
        'KB': 1024,
        'KIB': 1024,
        'MB': 1024**2,
        'MIB': 1024**2,
        'GB': 1024**3,
        'GIB': 1024**3,
        'TB': 1024**4,
        'TIB': 1024**4
    }
    
    return int(number * units.get(unit, 1))

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

def show_available_options(analysis):
    """Shows available languages and regions with file counts"""
    print(f"\n{Colors.BOLD}🌍 LANGUAGES DETECTED IN THIS URL:{Colors.END}")
    print("=" * 60)
    
    languages = analysis['languages']
    regions = analysis['regions']
    
    if languages:
        for i, (lang_code, count) in enumerate(sorted(languages.items(), key=lambda x: x[1], reverse=True), 1):
            examples = analysis['language_examples'].get(lang_code, [])
            example_text = f" (e.g., {examples[0][:50]}...)" if examples else ""
            print(f"{i:2}. {Colors.CYAN}{lang_code}{Colors.END}: {Colors.YELLOW}{count:,} files{Colors.END}{example_text}")
    else:
        print(f"{Colors.RED}No specific language codes detected{Colors.END}")
    
    print(f"\n{Colors.BOLD}🗺️  REGIONS/CONTINENTS DETECTED:{Colors.END}")
    print("=" * 60)
    
    if regions:
        for i, (region, count) in enumerate(sorted(regions.items(), key=lambda x: x[1], reverse=True), 1):
            examples = analysis['region_examples'].get(region, [])
            example_text = f" (e.g., {examples[0][:50]}...)" if examples else ""
            print(f"{i:2}. {Colors.GREEN}{region}{Colors.END}: {Colors.YELLOW}{count:,} files{Colors.END}{example_text}")
    else:
        print(f"{Colors.RED}No specific regions detected{Colors.END}")

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

def detect_exclusive_games(files, priority_games=None):
    """Detects games that are exclusive to specific countries/regions with keyword filtering"""
    print(f"\n{Colors.CYAN}🔍 Analyzing for exclusive games by region...{Colors.END}")
    print(f"{Colors.CYAN}🧠 Using intelligent keyword filtering to remove duplicates...{Colors.END}")
    
    # If priority games are provided, create a set of their keywords for filtering
    priority_keywords = set()
    if priority_games:
        print(f"{Colors.CYAN}🔍 Filtering against {len(priority_games)} priority language games...{Colors.END}")
        for game in priority_games:
            title = extract_base_title(game['name'])
            keywords = tuple(sorted(extract_key_words(title)[:4]))
            if keywords:
                priority_keywords.add(keywords)
    
    # Group games by base title
    games_by_title = defaultdict(list)
    
    for file_info in files:
        filename = file_info['name']
        base_title = extract_base_title(filename)
        
        # Detect region/country for this file
        region_info = {
            'filename': filename,
            'size': file_info['size'],
            'base_title': base_title,
            'countries': []
        }
        
        # Check for specific countries
        country_patterns = {
            'Japan': [r'Japan', r'\(Jp\)', r'\(.*Jp.*\)'],
            'USA': [r'USA', r'America', r'\(En\).*USA'],
            'Spain': [r'Spain', r'\(Es\)'],
            'France': [r'France', r'\(Fr\)'],
            'Germany': [r'Germany', r'\(De\)'],
            'Italy': [r'Italy', r'\(It\)'],
            'UK': [r'UK', r'United Kingdom'],
            'Korea': [r'Korea', r'\(Ko\)'],
            'China': [r'China', r'\(Zh\)'],
            'Brazil': [r'Brazil', r'Brasil'],
            'Australia': [r'Australia'],
            'Europe': [r'\(Europe\)', r'Europe']
        }
        
        for country, patterns in country_patterns.items():
            if any(re.search(pattern, filename, re.IGNORECASE) for pattern in patterns):
                region_info['countries'].append(country)
        
        # If no specific country found, mark as "Unknown"
        if not region_info['countries']:
            region_info['countries'] = ['Unknown']
        
        games_by_title[base_title].append(region_info)
    
    # Find exclusives
    exclusive_games = defaultdict(list)
    priority_duplicates_found = 0
    duplicate_check_counter = 0
    
    for title, regions in games_by_title.items():
        # Get all countries for this title
        all_countries = set()
        for region_info in regions:
            all_countries.update(region_info['countries'])
        
        # Remove "Unknown" and "Europe" from consideration
        filtered_countries = all_countries - {'Unknown', 'Europe'}
        
        # If only one specific country remains, it's truly exclusive
        if len(filtered_countries) == 1:
            exclusive_country = list(filtered_countries)[0]
            
            # Additional filter: exclude very common titles that might have false exclusives
            title_lower = title.lower()
            common_patterns = [
                'demo', 'preview', 'beta', 'sample', 'promo',
                'action replay', 'gameshark', 'cheat'
            ]
            
            # Skip if it's a common utility/demo type
            if any(pattern in title_lower for pattern in common_patterns):
                continue
            
            # Check if this exclusive game already exists in priority language
            if priority_keywords:
                title_keywords = tuple(sorted(extract_key_words(title)[:4]))
                
                # Special handling for numbered series (007, etc.)
                is_duplicate = False
                if title_keywords in priority_keywords:
                    is_duplicate = True
                else:
                    # Check for numbered series games (like 007, Medal of Honor, etc.)
                    for priority_keyword_set in priority_keywords:
                        # If both have numbers and share at least one significant keyword
                        title_numbers = [word for word in title_keywords if word.isdigit() or any(char.isdigit() for char in word)]
                        priority_numbers = [word for word in priority_keyword_set if word.isdigit() or any(char.isdigit() for char in word)]
                        
                        if title_numbers and priority_numbers:
                            # Check if they share any numbers
                            if any(num in priority_numbers for num in title_numbers):
                                # For numbered series, just having the number is enough to consider it a duplicate
                                is_duplicate = True
                                priority_duplicates_found += 1
                                if priority_duplicates_found % 20 == 0:  # Only show every 20th priority duplicate
                                    print(f"  🔍 Numbered series duplicate found: '{title}' (shares number with priority game) → Excluding from {exclusive_country}")
                                break
                
                if is_duplicate and title_keywords in priority_keywords:
                    priority_duplicates_found += 1
                    if priority_duplicates_found % 20 == 0:  # Only show every 20th priority duplicate
                        print(f"  🔍 Priority duplicate found: '{title}' → Excluding from {exclusive_country}")
                    continue
                elif is_duplicate:
                    continue
                
            # Only add files that are actually from that specific country
            for region_info in regions:
                if exclusive_country in region_info['countries']:
                    exclusive_games[exclusive_country].append(region_info)
    
    # Now apply keyword-based deduplication across ALL countries
    print(f"{Colors.CYAN}🔍 Applying cross-country keyword deduplication...{Colors.END}")
    
    # Create a global keyword map to find duplicates across countries
    global_keyword_map = {}
    games_to_remove = []
    
    # First pass: map all games by their keywords
    for country, games in exclusive_games.items():
        for game in games:
            keywords = tuple(sorted(extract_key_words(game['base_title'])[:4]))
            if keywords and keywords in global_keyword_map:
                # Duplicate found! Decide which to keep
                existing_country, existing_game = global_keyword_map[keywords]
                
                # Priority order for keeping games (you can adjust this)
                country_priority = {
                    'USA': 1, 'Japan': 2, 'UK': 3, 'Germany': 4, 
                    'France': 5, 'Spain': 6, 'Italy': 7, 'Australia': 8,
                    'Korea': 9, 'China': 10, 'Brazil': 11
                }
                
                current_priority = country_priority.get(country, 99)
                existing_priority = country_priority.get(existing_country, 99)
                
                if current_priority < existing_priority:
                    # Current game has higher priority, remove the existing one
                    games_to_remove.append((existing_country, existing_game))
                    global_keyword_map[keywords] = (country, game)
                else:
                    # Existing game has higher priority, mark current for removal
                    games_to_remove.append((country, game))
                
                # Show what we're comparing (reduced verbosity)
                duplicate_check_counter += 1
                if duplicate_check_counter % 100 == 0:  # Only show every 100th duplicate
                    print(f"  🔍 Duplicate detected: '{keywords}' keywords")
                    print(f"    {existing_country}: {existing_game['base_title']}")
                    print(f"    {country}: {game['base_title']}")
                    print(f"    → Keeping {existing_country if existing_priority <= current_priority else country} version")
                
            elif keywords:
                global_keyword_map[keywords] = (country, game)
    
    # Remove the duplicates
    duplicates_removed = 0
    for country, game_to_remove in games_to_remove:
        if game_to_remove in exclusive_games[country]:
            exclusive_games[country].remove(game_to_remove)
            duplicates_removed += 1
    
    # Clean up empty country lists
    exclusive_games = {k: v for k, v in exclusive_games.items() if v}
    
    if priority_duplicates_found > 0:
        print(f"{Colors.GREEN}✅ Filtered out {priority_duplicates_found} games that already exist in priority language{Colors.END}")
    
    print(f"{Colors.GREEN}✅ Removed {duplicates_removed} cross-country duplicates{Colors.END}")
    print(f"{Colors.GREEN}📊 Final exclusive games by country:{Colors.END}")
    for country, games in sorted(exclusive_games.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {country}: {len(games)} unique games")
    
    return dict(exclusive_games)

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

def get_priority_language_from_config(config):
    """Gets the priority language from config for comparison"""
    return config.get('primary_language', '')

def check_keywords_similarity(exclusive_title, valid_titles, threshold=0.7):
    """Checks if exclusive game has similar keywords to any valid game"""
    exclusive_keywords = set(extract_key_words(exclusive_title))
    
    if not exclusive_keywords:
        return False, None
    
    for valid_title in valid_titles:
        valid_keywords = set(extract_key_words(valid_title))
        
        if not valid_keywords:
            continue
        
        # Calculate similarity based on keyword overlap
        intersection = exclusive_keywords & valid_keywords
        union = exclusive_keywords | valid_keywords
        
        if len(union) == 0:
            similarity = 0
        else:
            similarity = len(intersection) / len(union)
        
        if similarity >= threshold:
            return True, valid_title
    
    return False, None

def show_exclusive_games_options(exclusive_games):
    """Shows available exclusive games by country and asks user for selection"""
    if not exclusive_games:
        print(f"{Colors.YELLOW}🤷 No exclusive games detected{Colors.END}")
        return []
    
    print(f"\n{Colors.BOLD}🎮 EXCLUSIVE GAMES DETECTED:{Colors.END}")
    print("=" * 60)
    
    country_options = []
    for i, (country, games) in enumerate(sorted(exclusive_games.items(), key=lambda x: len(x[1]), reverse=True), 1):
        total_size = sum(game['size'] for game in games)
        print(f"  {i}. {Colors.GREEN}{country}{Colors.END}: {Colors.YELLOW}{len(games)} exclusive games{Colors.END} ({convert_bytes_to_readable(total_size)})")
        
        # Show some examples
        examples = games[:3]
        for game in examples:
            title = extract_base_title(game['filename'])
            print(f"     • {title[:50]}")
        if len(games) > 3:
            print(f"     • ... and {len(games) - 3} more")
        
        country_options.append((country, games))
        print()
    
    print(f"  0. {Colors.YELLOW}Skip exclusive games{Colors.END}")
    
    # Get user selection
    selected_exclusives = []
    print(f"\n{Colors.BOLD}🎯 SELECT EXCLUSIVE REGIONS TO INCLUDE:{Colors.END}")
    print(f"{Colors.CYAN}(You can select multiple options separated by commas, e.g., 1,3,5){Colors.END}")
    
    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Select exclusive regions (0-{len(country_options)}) or 0 to skip: {Colors.END}").strip()
            
            if choice == "0":
                print(f"✅ Skipping exclusive games")
                break
            
            # Parse multiple selections
            selections = [int(x.strip()) for x in choice.split(',') if x.strip()]
            
            valid_selections = []
            for selection in selections:
                if 1 <= selection <= len(country_options):
                    valid_selections.append(selection)
                else:
                    print(f"{Colors.RED}❌ Invalid choice: {selection}. Must be 1-{len(country_options)}{Colors.END}")
                    continue
            
            if valid_selections:
                for selection in valid_selections:
                    country, games = country_options[selection - 1]
                    selected_exclusives.extend(games)
                    print(f"✅ Added {Colors.GREEN}{len(games)} exclusive games from {country}{Colors.END}")
                break
            
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input. Please enter numbers separated by commas{Colors.END}")
    
    return selected_exclusives

def get_user_priority_selection(analysis, files):
    """Gets user's priority selection for languages and regions with enhanced country selection"""
    languages = analysis['languages']
    regions = analysis['regions']
    
    # Language code to full name mapping
    language_names = {
        'Es': 'Spanish (Spain)',
        'En': 'English',
        'Fr': 'French (France)', 
        'De': 'German (Germany)',
        'It': 'Italian (Italy)',
        'Jp': 'Japanese (Japan)',
        'Pt': 'Portuguese (Portugal/Brazil)',
        'Nl': 'Dutch (Netherlands)',
        'Ru': 'Russian (Russia)',
        'Ko': 'Korean (Korea)',
        'Zh': 'Chinese (China)'
    }
    
    # Region code to full name mapping (SIMPLIFIED CONTINENTS)
    region_names = {
        'Europe': 'Europe (Spain, France, Germany, Italy, UK, etc.)',
        'Americas': 'Americas (USA, Brazil)',
        'Asia': 'Asia (Japan, China, Korea)',
        'Oceania': 'Oceania (Australia)',
        'World': 'World (Global release)'
    }
    
    # Clear separator and highlighted section
    print("\n" + "🟦" * 60)
    print(f"{Colors.BOLD}{Colors.YELLOW}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.RED}🎯 ATTENTION! YOU MUST SELECT YOUR PREFERENCES HERE 🎯{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}📋 SELECT YOUR PRIORITIES:{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'=' * 60}{Colors.END}")
    print("🟦" * 60)
    
    # Get language priority
    selected_language = None
    if languages:
        print(f"\n{Colors.BOLD}{Colors.RED}🔻 STEP 1: SELECT YOUR PREFERRED LANGUAGE 🔻{Colors.END}")
        print(f"{Colors.BOLD}1️⃣  PRIMARY PRIORITY - Select preferred language:{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
        lang_list = list(sorted(languages.items(), key=lambda x: x[1], reverse=True))
        
        for i, (lang_code, count) in enumerate(lang_list, 1):
            lang_name = language_names.get(lang_code, lang_code)
            print(f"  {Colors.BOLD}{i}.{Colors.END} {Colors.CYAN}{lang_code} - {lang_name}{Colors.END} ({count:,} files)")
        
        print(f"  {Colors.BOLD}0.{Colors.END} {Colors.YELLOW}No language preference (include all){Colors.END}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
        
        while True:
            try:
                choice = input(f"\n{Colors.BOLD}{Colors.GREEN}👉 Select language priority (0-{len(lang_list)}): {Colors.END}").strip()
                choice_num = int(choice)
                
                if choice_num == 0:
                    selected_language = None
                    print(f"✅ No language preference - all languages included")
                    break
                elif 1 <= choice_num <= len(lang_list):
                    selected_language = lang_list[choice_num - 1][0]
                    lang_name = language_names.get(selected_language, selected_language)
                    print(f"✅ Selected language: {Colors.CYAN}{selected_language} - {lang_name}{Colors.END}")
                    break
                else:
                    print(f"{Colors.RED}❌ Invalid choice. Please select 0-{len(lang_list)}{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Invalid input. Please enter a number{Colors.END}")
    
    # Get region priority
    selected_region = None
    selected_specific_country = None
    
    if regions:
        print(f"\n{Colors.BOLD}{Colors.RED}🔻 STEP 2: SELECT YOUR PREFERRED REGION 🔻{Colors.END}")
        print(f"{Colors.BOLD}2️⃣  SECONDARY PRIORITY - Select preferred region/continent:{Colors.END}")
        print(f"{Colors.GREEN}{'─' * 60}{Colors.END}")
        region_list = list(sorted(regions.items(), key=lambda x: x[1], reverse=True))
        
        for i, (region, count) in enumerate(region_list, 1):
            region_name = region_names.get(region, region)
            print(f"  {Colors.BOLD}{i}.{Colors.END} {Colors.GREEN}{region} - {region_name}{Colors.END} ({count:,} files)")
        
        print(f"  {Colors.BOLD}0.{Colors.END} {Colors.YELLOW}No region preference (include all){Colors.END}")
        print(f"{Colors.GREEN}{'─' * 60}{Colors.END}")
        
        while True:
            try:
                choice = input(f"\n{Colors.BOLD}{Colors.GREEN}👉 Select region priority (0-{len(region_list)}): {Colors.END}").strip()
                choice_num = int(choice)
                
                if choice_num == 0:
                    selected_region = None
                    print(f"✅ No region preference - all regions included")
                    break
                elif 1 <= choice_num <= len(region_list):
                    selected_region = region_list[choice_num - 1][0]
                    region_name = region_names.get(selected_region, selected_region)
                    print(f"✅ Selected region: {Colors.GREEN}{selected_region} - {region_name}{Colors.END}")
                    
                    # If Europe is selected, automatically choose the most relevant country
                    if selected_region == 'Europe' and selected_language:
                        # Detect available European countries for the selected language
                        european_countries = detect_european_countries(files, selected_language)
                        
                        if european_countries:
                            # Automatically select the best matching country for the language
                            language_country_map = {
                                'Es': 'Spain',
                                'Fr': 'France', 
                                'De': 'Germany',
                                'It': 'Italy',
                                'En': 'UK'
                            }
                            
                            preferred_country = language_country_map.get(selected_language)
                            
                            # If the preferred country exists and has files, select it automatically
                            if preferred_country and preferred_country in european_countries:
                                selected_specific_country = preferred_country
                                file_count = european_countries[preferred_country]
                                print(f"🎯 Auto-selected specific country: {Colors.BLUE}{preferred_country}{Colors.END} ({file_count:,} files) - best match for {selected_language}")
                            else:
                                # Otherwise, select the country with most files
                                selected_specific_country = max(european_countries.items(), key=lambda x: x[1])[0]
                                file_count = european_countries[selected_specific_country]
                                print(f"🎯 Auto-selected most available country: {Colors.BLUE}{selected_specific_country}{Colors.END} ({file_count:,} files)")
                        else:
                            selected_specific_country = None
                    
                    break
                else:
                    print(f"{Colors.RED}❌ Invalid choice. Please select 0-{len(region_list)}{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Invalid input. Please enter a number{Colors.END}")
    
    return {
        'language': selected_language,
        'region': selected_region,
        'specific_country': selected_specific_country
    }

def has_language_in_file(filename, language_code):
    """Checks if the file contains the specified language code"""
    if not language_code:
        return True
    
    # Search for language patterns like (En,Fr,De,Es,It)
    lang_match = re.search(r'\([A-Z][a-z](?:,[A-Z][a-z])+\)', filename)
    if lang_match:
        languages = lang_match.group(0)
        return language_code in languages
    
    # If no languages specified in Europe, accept it
    if 'Europe' in filename and not lang_match:
        return True
    
    return True

def is_valid_region_for_config(filename, config):
    """Validates if the file matches the selected language configuration"""
    region = extract_region(filename)
    
    # Check if region is in allowed regions
    if region not in config['regions'] and region not in config['priority']:
        return False
    
    # For Europe files, check language
    if 'Europe' in filename and config['language_code']:
        return has_language_in_file(filename, config['language_code'])
    
    return True

def analyze_files(files, config, include_demos):
    """Analyzes files and categorizes them as valid or invalid"""
    valid = []
    invalid = []
    
    for file_info in files:
        filename = file_info['name']
        
        # Skip demos if not included
        if not include_demos and '(Demo)' in filename:
            invalid.append((filename, "Demo file excluded", file_info['size']))
            continue
        
        # Validate region
        if is_valid_region_for_config(filename, config):
            region = extract_region(filename)
            priority = config['priority'].get(region, 999)
            valid.append((filename, region, priority, file_info['size']))
        else:
            region = extract_region(filename)
            invalid.append((filename, f"Region '{region}' not allowed or missing {config['language_code']}", file_info['size']))
    
    return valid, invalid

def group_by_title(valid_files):
    """Groups files by base title"""
    titles = defaultdict(list)
    for filename, region, priority, size in valid_files:
        base_title = extract_base_title(filename)
        titles[base_title].append((filename, region, priority, size))
    return titles

def select_best_files(titles_dict, config):
    """Selects the best file for each title based on priority"""
    selected = []
    discarded = []
    
    for title, files in titles_dict.items():
        if len(files) == 1:
            selected.append(files[0])
        else:
            # Sort by priority (lower is better)
            files_sorted = sorted(files, key=lambda x: x[2])
            selected.append(files_sorted[0])
            
            # Discard the rest
            for file_info in files_sorted[1:]:
                discarded.append(file_info)
    
    return selected, discarded

def print_preview_table(selected, discarded, invalid, config):
    """Prints the preview table organized by priority with samples"""
    if not selected:
        print(f"\n{Colors.YELLOW}⚠️  No files match the criteria{Colors.END}")
        return
    
    # Group selected files by priority
    priority_groups = defaultdict(list)
    for filename, region, priority, size in selected:
        priority_groups[priority].append((filename, region, priority, size))
    
    # Sort priorities
    sorted_priorities = sorted(priority_groups.keys())
    
    print(f"\n{Colors.CYAN}{'='*90}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}🎯 ARCHIVOS SELECCIONADOS POR PRIORIDAD{Colors.END}")
    print(f"{Colors.CYAN}{'='*90}{Colors.END}")
    
    total_files = 0
    total_size = 0
    
    for priority in sorted_priorities:
        files_in_priority = priority_groups[priority]
        priority_size = sum(f[3] for f in files_in_priority)
        
        # Get region name for this priority
        region_name = files_in_priority[0][1]
        
        # Priority colors
        priority_color = Colors.GREEN if priority == 1 else Colors.YELLOW if priority == 2 else Colors.BLUE
        
        print(f"\n{priority_color}{Colors.BOLD}📂 PRIORIDAD {priority} - {region_name.upper()}: {len(files_in_priority)} archivos ({convert_bytes_to_readable(priority_size)}){Colors.END}")
        print(f"{priority_color}{'-'*80}{Colors.END}")
        
        # Show first 10 files as examples
        sample_files = files_in_priority[:10]
        
        for filename, region, _, size in sample_files:
            title = extract_base_title(filename)
            size_text = convert_bytes_to_readable(size)
            print(f"  {title[:60]:<62} {size_text:>10}")
        
        # If there are more files, show summary
        if len(files_in_priority) > 10:
            remaining = len(files_in_priority) - 10
            remaining_size = sum(f[3] for f in files_in_priority[10:])
            print(f"  {Colors.CYAN}... and {remaining} more files ({convert_bytes_to_readable(remaining_size)}){Colors.END}")
        
        total_files += len(files_in_priority)
        total_size += priority_size
    
    # Summary
    print(f"\n{Colors.CYAN}{'='*90}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}📊 TOTAL SUMMARY:{Colors.END}")
    print(f"   📁 Total files: {total_files}")
    print(f"   💾 Total size: {convert_bytes_to_readable(total_size)}")
    
    # Show discarded summary if any
    if discarded:
        discarded_size = sum(f[3] for f in discarded)
        print(f"   ⚠️  Archivos descartados (duplicados): {len(discarded)} ({convert_bytes_to_readable(discarded_size)})")
    
    # Show ignored summary if any
    if invalid:
        print(f"   ❌ Archivos ignorados: {len(invalid)}")
    
    print(f"{Colors.CYAN}{'='*90}{Colors.END}")
    
    # Show some examples of what's being discarded/ignored
    if discarded:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  EXAMPLES OF DISCARDED FILES (lower priority):{Colors.END}")
        for filename, region, priority, size in discarded[:5]:
            title = extract_base_title(filename)
            print(f"  📤 {title[:50]:<52} ({region})")
        if len(discarded) > 5:
            print(f"  {Colors.YELLOW}... and {len(discarded) - 5} more{Colors.END}")
    
    if invalid and len(invalid) > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ EXAMPLES OF IGNORED FILES:{Colors.END}")
        for filename, reason, size in invalid[:5]:
            title = extract_base_title(filename)
            print(f"  🚫 {title[:40]:<42} ({reason})")
        if len(invalid) > 5:
            print(f"  {Colors.RED}... and {len(invalid) - 5} more{Colors.END}")

def ask_confirmation():
    """Asks user for confirmation to proceed"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*100}{Colors.END}")
    while True:
        response = input(f"{Colors.BOLD}Do you want to proceed with the download? (yes/no): {Colors.END}").strip().lower()
        if response in ['yes', 'y', 'si', 's']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print(f"{Colors.RED}Please answer 'yes' or 'no'{Colors.END}")

def ask_yes_no(question):
    """Asks user a yes/no question with default 'no' on empty input"""
    while True:
        response = input(f"{Colors.BOLD}{question} (yes/no) [default: no]: {Colors.END}").strip().lower()
        if response in ['yes', 'y', 'si', 's']:
            return True
        elif response in ['no', 'n'] or response == '':  # Empty input defaults to 'no'
            return False
        else:
            print(f"{Colors.RED}Please answer 'yes' or 'no'{Colors.END}")

def create_custom_config(user_priorities, analysis):
    """Creates a custom configuration based on user priorities"""
    config_name = f"Custom ({user_priorities['language'] or 'All'}/{user_priorities['region'] or 'All'}"
    if user_priorities.get('specific_country'):
        config_name += f"/{user_priorities['specific_country']}"
    config_name += ")"
    
    return {
        'name': config_name,
        'primary_language': user_priorities['language'],
        'primary_region': user_priorities['region'],
        'specific_country': user_priorities.get('specific_country'),
        'available_languages': list(analysis['languages'].keys()),
        'available_regions': list(analysis['regions'].keys())
    }

def analyze_files_with_priorities(files, config, include_demos):
    """Analyzes files using intelligent priority configuration with multi-disc support"""
    valid = []
    invalid = []
    
    # First, create a map to track which titles have versions in the primary language
    primary_language_titles = set()
    if config['primary_language']:
        for file_info in files:
            filename = file_info['name']
            base_title = extract_base_title(filename)
            
            # Check if this file has the primary language
            if config['primary_language'] == 'Es':
                if ('Spain' in filename or 
                    re.search(r'\(Es\)', filename) or 
                    re.search(r'\([^)]*Es[^)]*\)', filename)):
                    primary_language_titles.add(base_title)
            else:
                lang_patterns = [
                    fr'\({config["primary_language"]}\)',
                    fr'\([^)]*{config["primary_language"]}[^)]*\)',
                ]
                if any(re.search(pattern, filename, re.IGNORECASE) for pattern in lang_patterns):
                    primary_language_titles.add(base_title)
    
    # Group files by base title to handle multi-disc games properly
    files_by_title = defaultdict(list)
    for file_info in files:
        filename = file_info['name']
        base_title = extract_base_title(filename)
        files_by_title[base_title].append(file_info)
    
    print(f"{Colors.CYAN}🎮 Processing {len(files_by_title)} unique game titles...{Colors.END}")
    
    for base_title, title_files in files_by_title.items():
        # Check if this title has a version in the primary language
        has_primary_language = base_title in primary_language_titles
        
        # Process all files for this title
        title_valid = []
        title_invalid = []
        
        for file_info in title_files:
            filename = file_info['name']
            
            # Skip demos if not included
            if not include_demos and ('(Demo)' in filename or '(demo)' in filename.lower()):
                title_invalid.append((filename, "Demo file excluded", file_info['size']))
                continue
            
            # Extract region
            region = extract_region(filename)
            
            # Check if file matches user's preferences
            matches_language = True
            matches_region = True
            
            # INTELLIGENT LANGUAGE PRIORITIZATION with SPECIFIC COUNTRY support
            if config['primary_language'] and config['primary_region'] == 'Europe':
                # If specific country is selected, only include files from that country
                if config.get('specific_country'):
                    # Check if file matches the specific country
                    country_patterns = {
                        'Spain': [r'Spain', r'\(Es\)'],
                        'France': [r'France', r'\(Fr\)'],
                        'Germany': [r'Germany', r'\(De\)'],
                        'Italy': [r'Italy', r'\(It\)'],
                        'UK': [r'UK', r'United Kingdom'],
                        'Netherlands': [r'Netherlands', r'\(Nl\)'],
                        'Europe (Multi)': [r'\(Europe\)', r'\([A-Z][a-z](?:,[A-Z][a-z])+\).*Europe']
                    }
                    
                    specific_patterns = country_patterns.get(config['specific_country'], [])
                    matches_specific_country = any(re.search(pattern, filename, re.IGNORECASE) for pattern in specific_patterns)
                    
                    # Special case for Spain: also allow Europe files with Spanish language
                    matches_europe_with_spanish = False
                    if config['specific_country'] == 'Spain':
                        matches_europe_with_spanish = (
                            re.search(r'\(Europe\)', filename, re.IGNORECASE) and 
                            re.search(r'\([^)]*Es[^)]*\)', filename, re.IGNORECASE)
                        )
                    
                    if not matches_specific_country and not matches_europe_with_spanish:
                        title_invalid.append((filename, f"Not from selected country: {config['specific_country']}", file_info['size']))
                        continue
                else:
                    # If there's a primary language version and this isn't it, skip other versions
                    if has_primary_language:
                        is_primary_lang = False
                        if config['primary_language'] == 'Es':
                            is_primary_lang = ('Spain' in filename or 
                                            re.search(r'\(Es\)', filename) or 
                                            re.search(r'\([^)]*Es[^)]*\)', filename))
                        else:
                            lang_patterns = [
                                fr'\({config["primary_language"]}\)',
                                fr'\([^)]*{config["primary_language"]}[^)]*\)',
                            ]
                            is_primary_lang = any(re.search(pattern, filename, re.IGNORECASE) for pattern in lang_patterns)
                        
                        if not is_primary_lang:
                            # This is not the primary language version but primary language exists, skip it
                            title_invalid.append((filename, f"Primary language version available - skipping {region}", file_info['size']))
                            continue
            
            # Check language preference
            if config['primary_language']:
                # Determine if this file has the preferred language
                if config['primary_language'] == 'Es':
                    # Check specifically for Spanish
                    lang_patterns = [
                        r'\(Es\)',
                        r'\([^)]*Es[^)]*\)',
                        r'Spain'
                    ]
                else:
                    # For other languages
                    lang_patterns = [
                        fr'\({config["primary_language"]}\)',
                        fr'\([^)]*{config["primary_language"]}[^)]*\)',
                    ]
                
                matches_language = any(re.search(pattern, filename, re.IGNORECASE) for pattern in lang_patterns)
            
            # Check region preference with intelligent language filtering
            if config['primary_region']:
                # Create patterns for the selected continent
                continent_patterns = {
                    'Europe': [r'\(Europe\)', r'\(.*Europe.*\)', r'Spain', r'France', r'Germany', r'Italy', r'UK', r'Netherlands', r'Poland', r'Russia', r'Scandinavia'],
                    'Americas': [r'\(USA\)', r'\(.*USA.*\)', r'Brazil', r'America'],
                    'Asia': [r'\(Asia\)', r'\(.*Asia.*\)', r'Japan', r'China', r'Korea'],
                    'Oceania': [r'\(Australia\)', r'\(.*Australia.*\)', r'Oceania'],
                    'World': [r'\(World\)', r'\(.*World.*\)', r'Global']
                }
                
                # Check if file matches the selected continent
                patterns = continent_patterns.get(config['primary_region'], [])
                matches_region = any(re.search(pattern, filename, re.IGNORECASE) for pattern in patterns)            # INTELLIGENT FILTERING: For continental regions with language preference
            continental_regions = ['Europe', 'Asia', 'Americas', 'Oceania']
            if (config['primary_region'] in continental_regions and 
                config['primary_language'] and 
                matches_region):
                
                # For continental releases, verify they include our preferred language
                # Look for pattern like (En,Es,Fr,De) or (Es,En)
                multi_lang_pattern = r'\([A-Z][a-z](?:,[A-Z][a-z])+\)'
                multi_lang_match = re.search(multi_lang_pattern, filename)
                
                if multi_lang_match:
                    # Found multi-language indicator, check if our language is included
                    languages_in_file = multi_lang_match.group(0)
                    if config['primary_language'] not in languages_in_file:
                        matches_region = False
                        invalid.append((filename, f"{config['primary_region']} region missing {config['primary_language']} language support", file_info['size']))
                        continue
            
            # Determine priority score with INTELLIGENT PRIORITIZATION
            priority_score = 1000  # Default low priority
            
            # HIGHEST PRIORITY: Exact language match (e.g., Spain for Spanish)
            if config['primary_language'] == 'Es' and 'Spain' in filename:
                priority_score = 1  # Absolute highest priority for Spain
            elif config['primary_language'] == 'Es' and re.search(r'\(Europe\)', filename, re.IGNORECASE) and matches_language:
                priority_score = 2  # Europe files with Spanish language
            elif matches_language and matches_region:
                if config['primary_language'] == 'Es':
                    priority_score = 2  # Other Spanish files in Europe
                else:
                    priority_score = 1  # Perfect match for non-Spanish
            elif matches_language:
                priority_score = 3  # Language match only
            elif matches_region:
                # Only include regional matches if no language preference or no language version exists
                if not config['primary_language']:
                    priority_score = 4  # Regional match without language preference
                else:
                    # Skip regional-only matches when language preference exists
                    title_invalid.append((filename, f"Region match but missing preferred language {config['primary_language']}", file_info['size']))
                    continue
            elif not config['primary_language'] and not config['primary_region']:
                priority_score = 5  # Include all if no preferences
            else:
                # Does not match any criteria
                title_invalid.append((filename, "Does not match preferences", file_info['size']))
                continue
            
            # Add to title's valid files with priority
            file_with_priority = {
                **file_info,
                'region': region or 'Unknown',
                'priority': priority_score,
                'matches_language': matches_language,
                'matches_region': matches_region
            }
            
            if priority_score <= 100:  # Only include reasonably prioritized files
                title_valid.append(file_with_priority)
            else:
                title_invalid.append((filename, "Does not match preferences", file_info['size']))
        
        # Add all files for this title to the final lists
        # If we have valid files for this title, add them all (including all discs)
        if title_valid:
            # Sort by disc number to maintain order
            title_valid.sort(key=lambda x: extract_disc_info(x['name']) or 0)
            valid.extend(title_valid)
            
            # Show what we're keeping for multi-disc games
            disc_info = []
            for file_info in title_valid:
                disc = extract_disc_info(file_info['name'])
                if disc:
                    disc_info.append(f"Disc {disc}")
            
            if len(disc_info) > 1:
                print(f"  🎮 {base_title}: Keeping all {len(disc_info)} discs ({', '.join(disc_info)})")
        
        # Add invalid files to the final invalid list
        invalid.extend(title_invalid)
    
    return valid, invalid

def show_preview_with_priorities(url, config, valid, invalid, include_demos):
    """Shows preview with priority-based organization"""
    print(f"\n{Colors.BOLD}{'='*100}{Colors.END}")
    print(f"{Colors.BOLD}🔍 DOWNLOAD PREVIEW{Colors.END}")
    print(f"{'='*100}")
    print(f"📥 URL: {url}")
    print(f"🎯 Configuration: {config['name']}")
    print(f"🎮 Include Demos: {'Yes' if include_demos else 'No'}")
    
    # Group files by priority
    priority_groups = defaultdict(list)
    for file_info in valid:
        priority_groups[file_info['priority']].append(file_info)
    
    total_size = 0
    total_files = 0
    
    print(f"\n{Colors.BOLD}🎯 ARCHIVOS SELECCIONADOS POR PRIORIDAD{Colors.END}")
    print("="*90)
    
    priority_names = {
        0: "EXCLUSIVE GAMES (Region Exclusives)",
        1: "EXACT COUNTRY MATCH (Spain for Spanish)",
        2: "LANGUAGE MATCH (Spanish in Europe)", 
        3: "LANGUAGE ONLY",
        4: "REGION ONLY (Europe without Spanish)",
        5: "ALL FILES (No preferences)"
    }
    
    for priority in sorted(priority_groups.keys()):
        files = priority_groups[priority]
        if not files:
            continue
            
        group_size = sum(f['size'] for f in files)
        total_size += group_size
        total_files += len(files)
        
        print(f"\n📂 PRIORITY {priority} - {priority_names.get(priority, 'OTHER')}: {len(files)} files ({convert_bytes_to_readable(group_size)})")
        print("-" * 80)
        
        # Show first 10 files as examples
        for file_info in files[:10]:
            # Use full filename instead of base title to show disc info
            full_filename = file_info['name']
            # Remove file extension for cleaner display
            if full_filename.endswith('.zip'):
                title = full_filename[:-4]
            else:
                title = full_filename
            size_str = convert_bytes_to_readable(file_info['size'])
            print(f"  {title[:60]:<62} {size_str:>12}")
        
        if len(files) > 10:
            remaining_size = sum(f['size'] for f in files[10:])
            print(f"  ... and {len(files) - 10} more files ({convert_bytes_to_readable(remaining_size)})")
    
    print("\n" + "="*90)
    print(f"📊 TOTAL SUMMARY:")
    print(f"   📁 Total files: {total_files:,}")
    print(f"   💾 Total size: {convert_bytes_to_readable(total_size)}")
    if invalid:
        invalid_size = sum(size for _, _, size in invalid)
        print(f"   ❌ Ignored files: {len(invalid):,} ({convert_bytes_to_readable(invalid_size)})")
    print("="*90)

def download_selected_files(valid_files, output_dir='downloads', max_files=None):
    """Downloads the selected files with progress tracking"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Limit files if max_files is specified
    files_to_download = valid_files[:max_files] if max_files else valid_files
    
    print(f"\n{Colors.GREEN}🚀 STARTING DOWNLOAD TO: {output_path.absolute()}{Colors.END}")
    if max_files and len(valid_files) > max_files:
        print(f"{Colors.YELLOW}📊 Downloading first {max_files} files out of {len(valid_files)} total{Colors.END}")
    print("=" * 80)
    
    total_files = len(files_to_download)
    downloaded = 0
    skipped = 0
    errors = 0
    
    for i, file_info in enumerate(files_to_download, 1):
        filename = file_info['name']
        url = file_info['url']
        file_size = file_info['size']
        priority = file_info['priority']
        
        # Clean filename for filesystem
        safe_filename = filename.replace('/', '_').replace('\\', '_')
        file_path = output_path / safe_filename
        
        print(f"\n{Colors.CYAN}[{i:4d}/{total_files}]{Colors.END} {Colors.YELLOW}Priority {priority}{Colors.END} - {filename[:60]}...")
        
        # Check if file already exists
        if file_path.exists():
            print(f"  {Colors.YELLOW}⏭️  Already exists, skipping{Colors.END}")
            skipped += 1
            continue
        
        try:
            # Download with progress
            print(f"  {Colors.BLUE}⬇️  Downloading {convert_bytes_to_readable(file_size)}...{Colors.END}")
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Get total size from headers
            total_size = int(response.headers.get('content-length', file_size))
            downloaded_size = 0
            start_time = time.time()
            
            # Write file with progress bar
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Calculate progress and speed
                        progress = min(downloaded_size / total_size, 1.0) if total_size > 0 else 0
                        elapsed_time = time.time() - start_time
                        
                        if elapsed_time > 0:
                            speed_bps = downloaded_size / elapsed_time
                            speed_text = f"{convert_bytes_to_readable(speed_bps)}/s"
                        else:
                            speed_text = "-- MB/s"
                        
                        # Progress bar
                        bar_length = 30
                        filled_length = int(bar_length * progress)
                        bar = '█' * filled_length + '░' * (bar_length - filled_length)
                        percent = progress * 100
                        
                        # Clear line and print progress with speed
                        print(f"\r  {Colors.CYAN}📊 [{bar}] {percent:5.1f}% ({convert_bytes_to_readable(downloaded_size)}/{convert_bytes_to_readable(total_size)}) @ {speed_text}{Colors.END}", end='', flush=True)
            
            print(f"\n  {Colors.GREEN}✅ Downloaded successfully{Colors.END}")
            downloaded += 1
            
        except requests.exceptions.RequestException as e:
            print(f"  {Colors.RED}❌ Download error: {e}{Colors.END}")
            errors += 1
            
        except Exception as e:
            print(f"  {Colors.RED}❌ Unexpected error: {e}{Colors.END}")
            errors += 1
        
        # Small delay to avoid overwhelming the server
        if i % 10 == 0:  # Only sleep every 10 downloads to be more efficient
            time.sleep(0.5)
    
    # Final summary
    print(f"\n{Colors.BOLD}📊 DOWNLOAD SUMMARY:{Colors.END}")
    print("=" * 50)
    print(f"✅ Downloaded: {Colors.GREEN}{downloaded}{Colors.END}")
    print(f"⏭️  Skipped: {Colors.YELLOW}{skipped}{Colors.END}")
    print(f"❌ Errors: {Colors.RED}{errors}{Colors.END}")
    print(f"📁 Location: {output_path.absolute()}")
    print("=" * 50)
    
    return downloaded, skipped, errors

def main():
    """Main interactive function with dynamic language/region detection"""
    print_banner()
    
    while True:
        # Ask for URL first
        print(f"\n{Colors.BOLD}📥 Enter Myrient URL to analyze:{Colors.END}")
        print(f"{Colors.YELLOW}Example: https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/{Colors.END}")
        url = input(f"{Colors.BOLD}URL: {Colors.END}").strip()
        
        if not url:
            print(f"{Colors.RED}❌ URL cannot be empty{Colors.END}\n")
            continue
        
        if url.lower() == 'exit' or url.lower() == '0':
            print(f"\n{Colors.GREEN}👋 Thanks for using Myrient ROM Manager! Goodbye!{Colors.END}\n")
            sys.exit(0)
        
        # Validate URL
        if not validate_url(url):
            print(f"{Colors.RED}❌ Invalid URL. Must start with http:// or https://{Colors.END}\n")
            continue
        
        # Ask for search mode
        print(f"\n{Colors.BOLD}🔍 SEARCH MODE:{Colors.END}")
        print(f"  {Colors.GREEN}1.{Colors.END} Analyze entire collection (default)")
        print(f"  {Colors.CYAN}2.{Colors.END} Search for specific title")
        
        mode_choice = input(f"\n{Colors.BOLD}Select option (1-2) [default: 1]: {Colors.END}").strip()
        
        if mode_choice == '2':
            # Title-specific search mode
            title_to_search = input(f"\n{Colors.BOLD}Enter game title to search for: {Colors.END}").strip()
            if not title_to_search:
                print(f"{Colors.RED}❌ Title cannot be empty{Colors.END}\n")
                continue
        else:
            title_to_search = None
        
        # Ask for demos
        demos_input = input(f"\n{Colors.BOLD}Include Demo files? (yes/no) [default: no]: {Colors.END}").strip().lower()
        include_demos = demos_input in ['yes', 'y', 'si', 's']
        
        # Fetch directory listing
        files = fetch_directory_listing(url, include_demos)
        if files is None:
            print(f"{Colors.RED}❌ Could not fetch directory listing. Please check the URL.{Colors.END}\n")
            continue
        
        if not files:
            print(f"{Colors.YELLOW}⚠️  No .zip files found in the directory{Colors.END}\n")
            continue
        
        print(f"{Colors.GREEN}✓ Found {len(files)} .zip files{Colors.END}")
        
        # Filter files by title if in specific search mode
        if title_to_search:
            original_count = len(files)
            filtered_files = []
            
            print(f"\n{Colors.CYAN}🔍 Searching for titles containing '{title_to_search}'...{Colors.END}")
            
            for file_info in files:
                filename = file_info['name']
                # Case-insensitive search in the filename
                if title_to_search.lower() in filename.lower():
                    filtered_files.append(file_info)
            
            files = filtered_files
            
            if not files:
                print(f"{Colors.RED}❌ No files found containing '{title_to_search}'{Colors.END}\n")
                continue
            
            print(f"{Colors.GREEN}✓ Found {len(files)} files matching '{title_to_search}' (filtered from {original_count} total){Colors.END}")
            
            # Show found titles for confirmation
            print(f"\n{Colors.BOLD}📋 MATCHING TITLES FOUND:{Colors.END}")
            for i, file_info in enumerate(files[:10], 1):  # Show first 10
                filename = file_info['name'][:-4]  # Remove .zip extension
                size_text = convert_bytes_to_readable(file_info['size'])
                print(f"  {i:2}. {Colors.CYAN}{filename}{Colors.END} ({size_text})")
            
            if len(files) > 10:
                remaining = len(files) - 10
                print(f"  {Colors.YELLOW}... and {remaining} more files{Colors.END}")
            
            # Ask for confirmation
            if not ask_yes_no(f"\nProceed with these {len(files)} matching files?"):
                continue
        
        # Analyze available languages and regions
        analysis = analyze_available_languages_and_regions(files)
        
        # Show available options
        show_available_options(analysis)
        
        # Get user's priority selection
        user_priorities = get_user_priority_selection(analysis, files)
        
        print(f"\n{Colors.BOLD}🎯 SELECTED PRIORITIES:{Colors.END}")
        print(f"  📚 Language: {Colors.CYAN}{user_priorities['language'] or 'All languages'}{Colors.END}")
        print(f"  🌍 Region: {Colors.GREEN}{user_priorities['region'] or 'All regions'}{Colors.END}")
        if user_priorities.get('specific_country'):
            print(f"  🏛️  Specific Country: {Colors.BLUE}{user_priorities['specific_country']}{Colors.END}")
        
        # Create custom config based on user selection
        custom_config = create_custom_config(user_priorities, analysis)
        
        # Analyze files with custom config to get priority games first
        valid, invalid = analyze_files_with_priorities(files, custom_config, include_demos)
        
        # Now detect exclusive games, filtering against priority language games
        exclusive_games = detect_exclusive_games(files, valid)
        selected_exclusives = show_exclusive_games_options(exclusive_games)
        
        # Add selected exclusive games to valid files
        if selected_exclusives:
            print(f"\n{Colors.CYAN}📁 Adding {len(selected_exclusives)} exclusive games...{Colors.END}")
            print(f"{Colors.CYAN}🔍 Using intelligent keyword comparison with priority language...{Colors.END}")
            
            # Create a list of valid game titles and their info for keyword comparison
            valid_titles_info = []
            for v in valid:
                base_title = extract_base_title(v['name'])
                valid_titles_info.append({
                    'title': base_title,
                    'filename': v['name'],
                    'disc': extract_disc_info(v['name'])
                })
            
            added_exclusives = 0
            skipped_duplicates = 0
            keyword_matches = []
            
            for exclusive in selected_exclusives:
                exclusive_title = extract_base_title(exclusive['filename'])
                exclusive_disc = extract_disc_info(exclusive['filename'])
                
                # Check if this exclusive game has similar keywords to any priority game
                valid_titles = [info['title'] for info in valid_titles_info]
                is_similar, similar_title = check_keywords_similarity(exclusive_title, valid_titles, threshold=0.6)
                
                if is_similar:
                    # Found a similar game - this is likely a duplicate
                    keyword_matches.append({
                        'exclusive': exclusive_title,
                        'similar': similar_title,
                        'exclusive_disc': exclusive_disc,
                        'exclusive_filename': exclusive['filename']
                    })
                    skipped_duplicates += 1
                    
                    # Show what was detected
                    exclusive_keywords = ', '.join(extract_key_words(exclusive_title)[:4])
                    similar_keywords = ', '.join(extract_key_words(similar_title)[:4])
                    print(f"  🔍 Similar keywords detected:")
                    print(f"    Exclusive: '{exclusive_title}' → Keywords: {exclusive_keywords}")
                    print(f"    Priority:  '{similar_title}' → Keywords: {similar_keywords}")
                    print(f"    ⏭️  Skipping exclusive (priority language takes precedence)")
                    continue
                
                # Convert exclusive game format to match valid files format
                exclusive_file = {
                    'name': exclusive['filename'],
                    'size': exclusive['size'],
                    'url': f"{url.rstrip('/')}/{exclusive['filename']}",
                    'priority': 0,  # Highest priority for exclusives
                    'matches_language': False,
                    'matches_region': False,
                    'region': 'Exclusive'
                }
                
                # Add to valid files
                valid.insert(0, exclusive_file)  # Insert at beginning for highest priority
                added_exclusives += 1
            
            print(f"\n  ✅ Added {Colors.GREEN}{added_exclusives} unique exclusive games{Colors.END}")
            if skipped_duplicates > 0:
                print(f"  ⏭️  Skipped {Colors.YELLOW}{skipped_duplicates} duplicates{Colors.END} (similar keywords to priority games)")
                
                # Show summary of keyword matches
                if keyword_matches:
                    print(f"\n{Colors.CYAN}🧠 KEYWORD DUPLICATE DETECTION EXAMPLES:{Colors.END}")
                    for i, match in enumerate(keyword_matches[:3]):
                        exclusive_kw = ', '.join(extract_key_words(match['exclusive'])[:3])
                        similar_kw = ', '.join(extract_key_words(match['similar'])[:3])
                        print(f"  • Keywords '{Colors.YELLOW}{exclusive_kw}{Colors.END}' found in both:")
                        print(f"    ❌ Exclusive: {match['exclusive']}")
                        print(f"    ✅ Priority:  {match['similar']} (kept - priority language)")
                    
                    if len(keyword_matches) > 3:
                        print(f"  • ... and {len(keyword_matches) - 3} more keyword matches detected")
        
        if not valid:
            print(f"\n{Colors.YELLOW}⚠️  No files match the selected criteria{Colors.END}")
            print(f"{Colors.YELLOW}Total ignored: {len(invalid)}{Colors.END}\n")
            
            if ask_yes_no("Try with different settings?"):
                continue
            else:
                break
        
        # Show preview
        show_preview_with_priorities(url, custom_config, valid, invalid, include_demos)
        
        # Ask for download confirmation
        if ask_yes_no("Do you want to proceed with the download?"):
            # Ask for test mode
            test_mode = ask_yes_no("Download only first 20 files for testing?")
            max_files = 20 if test_mode else None
            
            # Ask for output directory
            default_output = 'downloads'
            output_input = input(f"\n{Colors.BOLD}Output directory [default: {default_output}]: {Colors.END}").strip()
            output_dir = output_input if output_input else default_output
            
            print(f"\n{Colors.GREEN}📁 Output directory: {output_dir}{Colors.END}")
            
            if test_mode:
                print(f"{Colors.YELLOW}🧪 TEST MODE: Only downloading first 20 files{Colors.END}")
            
            # Start actual download
            downloaded, skipped, errors = download_selected_files(valid, output_dir, max_files)
            
            if downloaded > 0:
                print(f"\n{Colors.GREEN}🎉 Download completed! {downloaded} files downloaded successfully!{Colors.END}")
                
                # Ask if user wants to extract the downloaded files
                if ask_yes_no("\n📦 Do you want to extract the downloaded ZIP files?"):
                    extracted, extract_errors = extract_downloaded_files(output_dir)
                    if extracted > 0:
                        print(f"\n{Colors.GREEN}🎉 Extraction completed! {extracted} files extracted successfully!{Colors.END}")
                        if extract_errors > 0:
                            print(f"{Colors.YELLOW}⚠️  {extract_errors} files had extraction errors{Colors.END}")
                    else:
                        print(f"\n{Colors.YELLOW}⚠️  No files were extracted{Colors.END}")
                else:
                    print(f"\n{Colors.CYAN}💾 Files remain compressed in: {output_dir}{Colors.END}")
            else:
                print(f"\n{Colors.YELLOW}⚠️  No files were downloaded.{Colors.END}")
                
                # Check if there are existing ZIP files to extract
                zip_files = glob.glob(os.path.join(output_dir, "*.zip"))
                if zip_files:
                    print(f"\n{Colors.CYAN}🔍 Found {len(zip_files)} existing ZIP files in {output_dir}{Colors.END}")
                    if ask_yes_no("\n📦 Do you want to extract the existing ZIP files?"):
                        extracted, extract_errors = extract_downloaded_files(output_dir)
                        if extracted > 0:
                            print(f"\n{Colors.GREEN}🎉 Extraction completed! {extracted} files extracted successfully!{Colors.END}")
                            if extract_errors > 0:
                                print(f"{Colors.YELLOW}⚠️  {extract_errors} files had extraction errors{Colors.END}")
                        else:
                            print(f"\n{Colors.YELLOW}⚠️  No files were extracted{Colors.END}")
                    else:
                        print(f"\n{Colors.CYAN}💾 Files remain compressed in: {output_dir}{Colors.END}")
            break
        else:
            print(f"{Colors.YELLOW}❌ Download cancelled{Colors.END}")
            
            if ask_yes_no("Try with different settings?"):
                continue
            else:
                break

def main_old():
    """Main interactive function"""
    print_banner()
    
    while True:
        print_menu()
        
        choice = input(f"{Colors.BOLD}Select an option (0-6): {Colors.END}").strip()
        
        if choice == '0':
            print(f"\n{Colors.GREEN}👋 Thanks for using Myrient ROM Manager! Goodbye!{Colors.END}\n")
            sys.exit(0)
        
        config = get_language_config(choice)
        if not config:
            print(f"{Colors.RED}❌ Invalid option. Please try again.{Colors.END}\n")
            continue
        
        print(f"\n{Colors.GREEN}✅ Selected language: {config['name']}{Colors.END}")
        print(f"{Colors.BLUE}📋 Priority regions: {' > '.join([f'{k}({v})' for k, v in sorted(config['priority'].items(), key=lambda x: x[1])])}{Colors.END}")
        
        # Ask for URL
        print(f"\n{Colors.BOLD}📥 Enter Myrient URL:{Colors.END}")
        print(f"{Colors.YELLOW}Example: https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/{Colors.END}")
        url = input(f"{Colors.BOLD}URL: {Colors.END}").strip()
        
        if not url:
            print(f"{Colors.RED}❌ URL cannot be empty{Colors.END}\n")
            continue
        
        # Validate URL
        if not validate_url(url):
            print(f"{Colors.RED}❌ Invalid URL. Must start with http:// or https://{Colors.END}\n")
            continue
        
        # Ask for demos
        demos_input = input(f"\n{Colors.BOLD}Include Demo files? (yes/no) [default: no]: {Colors.END}").strip().lower()
        include_demos = demos_input in ['yes', 'y', 'si', 's']
        
        # Fetch directory listing
        files = fetch_directory_listing(url, include_demos)
        if files is None:
            print(f"{Colors.RED}❌ Could not fetch directory listing. Please check the URL.{Colors.END}\n")
            continue
        
        if not files:
            print(f"{Colors.YELLOW}⚠️  No .zip files found in the directory{Colors.END}\n")
            continue
        
        print(f"{Colors.GREEN}✓ Found {len(files)} .zip files{Colors.END}")
        
        # Analyze files
        valid, invalid = analyze_files(files, config, include_demos)
        
        if not valid:
            print(f"\n{Colors.YELLOW}⚠️  No files match the selected language criteria{Colors.END}")
            print(f"{Colors.YELLOW}Total ignored: {len(invalid)}{Colors.END}\n")
            
            retry = input(f"{Colors.BOLD}Try with different settings? (yes/no): {Colors.END}").strip().lower()
            if retry in ['yes', 'y', 'si', 's']:
                continue  # Go back to main menu
            else:
                print(f"\n{Colors.YELLOW}� Tip: Try a different language configuration or a different platform URL{Colors.END}")
                continue  # Go back to main menu instead of exiting
        
        # Group by title and select best files
        titles_dict = group_by_title(valid)
        selected, discarded = select_best_files(titles_dict, config)
        
        # Print preview
        print(f"\n{Colors.CYAN}{'='*100}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}🔍 DOWNLOAD PREVIEW{Colors.END}")
        print(f"{Colors.CYAN}{'='*100}{Colors.END}")
        print(f"{Colors.BLUE}📥 URL: {url}{Colors.END}")
        print(f"{Colors.BLUE}🌍 Language: {config['name']}{Colors.END}")
        print(f"{Colors.BLUE}🎮 Include Demos: {'Yes' if include_demos else 'No'}{Colors.END}")
        
        print_preview_table(selected, discarded, invalid, config)
        
        # Ask for confirmation
        if not ask_confirmation():
            print(f"\n{Colors.YELLOW}❌ Download cancelled{Colors.END}\n")
            
            retry = input(f"{Colors.BOLD}Try with different settings? (yes/no): {Colors.END}").strip().lower()
            if retry in ['yes', 'y', 'si', 's']:
                continue  # Go back to main menu
            else:
                print(f"\n{Colors.YELLOW}� Returning to main menu...{Colors.END}")
                continue  # Go back to main menu instead of exiting
        
        # Ask for output directory
        default_output = 'myrient_roms'
        output_input = input(f"\n{Colors.BOLD}Output directory [default: {default_output}]: {Colors.END}").strip()
        output_dir = output_input if output_input else default_output
        
        print(f"\n{Colors.GREEN}📁 Output directory: {output_dir}{Colors.END}")
        
        # Note: Here we would need to modify download_and_filter to accept custom config
        # For now, show message
        print(f"\n{Colors.YELLOW}⚠️  Note: Download functionality needs to be updated to support custom language priorities{Colors.END}")
        print(f"{Colors.YELLOW}    For now, use the original downloadroms.py with Spain priority{Colors.END}\n")
        
        another = input(f"{Colors.BOLD}Analyze another URL? (yes/no): {Colors.END}").strip().lower()
        if another not in ['yes', 'y', 'si', 's']:
            print(f"\n{Colors.GREEN}👋 Thanks for using Myrient ROM Manager! Goodbye!{Colors.END}\n")
            sys.exit(0)

def validate_url(url):
    """Validates that the URL is correct"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Program interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
        sys.exit(0)
