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

# Import functions from downloadroms.py and modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from downloadroms import (
    extract_base_title,
    extract_region,
    get_priority,
    is_valid_region,
    has_spanish_language,
    download_and_filter
)

# Import from modules
from modules.filters import (
    is_demo_or_variant,
    has_language_in_file,
    is_valid_region_for_config,
    extract_key_words,
    extract_disc_info,
    get_priority_language_from_config,
    check_keywords_similarity
)
from modules.display import (
    Colors,
    print_banner,
    print_menu,
    convert_bytes_to_readable,
    print_preview_table,
    show_available_options,
    show_exclusive_games_options,
    ask_confirmation,
    ask_yes_no,
    print_progress
)
from modules.config import (
    get_language_config,
    create_custom_config,
    get_all_available_configs
)
from modules.extractor import extract_downloaded_files


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_development_mode():
    """Check if running from source code (development) or compiled executable"""
    # PyInstaller sets sys.frozen attribute when compiled
    return not getattr(sys, 'frozen', False)


# ============================================================================
# FILE EXTRACTION AND PROCESSING (Legacy wrapper)
# ============================================================================

def extract_downloaded_files_legacy(output_dir, delete_zips_after=False):
    """Extract all ZIP files in the output directory
    
    Args:
        output_dir: Directory containing ZIP files
        delete_zips_after: If True, deletes each ZIP immediately after successful extraction
    """
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"\n{Colors.CYAN}📦 STARTING FILE EXTRACTION{Colors.END}")
    print("=" * 60)
    
    zip_files = list(Path(output_dir).glob("*.zip"))
    
    if not zip_files:
        print(f"{Colors.YELLOW}⚠️  No ZIP files found to extract{Colors.END}")
        return 0, 0, 0
    
    extracted_count = 0
    error_count = 0
    deleted_count = 0
    total_freed_space = 0
    
    for zip_file in zip_files:
        try:
            print(f"\n📦 Extracting: {Colors.CYAN}{zip_file.name}{Colors.END}")
            zip_size = zip_file.stat().st_size
            
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
                
                # Delete ZIP immediately after successful extraction if requested
                if delete_zips_after:
                    try:
                        zip_file.unlink()
                        deleted_count += 1
                        total_freed_space += zip_size
                        print(f"  🗑️  Deleted ZIP file (freed {convert_bytes_to_readable(zip_size)})")
                    except Exception as e:
                        print(f"  ⚠️  {Colors.YELLOW}Warning: Could not delete ZIP: {str(e)}{Colors.END}")
                
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
    if delete_zips_after and deleted_count > 0:
        print(f"🗑️  Deleted ZIPs: {Colors.YELLOW}{deleted_count}{Colors.END}")
        print(f"💾 Space freed: {Colors.GREEN}{convert_bytes_to_readable(total_freed_space)}{Colors.END}")
    print(f"📁 Location: {Colors.CYAN}{output_dir}{Colors.END}")
    
    return extracted_count, error_count, deleted_count

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
                
                # Include or exclude demos/variants (check both original and decoded)
                if not include_demos and (is_demo_or_variant(href) or is_demo_or_variant(decoded_name)):
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
    Returns detailed statistics for user selection, including languages per region
    """
    print(f"\n{Colors.CYAN}🔍 Analyzing {len(files)} files to detect available languages and regions...{Colors.END}")
    
    # Language patterns (by language codes)
    language_stats = defaultdict(int)
    region_stats = defaultdict(int)
    language_examples = defaultdict(list)
    region_examples = defaultdict(list)
    
    # NEW: Track languages per region
    languages_by_region = defaultdict(lambda: defaultdict(int))
    
    # Define language patterns to detect - ALL possible language codes
    language_full_names = {
        'Es': 'Spanish (Spain) 🇪🇸',
        'En': 'English 🇬🇧🇺🇸',
        'Fr': 'French (France) 🇫🇷',
        'De': 'German (Germany) 🇩🇪',
        'It': 'Italian (Italy) 🇮🇹',
        'Jp': 'Japanese (Japan) 🇯🇵',
        'Pt': 'Portuguese (Portugal/Brazil) 🇵🇹🇧🇷',
        'Nl': 'Dutch (Netherlands) 🇳🇱',
        'Ru': 'Russian (Russia) 🇷🇺',
        'Ko': 'Korean (Korea) 🇰🇷',
        'Zh': 'Chinese (China) 🇨🇳',
        'Pl': 'Polish (Poland) 🇵🇱',
        'Sv': 'Swedish (Sweden) 🇸🇪',
        'No': 'Norwegian (Norway) 🇳🇴',
        'Da': 'Danish (Denmark) 🇩🇰',
        'Fi': 'Finnish (Finland) 🇫🇮',
        'Cs': 'Czech (Czech Republic) 🇨🇿',
        'Hu': 'Hungarian (Hungary) 🇭🇺',
        'Ar': 'Arabic 🇸🇦',
        'He': 'Hebrew (Israel) 🇮🇱',
        'Tr': 'Turkish (Turkey) 🇹🇷',
        'El': 'Greek (Greece) 🇬🇷',
        'Ja': 'Japanese (Japan) 🇯🇵'
    }
    
    # Define language patterns to detect (for general stats)
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
    
    # Define SIMPLIFIED geographical regions (continents only) with country mappings
    region_countries = {
        'Europe': [r'\(Europe\)', r'\(Spain\)', r'\(France\)', r'\(Germany\)', r'\(Italy\)', r'\(UK\)', r'\(Netherlands\)', r'\(Poland\)', r'\(Russia\)', r'\(Scandinavia\)'],
        'USA': [r'\(USA\)', r'\(U\)', r'\(Brazil\)', r'\(America\)'],
        'Asia': [r'\(Japan\)', r'\(China\)', r'\(Korea\)', r'\(Asia\)'],
        'Oceania': [r'\(Australia\)', r'\(Oceania\)'],
        'World': [r'\(World\)']
    }
    
    for file_info in files:
        filename = file_info['name']
        
        # Count languages (general)
        for language_code, patterns in language_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    language_stats[language_code] += 1
                    if len(language_examples[language_code]) < 3:
                        language_examples[language_code].append(filename)
                    break
        
        # Count geographical regions and detect languages per region
        for region, patterns in region_countries.items():
            if any(re.search(pattern, filename, re.IGNORECASE) for pattern in patterns):
                region_stats[region] += 1
                if len(region_examples[region]) < 3:
                    region_examples[region].append(filename)
                
                # Extract language codes from parentheses only (after region info)
                # Pattern: Find content inside parentheses that contains language codes
                # Example: (USA) (En,Es,Fr) or (Europe) (En) or (Japan)
                paren_contents = re.findall(r'\(([^)]+)\)', filename)
                for content in paren_contents:
                    # Split by comma to get individual language codes
                    potential_langs = re.split(r'[,\s]+', content.strip())
                    for lang_code in potential_langs:
                        # Only accept if it's a valid 2-letter code in our dictionary
                        if lang_code in language_full_names:
                            languages_by_region[region][lang_code] += 1
    
    return {
        'languages': dict(language_stats),
        'regions': dict(region_stats),
        'language_examples': dict(language_examples),
        'region_examples': dict(region_examples),
        'languages_by_region': dict(languages_by_region),  # NEW: Pre-analyzed languages per region
        'language_full_names': language_full_names,  # NEW: Full names dictionary
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
    
    # FILTER: Only keep Japan and Korea exclusives
    filtered_exclusive_games = {}
    allowed_countries = ['Japan', 'Korea']
    
    for country in allowed_countries:
        if country in exclusive_games and exclusive_games[country]:
            filtered_exclusive_games[country] = exclusive_games[country]
    
    # Show what was filtered out
    excluded_countries = [c for c in exclusive_games.keys() if c not in allowed_countries]
    if excluded_countries:
        excluded_count = sum(len(exclusive_games[c]) for c in excluded_countries)
        print(f"{Colors.YELLOW}ℹ️  Filtered out {excluded_count} exclusive games from other regions: {', '.join(excluded_countries)}{Colors.END}")
        print(f"{Colors.CYAN}📌 Only showing Japan and Korea exclusives{Colors.END}")
    
    print(f"{Colors.GREEN}📊 Final exclusive games by country:{Colors.END}")
    for country, games in sorted(filtered_exclusive_games.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {country}: {len(games)} unique games")
    
    return dict(filtered_exclusive_games)


# ============================================================================
# EXCLUSIVE GAMES AND USER SELECTION
# ============================================================================

def show_exclusive_games_options(exclusive_games):
    """Shows available exclusive games by country and asks user for selection"""
    if not exclusive_games:
        print(f"{Colors.YELLOW}🤷 No exclusive games detected{Colors.END}")
        return []
    
    os.system('clear' if os.name != 'nt' else 'cls')
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
        'Zh': 'Chinese (China)',
        'Pl': 'Polish (Poland)',
        'Sv': 'Swedish (Sweden)',
        'No': 'Norwegian (Norway)',
        'Da': 'Danish (Denmark)',
        'Fi': 'Finnish (Finland)',
        'Ja': 'Japanese (Japan)'
    }
    
    # Region code to full name mapping (SIMPLIFIED CONTINENTS)
    region_names = {
        'Europe': 'Europe (Spain, France, Germany, Italy, UK, etc.)',
        'USA': 'USA (United States, Brazil)',
        'Asia': 'Asia (Japan, China, Korea)',
        'Oceania': 'Oceania (Australia)',
        'World': 'World (Global release)'
    }
    
    # Specific countries mapping
    country_names = {
        'Spain': 'Spain 🇪🇸',
        'France': 'France 🇫🇷',
        'Germany': 'Germany 🇩🇪',
        'Italy': 'Italy 🇮🇹',
        'UK': 'United Kingdom 🇬🇧',
        'USA': 'United States 🇺🇸',
        'Japan': 'Japan 🇯🇵',
        'Brazil': 'Brazil 🇧🇷',
        'Netherlands': 'Netherlands 🇳🇱',
        'Australia': 'Australia 🇦🇺',
        'Korea': 'Korea 🇰🇷',
        'China': 'China 🇨🇳',
        'Russia': 'Russia 🇷🇺',
        'Portugal': 'Portugal 🇵🇹'
    }
    
    # Continental regions
    continental_regions = ['Europe', 'USA', 'Asia', 'Oceania', 'World']
    
    # ========================================
    # SHOW ANALYSIS SUMMARY FIRST
    # ========================================
    os.system('clear' if os.name != 'nt' else 'cls')
    print("\n" + "🟦" * 60)
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}📊 ANALYSIS OF AVAILABLE FILES 📊{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
    print("🟦" * 60)
    
    # Show available languages
    if languages:
        print(f"\n{Colors.BOLD}{Colors.GREEN}🌍 AVAILABLE LANGUAGES:{Colors.END}")
        print(f"{Colors.GREEN}{'─' * 60}{Colors.END}")
        lang_list = list(sorted(languages.items(), key=lambda x: x[1], reverse=True))
        for lang_code, count in lang_list[:10]:  # Show top 10
            lang_name = language_names.get(lang_code, lang_code)
            print(f"  • {Colors.CYAN}{lang_code:3s}{Colors.END} - {lang_name:30s} ({count:,} files)")
        
        if len(lang_list) > 10:
            print(f"  {Colors.YELLOW}... and {len(lang_list) - 10} more languages{Colors.END}")
    
    # Show available regions
    if regions:
        print(f"\n{Colors.BOLD}{Colors.BLUE}🗺️  AVAILABLE REGIONS:{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 60}{Colors.END}")
        region_list = list(sorted(regions.items(), key=lambda x: x[1], reverse=True))
        for region, count in region_list:
            region_display = region_names.get(region, region)
            print(f"  • {Colors.BLUE}{region:10s}{Colors.END} - {region_display:40s} ({count:,} files)")
    
    # Detect and show available countries
    print(f"\n{Colors.BOLD}{Colors.YELLOW}🏛️  AVAILABLE SPECIFIC COUNTRIES:{Colors.END}")
    print(f"{Colors.YELLOW}{'─' * 60}{Colors.END}")
    
    available_countries = {}
    country_patterns = {
        'Spain': r'\(Spain\)',
        'France': r'\(France\)',
        'Germany': r'\(Germany\)',
        'Italy': r'\(Italy\)',
        'UK': r'\(UK\)',
        'USA': r'\(USA\)',
        'Japan': r'\(Japan\)',
        'Brazil': r'\(Brazil\)',
        'Netherlands': r'\(Netherlands\)',
        'Australia': r'\(Australia\)',
        'Korea': r'\(Korea\)',
        'China': r'\(China\)',
        'Russia': r'\(Russia\)',
        'Portugal': r'\(Portugal\)'
    }
    
    for file_info in files:
        filename = file_info['name']
        for country, pattern in country_patterns.items():
            if re.search(pattern, filename, re.IGNORECASE):
                available_countries[country] = available_countries.get(country, 0) + 1
    
    if available_countries:
        country_list = list(sorted(available_countries.items(), key=lambda x: x[1], reverse=True))
        for country, count in country_list[:10]:  # Show top 10
            country_display = country_names.get(country, country)
            print(f"  • {country_display:30s} ({count:,} files)")
        
        if len(country_list) > 10:
            print(f"  {Colors.YELLOW}... and {len(country_list) - 10} more countries{Colors.END}")
    else:
        print(f"  {Colors.YELLOW}No specific country tags detected{Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
    print("🟦" * 60)
    
    # Clear separator and highlighted section
    os.system('clear' if os.name != 'nt' else 'cls')
    print("\n" + "🟦" * 60)
    print(f"{Colors.BOLD}{Colors.YELLOW}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.RED}🎯 SELECT YOUR FILTER CRITERIA 🎯{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'=' * 60}{Colors.END}")
    print("🟦" * 60)
    
    selected_language = None
    selected_region = None
    selected_specific_country = None
    selection_mode = None  # 'country', 'region_language', or 'region_only'
    
    # STEP 1: Choose selection mode
    print(f"\n{Colors.BOLD}{Colors.RED}🔻 STEP 1: SELECT FILTER TYPE 🔻{Colors.END}")
    print(f"{Colors.BOLD}Choose how you want to filter ROMs:{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
    print(f"  {Colors.BOLD}1.{Colors.END} {Colors.GREEN}🌍 By specific country{Colors.END} (e.g., Spain → (Spain))")
    print(f"  {Colors.BOLD}2.{Colors.END} {Colors.BLUE}🗺️  By region + language code{Colors.END} (e.g., Europe + Es → (Europe) with Es)")
    print(f"  {Colors.BOLD}3.{Colors.END} {Colors.HEADER}🌎 By region only{Colors.END} (e.g., Europe → (Europe) without languages)")
    print(f"  {Colors.BOLD}0.{Colors.END} {Colors.YELLOW}No filter (include all){Colors.END}")
    print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
    
    while True:
        try:
            choice = input(f"\n{Colors.BOLD}{Colors.GREEN}� Select filter type (0-3): {Colors.END}").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                print(f"✅ No filter - all files will be included")
                selection_mode = None
                break
            elif choice_num == 1:
                selection_mode = 'country'
                print(f"✅ Filter by specific country selected")
                break
            elif choice_num == 2:
                selection_mode = 'region_language'
                print(f"✅ Filter by region + language code selected")
                break
            elif choice_num == 3:
                selection_mode = 'region_only'
                print(f"✅ Filter by region only (no language codes) selected")
                break
            else:
                print(f"{Colors.RED}❌ Invalid choice. Please select 0, 1, 2, or 3{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}❌ Invalid input. Please enter a number{Colors.END}")
    
    # STEP 2: Based on selection mode, ask for specific criteria
    if selection_mode == 'country':
        # Detect available countries from the files
        print(f"\n{Colors.BOLD}{Colors.RED}🔻 STEP 2: SELECT SPECIFIC COUNTRY 🔻{Colors.END}")
        print(f"{Colors.BOLD}Select the country you want:{Colors.END}")
        print(f"{Colors.GREEN}{'─' * 60}{Colors.END}")
        
        # Detect countries from files
        available_countries = {}
        country_patterns = {
            'Spain': r'\(Spain\)',
            'France': r'\(France\)',
            'Germany': r'\(Germany\)',
            'Italy': r'\(Italy\)',
            'UK': r'\(UK\)',
            'USA': r'\(USA\)',
            'Japan': r'\(Japan\)',
            'Brazil': r'\(Brazil\)',
            'Netherlands': r'\(Netherlands\)',
            'Australia': r'\(Australia\)',
            'Korea': r'\(Korea\)',
            'China': r'\(China\)',
            'Russia': r'\(Russia\)',
            'Portugal': r'\(Portugal\)'
        }
        
        for file_info in files:
            filename = file_info['name']
            for country, pattern in country_patterns.items():
                if re.search(pattern, filename, re.IGNORECASE):
                    available_countries[country] = available_countries.get(country, 0) + 1
        
        if available_countries:
            country_list = list(sorted(available_countries.items(), key=lambda x: x[1], reverse=True))
            
            for i, (country, count) in enumerate(country_list, 1):
                country_display = country_names.get(country, country)
                print(f"  {Colors.BOLD}{i}.{Colors.END} {Colors.GREEN}{country_display}{Colors.END} ({count:,} files)")
            
            print(f"{Colors.GREEN}{'─' * 60}{Colors.END}")
            
            while True:
                try:
                    choice = input(f"\n{Colors.BOLD}{Colors.GREEN}👉 Select country (1-{len(country_list)}): {Colors.END}").strip()
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(country_list):
                        selected_specific_country = country_list[choice_num - 1][0]
                        country_display = country_names.get(selected_specific_country, selected_specific_country)
                        print(f"✅ Selected country: {Colors.GREEN}{country_display}{Colors.END}")
                        print(f"   → Will search for files with: {Colors.CYAN}({selected_specific_country}){Colors.END}")
                        break
                    else:
                        print(f"{Colors.RED}❌ Invalid choice. Please select 1-{len(country_list)}{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}❌ Invalid input. Please enter a number{Colors.END}")
        else:
            print(f"{Colors.RED}❌ No specific countries detected in files{Colors.END}")
    
    elif selection_mode == 'region_language':
        # First, select the region
        print(f"\n{Colors.BOLD}{Colors.RED}🔻 STEP 2A: SELECT REGION 🔻{Colors.END}")
        print(f"{Colors.BOLD}Select the continental region:{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 60}{Colors.END}")
        
        region_list = list(sorted(regions.items(), key=lambda x: x[1], reverse=True))
        
        for i, (region, count) in enumerate(region_list, 1):
            region_name = region_names.get(region, region)
            print(f"  {Colors.BOLD}{i}.{Colors.END} {Colors.BLUE}{region} - {region_name}{Colors.END} ({count:,} files)")
        
        print(f"{Colors.BLUE}{'─' * 60}{Colors.END}")
        
        while True:
            try:
                choice = input(f"\n{Colors.BOLD}{Colors.GREEN}👉 Select region (1-{len(region_list)}): {Colors.END}").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(region_list):
                    selected_region = region_list[choice_num - 1][0]
                    region_name = region_names.get(selected_region, selected_region)
                    print(f"✅ Selected region: {Colors.BLUE}{selected_region} - {region_name}{Colors.END}")
                    break
                else:
                    print(f"{Colors.RED}❌ Invalid choice. Please select 1-{len(region_list)}{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Invalid input. Please enter a number{Colors.END}")
        
        # Now, select the language code
        print(f"\n{Colors.BOLD}{Colors.RED}🔻 STEP 2B: SELECT LANGUAGE CODE 🔻{Colors.END}")
        
        # Use pre-analyzed language data from initial analysis
        languages_by_region = analysis.get('languages_by_region', {})
        language_full_names = analysis.get('language_full_names', {})
        
        # Get available languages for the selected region
        available_languages = languages_by_region.get(selected_region, {})
        
        if not available_languages:
            print(f"{Colors.YELLOW}⚠️  No language codes detected in {selected_region} files{Colors.END}")
            print(f"{Colors.YELLOW}   Proceeding without language filter{Colors.END}")
            selected_language = None
        else:
            print(f"{Colors.BOLD}Select the language code to filter within {selected_region}:{Colors.END}")
            print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
            
            # Sort by file count (most common first)
            lang_options = list(sorted(available_languages.items(), key=lambda x: x[1], reverse=True))
            
            for i, (code, count) in enumerate(lang_options, 1):
                name = language_full_names.get(code, code)
                print(f"  {Colors.BOLD}{i}.{Colors.END} {Colors.CYAN}{code} - {name}{Colors.END} ({count:,} files)")
            
            print(f"  {Colors.BOLD}0.{Colors.END} {Colors.YELLOW}No specific language (accept all){Colors.END}")
            print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
            
            while True:
                try:
                    lang_choice = input(f"\n{Colors.BOLD}{Colors.GREEN}👉 Select language code (0-{len(lang_options)}): {Colors.END}").strip()
                    lang_choice_num = int(lang_choice)
                    
                    if lang_choice_num == 0:
                        selected_language = None
                        print(f"✅ No language filter - accepting all languages in {selected_region}")
                        print(f"   → Will search for files with: {Colors.CYAN}({selected_region}){Colors.END}")
                        break
                    elif 1 <= lang_choice_num <= len(lang_options):
                        selected_language = lang_options[lang_choice_num - 1][0]
                        lang_name = language_full_names.get(selected_language, selected_language)
                        print(f"✅ Selected language code: {Colors.CYAN}{selected_language} - {lang_name}{Colors.END}")
                        print(f"   → Will search for files with: {Colors.CYAN}({selected_region}){Colors.END} containing {Colors.CYAN}{selected_language}{Colors.END}")
                        break
                    else:
                        print(f"{Colors.RED}❌ Invalid choice. Please select 0-{len(lang_options)}{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}❌ Invalid input. Please enter a number{Colors.END}")
    
    elif selection_mode == 'region_only':
        # Select region without language codes
        print(f"\n{Colors.BOLD}{Colors.RED}🔻 STEP 2: SELECT REGION 🔻{Colors.END}")
        print(f"{Colors.BOLD}Select the continental region:{Colors.END}")
        print(f"{Colors.HEADER}{'─' * 60}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  This will only include files with ONLY the region tag")
        print(f"   Example: (Europe) → ✅  |  (Europe)(En,Fr,De) → ❌{Colors.END}")
        print(f"{Colors.HEADER}{'─' * 60}{Colors.END}")
        
        region_list = list(sorted(regions.items(), key=lambda x: x[1], reverse=True))
        
        for i, (region, count) in enumerate(region_list, 1):
            region_name = region_names.get(region, region)
            print(f"  {Colors.BOLD}{i}.{Colors.END} {Colors.HEADER}{region} - {region_name}{Colors.END} ({count:,} files)")
        
        print(f"{Colors.HEADER}{'─' * 60}{Colors.END}")
        
        while True:
            try:
                choice = input(f"\n{Colors.BOLD}{Colors.GREEN}👉 Select region (1-{len(region_list)}): {Colors.END}").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(region_list):
                    selected_region = region_list[choice_num - 1][0]
                    region_name = region_names.get(selected_region, selected_region)
                    print(f"✅ Selected region: {Colors.HEADER}{selected_region} - {region_name}{Colors.END}")
                    print(f"   → Will search for files with ONLY: {Colors.HEADER}({selected_region}){Colors.END} (no language codes)")
                    selected_language = None  # No language filtering for region_only mode
                    break
                else:
                    print(f"{Colors.RED}❌ Invalid choice. Please select 1-{len(region_list)}{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Invalid input. Please enter a number{Colors.END}")
    
    return {
        'language': selected_language,
        'region': selected_region,
        'specific_country': selected_specific_country,
        'filter_mode': selection_mode  # Add the selection mode to the config
    }


# ============================================================================
# FILE ANALYSIS AND FILTERING
# ============================================================================

def analyze_files(files, config, include_demos):
    """Analyzes files and categorizes them as valid or invalid"""
    valid = []
    invalid = []
    
    for file_info in files:
        filename = file_info['name']
        
        # Skip demos/variants if not included
        if not include_demos and is_demo_or_variant(filename):
            invalid.append((filename, "Demo/variant file excluded", file_info['size']))
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
    # Check if filter_mode was explicitly set (e.g., 'region_only')
    explicit_filter_mode = user_priorities.get('filter_mode')
    
    if explicit_filter_mode:
        # Use the explicitly provided filter mode
        filter_mode = explicit_filter_mode
        
        # Create appropriate config name based on the mode
        if filter_mode == 'region_only':
            config_name = f"Region Only: {user_priorities['region']} (no language codes)"
        elif filter_mode == 'country':
            config_name = f"Country: {user_priorities['specific_country']}"
        elif filter_mode == 'region_language':
            config_name = f"Region: {user_priorities['region']} (Language: {user_priorities['language']})"
        elif filter_mode == 'language':
            config_name = f"Language: {user_priorities['language']}"
        elif filter_mode == 'region':
            config_name = f"Region: {user_priorities['region']}"
        else:
            config_name = "All files (No filter)"
    else:
        # Legacy behavior: determine mode from priorities
        if user_priorities.get('specific_country'):
            # Country-specific mode
            config_name = f"Country: {user_priorities['specific_country']}"
            filter_mode = 'country'
        elif user_priorities.get('region') and user_priorities.get('language'):
            # Region + language mode
            config_name = f"Region: {user_priorities['region']} (Language: {user_priorities['language']})"
            filter_mode = 'region_language'
        elif user_priorities.get('language'):
            # Language only mode
            config_name = f"Language: {user_priorities['language']}"
            filter_mode = 'language'
        elif user_priorities.get('region'):
            # Region only mode
            config_name = f"Region: {user_priorities['region']}"
            filter_mode = 'region'
        else:
            # No filter mode
            config_name = "All files (No filter)"
            filter_mode = 'none'
    
    return {
        'name': config_name,
        'filter_mode': filter_mode,
        'language': user_priorities.get('language'),
        'region': user_priorities.get('region'),
        'specific_country': user_priorities.get('specific_country'),
        'available_languages': list(analysis['languages'].keys()),
        'available_regions': list(analysis['regions'].keys())
    }

def analyze_files_with_priorities(files, config, include_demos):
    """Analyzes files using direct filter mode (no priorities)"""
    valid = []
    invalid = []
    
    filter_mode = config.get('filter_mode', 'none')
    
    print(f"{Colors.CYAN}🎮 Processing {len(files)} files with filter mode: {filter_mode}...{Colors.END}")
    
    for file_info in files:
        filename = file_info['name']
        
        # Skip demos/variants if not included
        if not include_demos and is_demo_or_variant(filename):
            invalid.append((filename, "Demo/variant file excluded", file_info['size']))
            continue
        
        # Apply filter based on mode
        include_file = False
        reason = ""
        
        if filter_mode == 'none':
            # No filter - include all
            include_file = True
            
        elif filter_mode == 'country':
            # Filter by specific country only
            country = config.get('specific_country')
            country_pattern = fr'\({country}\)'
            
            if re.search(country_pattern, filename, re.IGNORECASE):
                include_file = True
            else:
                reason = f"Not from selected country: {country}"
                
        elif filter_mode == 'region_language':
            # Filter by region + language code
            # When selecting region + language, ONLY match region tags like (Europe), NOT specific countries
            region = config.get('region')
            language = config.get('language')
            
            # For region+language mode, only use the region tag itself
            region_pattern = fr'\({region}\)'
            
            # Check if file has the region tag
            has_region = re.search(region_pattern, filename, re.IGNORECASE)
            
            if has_region:
                if language:
                    # Check if file contains the language code
                    # Pattern for language codes like (Es), (En,Fr,De), etc.
                    lang_in_file = re.search(fr'\b{language}\b', filename, re.IGNORECASE)
                    
                    if lang_in_file:
                        include_file = True
                    else:
                        reason = f"Region {region} found but missing language {language}"
                else:
                    # No language filter, just region
                    include_file = True
            else:
                reason = f"Not from selected region: {region}"
                
        elif filter_mode == 'language':
            # Filter by language only
            language = config.get('language')
            lang_in_file = re.search(fr'\b{language}\b', filename, re.IGNORECASE)
            
            if lang_in_file:
                include_file = True
            else:
                reason = f"Does not contain language: {language}"
                
        elif filter_mode == 'region':
            # Filter by region only
            region = config.get('region')
            
            # Define region to countries mapping
            region_countries = {
                'Europe': [r'\(Europe\)', r'\(Spain\)', r'\(France\)', r'\(Germany\)', r'\(Italy\)', r'\(UK\)', r'\(Netherlands\)', r'\(Poland\)', r'\(Russia\)', r'\(Scandinavia\)'],
                'USA': [r'\(USA\)', r'\(U\)', r'\(Brazil\)', r'\(America\)'],
                'Asia': [r'\(Japan\)', r'\(China\)', r'\(Korea\)', r'\(Asia\)'],
                'Oceania': [r'\(Australia\)', r'\(Oceania\)'],
                'World': [r'\(World\)']
            }
            
            # Get patterns for the selected region
            region_patterns = region_countries.get(region, [fr'\({region}\)'])
            
            # Check if file matches any pattern for this region
            if any(re.search(pattern, filename, re.IGNORECASE) for pattern in region_patterns):
                include_file = True
            else:
                reason = f"Not from selected region: {region}"
        
        elif filter_mode == 'region_only':
            # Filter by region tag only, without language codes
            # This matches files like "007 Racing (Europe).zip" but NOT "007 Racing (Europe)(En,Fr,De).zip"
            region = config.get('region')
            region_pattern = fr'\({region}\)'
            
            # Check if file has the region tag
            has_region = re.search(region_pattern, filename, re.IGNORECASE)
            
            if has_region:
                # Now check that there are NO language codes anywhere in the filename
                # Language codes pattern: (En), (En,Fr,De), (En,Es), etc.
                # Match: opening paren, then 2-letter code(s) with optional commas and spaces, closing paren
                # Examples: (En), (En,Fr), (En, Fr), (En,Es,De), etc.
                lang_pattern = r'\(\s*[A-Z][a-z](?:\s*,\s*[A-Z][a-z])*\s*\)'
                has_language_codes = re.search(lang_pattern, filename)
                
                if not has_language_codes:
                    # File has region but no language codes - perfect!
                    include_file = True
                else:
                    reason = f"Has {region} but also contains language codes (excluded in region-only mode)"
            else:
                reason = f"Not from selected region: {region}"
        
        # Add to appropriate list
        if include_file:
            file_with_info = {
                **file_info,
                'region': extract_region(filename) or 'Unknown'
            }
            valid.append(file_with_info)
        else:
            invalid.append((filename, reason, file_info['size']))
    
    print(f"{Colors.GREEN}✓ {len(valid)} files match the filter{Colors.END}")
    print(f"{Colors.YELLOW}⚠ {len(invalid)} files excluded{Colors.END}")
    
    return valid, invalid

def check_existing_files(files, output_dir):
    """
    Intelligently checks which files already exist in the output directory
    Uses keyword matching to detect same game in different languages/regions
    
    Returns: (new_files, existing_files, similar_files)
    - new_files: list of files that don't exist and have no similar match
    - existing_files: list of files that already exist (exact match)
    - similar_files: list of tuples (file_to_download, existing_file, matching_keywords)
    """
    output_path = Path(output_dir)
    
    # Create directory if it doesn't exist
    if not output_path.exists():
        return files, [], []
    
    # Get all existing ZIP files AND extracted directories in the directory
    existing_items = []
    try:
        # Check for ZIP files
        for existing_file in output_path.glob("*.zip"):
            existing_items.append({
                'name': existing_file.name,
                'path': existing_file,
                'type': 'zip',
                'keywords': extract_key_words(existing_file.name)
            })
        
        # Check for extracted directories (folders with game names)
        for existing_dir in output_path.iterdir():
            if existing_dir.is_dir():
                # Skip common system directories
                if existing_dir.name.startswith('.'):
                    continue
                
                # Add directory to comparison list
                # Treat directory name as if it were a ZIP file for keyword matching
                dir_name_as_zip = f"{existing_dir.name}.zip"
                existing_items.append({
                    'name': existing_dir.name,
                    'path': existing_dir,
                    'type': 'directory',
                    'keywords': extract_key_words(dir_name_as_zip)
                })
    except Exception:
        # If directory doesn't exist or can't be read, return all files as new
        return files, [], []
    
    new_files = []
    existing_files = []
    similar_files = []
    
    for file_info in files:
        filename = file_info['name']
        # Clean filename for filesystem (same logic as in download)
        safe_filename = filename.replace('/', '_').replace('\\', '_')
        file_path = output_path / safe_filename
        
        # Check for exact match first
        if file_path.exists():
            # File already exists with exact same name
            existing_files.append({
                **file_info,
                'path': file_path,
                'match_type': 'exact'
            })
            continue
        
        # Extract keywords from the file to download
        file_keywords = extract_key_words(filename)
        
        # Check for similar files using keyword matching
        best_match = None
        best_match_score = 0
        
        for existing in existing_items:
            # STRICT CHECK 0: Check disc numbers first - different discs are different files!
            # Extract disc information from both filenames
            file_disc = extract_disc_info(filename)
            existing_disc = extract_disc_info(existing['name'])
            
            # If both have disc numbers but they're different, they're different discs of the same game
            if file_disc is not None and existing_disc is not None and file_disc != existing_disc:
                continue  # Skip - different discs (e.g., Disc 1 vs Disc 2)
            
            # Calculate keyword overlap
            matching_keywords = set(file_keywords) & set(existing['keywords'])
            
            # Extract ALL words (including numbers and sport types) from both titles
            file_numbers = [k for k in file_keywords if k.isdigit() or k in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']]
            existing_numbers = [k for k in existing['keywords'] if k.isdigit() or k in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']]
            
            # STRICT CHECK 1: If both have numbers but they're different, it's a different game
            if file_numbers and existing_numbers and set(file_numbers) != set(existing_numbers):
                continue  # Skip - different versions (e.g., Ace Combat 2 vs 3)
            
            # STRICT CHECK 2: If one has numbers and the other doesn't, they're probably different
            if (file_numbers and not existing_numbers) or (not file_numbers and existing_numbers):
                # This catches cases like "Tony Hawk Pro Skater" vs "Tony Hawk Pro Skater 2"
                # The number indicates a sequel/different version
                # Only allow match if keywords are short (<=2 words) - these might be year suffixes
                file_kw_no_numbers = [k for k in file_keywords if not k.isdigit()]
                existing_kw_no_numbers = [k for k in existing['keywords'] if not k.isdigit()]
                
                # If both have 2 or fewer words (excluding numbers), might be annual series
                # Otherwise, the number likely indicates a sequel/version
                if len(file_kw_no_numbers) > 2 or len(existing_kw_no_numbers) > 2:
                    continue  # Skip - likely different versions (e.g., "Game" vs "Game 2")
            
            # Get meaningful matches (excluding generic words)
            meaningful_matches = [k for k in matching_keywords if k not in ['zip', 'rar', '7z']]
            
            # STRICT CHECK 3: Require at least 3 matching keywords OR 2 if they're very specific
            min_keywords = 3
            if len(meaningful_matches) >= 2:
                # Check if we have specific/unique words (longer than 4 chars OR numbers)
                specific_words = [k for k in meaningful_matches if len(k) > 4 or k.isdigit()]
                # Also check if both files have short titles (2-3 keywords total)
                file_kw_count = len([k for k in file_keywords if k not in ['zip', 'rar', '7z']])
                existing_kw_count = len([k for k in existing['keywords'] if k not in ['zip', 'rar', '7z']])
                
                # Allow 2 keywords if:
                # - Both words are specific (long or numbers), OR
                # - Both files have short titles (2-3 keywords) and all match
                if len(specific_words) >= 2 or (file_kw_count <= 3 and existing_kw_count <= 3 and len(meaningful_matches) == file_kw_count):
                    min_keywords = 2  # Allow 2 keywords if they're very specific or complete short title match
            
            if len(meaningful_matches) < min_keywords:
                continue  # Not enough keywords
            
            # STRICT CHECK 4: Check for sport-specific or genre-specific keywords that differ
            # This prevents "All Star Boxing" from matching "All Star Tennis"
            sport_keywords = {'boxing', 'tennis', 'football', 'soccer', 'basketball', 'baseball', 'hockey', 
                            'racing', 'golf', 'cricket', 'rugby', 'volleyball', 'wrestling'}
            
            file_sports = set(file_keywords) & sport_keywords
            existing_sports = set(existing['keywords']) & sport_keywords
            
            # If they have different sports keywords, they're different games
            if file_sports and existing_sports and file_sports != existing_sports:
                continue  # Different sports games
            
            # Calculate match score (percentage of keywords that match)
            # Remove generic file extensions from count
            file_kw_meaningful = [k for k in file_keywords if k not in ['zip', 'rar', '7z']]
            existing_kw_meaningful = [k for k in existing['keywords'] if k not in ['zip', 'rar', '7z']]
            total_keywords = max(len(file_kw_meaningful), len(existing_kw_meaningful))
            
            if total_keywords > 0:
                match_score = len(meaningful_matches) / total_keywords
                
                # STRICT CHECK 5: Require at least 70% match for similar files (increased from 60%)
                if match_score > best_match_score and match_score >= 0.70:
                    best_match_score = match_score
                    best_match = {
                        'existing_file': existing['name'],
                        'existing_path': existing['path'],
                        'existing_type': existing['type'],  # 'zip' or 'directory'
                        'matching_keywords': meaningful_matches,
                        'match_score': match_score
                    }
        
        if best_match:
            # Found a similar file (same game, different region/language)
            similar_files.append({
                **file_info,
                'similar_to': best_match['existing_file'],
                'similar_path': best_match['existing_path'],
                'similar_type': best_match['existing_type'],  # 'zip' or 'directory'
                'matching_keywords': best_match['matching_keywords'],
                'match_score': best_match['match_score']
            })
        else:
            # No match found - this is a new file
            new_files.append(file_info)
    
    return new_files, existing_files, similar_files

def show_preview_with_priorities(url, config, valid, invalid, include_demos):
    """Shows preview of selected files (no priorities, just direct filter results)"""
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"\n{Colors.BOLD}{'='*100}{Colors.END}")
    print(f"{Colors.BOLD}🔍 DOWNLOAD PREVIEW{Colors.END}")
    print(f"{'='*100}")
    print(f"📥 URL: {url}")
    print(f"🎯 Filter: {config['name']}")
    print(f"🎮 Include Demos: {'Yes' if include_demos else 'No'}")
    
    if not valid:
        print(f"\n{Colors.YELLOW}⚠️  No files match the selected criteria{Colors.END}")
        return
    
    total_size = sum(f['size'] for f in valid)
    total_files = len(valid)
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}📁 SELECTED FILES{Colors.END}")
    print(f"{Colors.CYAN}{'='*90}{Colors.END}")
    print(f"{Colors.GREEN}✓ {total_files:,} files selected ({convert_bytes_to_readable(total_size)}){Colors.END}")
    print(f"{Colors.CYAN}{'-' * 90}{Colors.END}")
    
    # Show first 10 files as examples
    for file_info in valid[:10]:
        # Use full filename instead of base title to show disc info
        full_filename = file_info['name']
        # Remove file extension for cleaner display
        if full_filename.endswith('.zip'):
            title = full_filename[:-4]
        else:
            title = full_filename
        size_str = convert_bytes_to_readable(file_info['size'])
        print(f"  {title[:60]:<62} {size_str:>12}")
    
    if len(valid) > 10:
        remaining_size = sum(f['size'] for f in valid[10:])
        print(f"  {Colors.CYAN}... and {len(valid) - 10:,} more files ({convert_bytes_to_readable(remaining_size)}){Colors.END}")
    
    print(f"{Colors.CYAN}{'='*90}{Colors.END}")
    print(f"{Colors.BOLD}📊 SUMMARY:{Colors.END}")
    print(f"   📁 Total files to download: {total_files:,}")
    print(f"   💾 Total size: {convert_bytes_to_readable(total_size)}")
    
    if invalid:
        invalid_size = sum(size for _, _, size in invalid)
        print(f"   ❌ Excluded files: {len(invalid):,} ({convert_bytes_to_readable(invalid_size)})")
    
    print(f"{Colors.CYAN}{'='*90}{Colors.END}")

def download_selected_files(valid_files, output_dir='downloads', max_files=None):
    """Downloads the selected files with progress tracking"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Limit files if max_files is specified
    files_to_download = valid_files[:max_files] if max_files else valid_files
    
    os.system('clear' if os.name != 'nt' else 'cls')
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
        
        # Clean filename for filesystem
        safe_filename = filename.replace('/', '_').replace('\\', '_')
        file_path = output_path / safe_filename
        
        print(f"\n{Colors.CYAN}[{i:4d}/{total_files}]{Colors.END} {filename[:70]}...")
        
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
        
        # Ask for output directory BEFORE showing preview (to check existing files)
        default_output = 'downloads'
        print(f"\n{Colors.BOLD}📁 Output directory configuration:{Colors.END}")
        output_input = input(f"{Colors.BOLD}Enter output directory [default: {default_output}]: {Colors.END}").strip()
        output_dir = output_input if output_input else default_output
        
        # Check for existing files in the output directory
        print(f"\n{Colors.CYAN}🔍 Analyzing existing files in '{output_dir}' using intelligent keyword matching...{Colors.END}")
        new_files, existing_files, similar_files = check_existing_files(valid, output_dir)
        
        # Show information about existing files
        total_existing = len(existing_files) + len(similar_files)
        
        if existing_files:
            existing_size = sum(f['size'] for f in existing_files)
            print(f"\n{Colors.GREEN}📦 Found {len(existing_files)} exact matches ({convert_bytes_to_readable(existing_size)}){Colors.END}")
        
        # Show similar files (same game, different region/language)
        if similar_files:
            similar_size = sum(f['size'] for f in similar_files)
            print(f"\n{Colors.YELLOW}🔍 Found {len(similar_files)} similar games (same game, different region/language){Colors.END}")
            print(f"{Colors.YELLOW}   Total size: {convert_bytes_to_readable(similar_size)}{Colors.END}")
            
            # Show examples of similar files
            print(f"\n{Colors.CYAN}🧠 KEYWORD MATCHING EXAMPLES:{Colors.END}")
            for i, similar in enumerate(similar_files[:5], 1):
                keywords = ', '.join(similar['matching_keywords'][:4])
                match_percent = int(similar['match_score'] * 100)
                similar_type = similar.get('similar_type', 'zip')
                type_icon = '📦' if similar_type == 'zip' else '📁'
                type_label = 'ZIP' if similar_type == 'zip' else 'Extracted'
                
                print(f"\n  {i}. {Colors.BOLD}Match: {match_percent}%{Colors.END} | Keywords: {Colors.YELLOW}{keywords}{Colors.END}")
                print(f"     📥 To download: {Colors.CYAN}{similar['name']}{Colors.END}")
                print(f"     {type_icon} Already have: {Colors.GREEN}{similar['similar_to']}{Colors.END} ({type_label})")
            
            if len(similar_files) > 5:
                print(f"\n  ... and {len(similar_files) - 5} more similar matches")
        
        # Ask user what to do if there are existing or similar files
        files_to_download = new_files  # Default: only truly new files
        
        if total_existing > 0:
            print(f"\n{Colors.BOLD}What do you want to do?{Colors.END}")
            print(f"  1. {Colors.GREEN}Skip all existing/similar files{Colors.END} (download only {len(new_files)} new games)")
            print(f"  2. {Colors.YELLOW}Download similar files anyway{Colors.END} (different regions/languages)")
            print(f"  3. {Colors.RED}Re-download everything{Colors.END} (overwrite all)")
            
            while True:
                choice = input(f"\n{Colors.BOLD}Select option (1-3) [default: 1]: {Colors.END}").strip()
                if not choice:
                    choice = '1'
                
                if choice == '1':
                    # Skip both exact matches and similar files
                    files_to_download = new_files
                    print(f"\n{Colors.GREEN}✅ Will skip {total_existing} existing/similar files{Colors.END}")
                    print(f"   → Downloading {len(new_files)} truly new games")
                    break
                elif choice == '2':
                    # Skip exact matches but download similar files
                    files_to_download = new_files + similar_files
                    print(f"\n{Colors.YELLOW}⚠️  Will skip {len(existing_files)} exact matches but download {len(similar_files)} similar files{Colors.END}")
                    print(f"   → Downloading {len(files_to_download)} games total")
                    break
                elif choice == '3':
                    # Re-download everything
                    files_to_download = valid
                    print(f"\n{Colors.RED}⚠️  Will re-download all {len(valid)} files (existing files will be overwritten){Colors.END}")
                    break
                else:
                    print(f"{Colors.RED}Invalid option. Please enter 1, 2, or 3.{Colors.END}")
        else:
            # No existing files, download all
            print(f"\n{Colors.GREEN}✅ No existing files found, all {len(new_files)} files will be downloaded{Colors.END}")
        
        files_to_show = files_to_download
        
        # Show preview with the appropriate file list
        show_preview_with_priorities(url, custom_config, files_to_show, invalid, include_demos)
        
        # Show skipped files summary if any were skipped
        skipped_count = len(valid) - len(files_to_show)
        if skipped_count > 0:
            print(f"\n{Colors.CYAN}📋 SKIPPED FILES ({skipped_count} files will not be downloaded):{Colors.END}")
            print(f"{Colors.CYAN}{'─' * 80}{Colors.END}")
            
            # Show exact matches
            if existing_files and len(files_to_show) < len(valid):
                print(f"\n  {Colors.GREEN}Exact matches ({len(existing_files)}):{Colors.END}")
                for i, file_info in enumerate(existing_files[:3], 1):
                    size_text = convert_bytes_to_readable(file_info['size'])
                    print(f"    ⏭️  {file_info['name'][:63]:<65} {size_text:>10}")
                if len(existing_files) > 3:
                    print(f"    ... and {len(existing_files) - 3} more exact matches")
            
            # Show similar files if they're being skipped
            if similar_files and files_to_show == new_files:
                print(f"\n  {Colors.YELLOW}Similar games ({len(similar_files)}):{Colors.END}")
                for i, file_info in enumerate(similar_files[:3], 1):
                    size_text = convert_bytes_to_readable(file_info['size'])
                    keywords = ', '.join(file_info['matching_keywords'][:3])
                    print(f"    🔍 {file_info['name'][:60]:<62} {size_text:>10}")
                    print(f"       → Similar to: {file_info['similar_to'][:70]}")
                    print(f"       → Matching keywords: {Colors.YELLOW}{keywords}{Colors.END}")
                if len(similar_files) > 3:
                    print(f"    ... and {len(similar_files) - 3} more similar matches")
            
            print(f"{Colors.CYAN}{'─' * 80}{Colors.END}")
        
        # Ask for download confirmation
        if ask_yes_no("Do you want to proceed with the download?"):
            # Ask for test mode (only in development mode)
            max_files = None
            if is_development_mode():
                test_mode = ask_yes_no("Download only first 10 files for testing?")
                max_files = 10 if test_mode else None
            else:
                test_mode = False
            
            print(f"\n{Colors.GREEN}📁 Output directory: {output_dir}{Colors.END}")
            
            if test_mode:
                print(f"{Colors.YELLOW}🧪 TEST MODE: Only downloading first 10 files{Colors.END}")
            
            # Start actual download with the appropriate file list
            downloaded, skipped, errors = download_selected_files(files_to_show, output_dir, max_files)
            
            if downloaded > 0:
                print(f"\n{Colors.GREEN}🎉 Download completed! {downloaded} files downloaded successfully!{Colors.END}")
                
                # Ask if user wants to extract the downloaded files
                if ask_yes_no("\n📦 Do you want to extract the downloaded ZIP files?"):
                    # Ask if user wants to delete ZIPs after extraction to save space
                    delete_zips = ask_yes_no("🗑️  Delete ZIP files immediately after extraction to save disk space?")
                    
                    extracted, extract_errors, deleted = extract_downloaded_files(output_dir, delete_zips_after=delete_zips)
                    
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
                        # Ask if user wants to delete ZIPs after extraction to save space
                        delete_zips = ask_yes_no("🗑️  Delete ZIP files immediately after extraction to save disk space?")
                        
                        extracted, extract_errors, deleted = extract_downloaded_files(output_dir, delete_zips_after=delete_zips)
                        
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
