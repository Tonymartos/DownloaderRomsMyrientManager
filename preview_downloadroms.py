#!/usr/bin/env python3
# Copyright (C) 2025 Myrient ROM Manager Contributors
# This file is licensed under the GNU General Public License v3.0
# See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""
Preview script for downloadroms.py
Analyzes the URL without downloading files and shows a table of what will be downloaded
"""

import sys
import re
import requests
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Import functions from downloadroms.py in the same directory
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from downloadroms import (
    extract_base_title,
    extract_region,
    get_priority,
    is_valid_region,
    has_spanish_language,
    validate_url
)

class Colors:
    """Terminal colors"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def fetch_directory_listing(url, include_demos=False):
    """
    Gets the file listing from a URL
    """
    print(f"\n🔍 Analyzing URL: {url}")
    print("⏳ Getting file listing...\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for all links
        links = soup.find_all('a', href=True)
        
        files = []
        for link in links:
            href = link['href']
            filename = link.get_text().strip()
            
            # Only .zip files
            if not filename.endswith('.zip'):
                continue
            
            # Build complete URL
            file_url = urljoin(url, href)
            
            # Get size if available
            size = "N/A"
            parent = link.parent
            if parent and parent.name == 'td':
                size_td = parent.find_next_sibling('td')
                if size_td:
                    size_text = size_td.get_text().strip()
                    if size_text and size_text != '-':
                        size = size_text
            
            files.append({
                'name': filename,
                'url': file_url,
                'size': size
            })
        
        return files
    
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}❌ Error getting file listing: {e}{Colors.ENDC}")
        return []

def analyze_files(files, include_demos=False):
    """
    Analyzes files and classifies them
    """
    valid_files = []
    invalid_files = []
    
    for file_info in files:
        filename = file_info['name']
        
        # Validate region
        if is_valid_region(filename):
            region = extract_region(filename)
            base_title = extract_base_title(filename)
            priority = get_priority(region)
            has_spanish = has_spanish_language(filename)
            
            valid_files.append({
                'name': filename,
                'url': file_info['url'],
                'size': file_info['size'],
                'base_title': base_title,
                'region': region,
                'priority': priority,
                'has_spanish': has_spanish
            })
        else:
            reason = "No valid region or Europe without Es"
            if 'France' in filename or 'USA' in filename or 'Germany' in filename or 'Italy' in filename:
                reason = "Individual region (not allowed)"
            elif 'Europe' in filename and not has_spanish_language(filename):
                reason = "Europe without Spanish (Es)"
            
            invalid_files.append({
                'name': filename,
                'reason': reason
            })
    
    return valid_files, invalid_files

def group_by_title(valid_files):
    """
    Groups files by base title
    """
    titles_dict = defaultdict(list)
    
    for file_info in valid_files:
        titles_dict[file_info['base_title']].append(file_info)
    
    return titles_dict

def select_best_files(titles_dict):
    """
    Selects the best files according to priority
    """
    selected = []
    discarded = []
    
    for base_title, files in titles_dict.items():
        # If there's Spain, remove Europe
        has_spain = any(f['region'] == 'Spain' for f in files)
        
        if has_spain:
            files_filtered = [f for f in files if f['region'] != 'Europe']
            discarded.extend([f for f in files if f['region'] == 'Europe'])
        else:
            files_filtered = files
        
        # Select the best by priority
        best_file = min(files_filtered, key=lambda x: x['priority'])
        selected.append(best_file)
        
        # Add discarded
        for f in files_filtered:
            if f != best_file:
                discarded.append(f)
    
    return selected, discarded

def format_size(size_str):
    """Formats size for better readability"""
    if size_str == "N/A" or not size_str:
        return "?"
    
    # If it already has unit (KB, MB, GB)
    if any(unit in size_str.upper() for unit in ['KB', 'MB', 'GB', 'TB']):
        return size_str
    
    # If it's a number, convert bytes
    try:
        size_bytes = float(size_str)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
    except:
        pass
    
    return size_str

def print_table(selected, discarded, invalid):
    """
    Prints a nice table with the results
    """
    print("\n" + "=" * 120)
    print(f"{Colors.BOLD}{Colors.OKGREEN}✅ FILES TO BE DOWNLOADED{Colors.ENDC}")
    print("=" * 120)
    
    if not selected:
        print(f"{Colors.WARNING}⚠️  No valid files found to download{Colors.ENDC}")
    else:
        # Header
        print(f"{Colors.BOLD}{'TITLE':<60} {'REGION':<10} {'SIZE':<12} {'PRIORITY':<10}{Colors.ENDC}")
        print("-" * 120)
        
        # Sort by title
        selected_sorted = sorted(selected, key=lambda x: x['base_title'])
        
        total_count = 0
        for file_info in selected_sorted:
            title = file_info['base_title'][:58]
            region = file_info['region']
            size = format_size(file_info['size'])
            priority = file_info['priority']
            
            region_color = Colors.OKGREEN if region == 'Spain' else Colors.OKCYAN if region == 'Europe' else Colors.OKBLUE
            
            print(f"{title:<60} {region_color}{region:<10}{Colors.ENDC} {size:<12} {priority:<10}")
            total_count += 1
        
        print("-" * 120)
        print(f"{Colors.BOLD}Total files to download: {total_count}{Colors.ENDC}")
    
    # Discarded files
    if discarded:
        print("\n" + "=" * 120)
        print(f"{Colors.BOLD}{Colors.WARNING}⏭️  DISCARDED FILES (duplicates or lower priority){Colors.ENDC}")
        print("=" * 120)
        print(f"{Colors.BOLD}{'FILE':<80} {'REGION':<15} {'REASON':<25}{Colors.ENDC}")
        print("-" * 120)
        
        for file_info in discarded[:20]:  # Show only first 20
            name = file_info['name'][:78]
            region = file_info['region']
            reason = "Lower priority"
            
            print(f"{name:<80} {region:<15} {reason:<25}")
        
        if len(discarded) > 20:
            print(f"\n... and {len(discarded) - 20} more discarded files")
        
        print(f"\n{Colors.BOLD}Total discarded: {len(discarded)}{Colors.ENDC}")
    
    # Invalid files
    if invalid:
        print("\n" + "=" * 120)
        print(f"{Colors.BOLD}{Colors.FAIL}❌ IGNORED FILES (don't meet criteria){Colors.ENDC}")
        print("=" * 120)
        print(f"{Colors.BOLD}{'FILE':<80} {'REASON':<40}{Colors.ENDC}")
        print("-" * 120)
        
        for file_info in invalid[:20]:  # Show only first 20
            name = file_info['name'][:78]
            reason = file_info['reason'][:38]
            
            print(f"{name:<80} {reason:<40}")
        
        if len(invalid) > 20:
            print(f"\n... and {len(invalid) - 20} more ignored files")
        
        print(f"\n{Colors.BOLD}Total ignored: {len(invalid)}{Colors.ENDC}")

def print_summary(selected, discarded, invalid):
    """
    Prints statistics summary
    """
    print("\n" + "=" * 120)
    print(f"{Colors.BOLD}📊 ANALYSIS SUMMARY{Colors.ENDC}")
    print("=" * 120)
    
    total = len(selected) + len(discarded) + len(invalid)
    
    print(f"📁 Total .zip files found: {Colors.BOLD}{total}{Colors.ENDC}")
    print(f"✅ Files to download: {Colors.OKGREEN}{Colors.BOLD}{len(selected)}{Colors.ENDC}")
    print(f"⏭️  Files discarded: {Colors.WARNING}{len(discarded)}{Colors.ENDC}")
    print(f"❌ Files ignored: {Colors.FAIL}{len(invalid)}{Colors.ENDC}")
    
    # Breakdown by regions in selected files
    if selected:
        regions = defaultdict(int)
        for f in selected:
            regions[f['region']] += 1
        
        print(f"\n📊 Breakdown by regions:")
        for region, count in sorted(regions.items(), key=lambda x: x[1], reverse=True):
            region_color = Colors.OKGREEN if region == 'Spain' else Colors.OKCYAN if region == 'Europe' else Colors.OKBLUE
            print(f"   {region_color}● {region}: {count}{Colors.ENDC}")

def ask_confirmation():
    """
    Asks user for confirmation
    """
    print("\n" + "=" * 120)
    response = input(f"{Colors.BOLD}Do you want to proceed with the download? (y/N): {Colors.ENDC}").strip().lower()
    return response in ['s', 'si', 'yes', 'y']

def main():
    """
    Main function
    """
    if len(sys.argv) < 2:
        print("=" * 120)
        print(f"{Colors.BOLD}🔍 DOWNLOAD PREVIEW - DOWNLOADROMS{Colors.ENDC}")
        print("=" * 120)
        print("\nUsage: python preview_downloadroms.py <URL> [options]")
        print("\nOptions:")
        print("  --demos      Include Demo files")
        print("\nExamples:")
        print("  python preview_downloadroms.py 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/'")
        print("  python preview_downloadroms.py 'https://example.com/roms/' --demos")
        print("\nThis script:")
        print("  ✓ Analyzes URL without downloading")
        print("  ✓ Shows which files would be downloaded")
        print("  ✓ Applies the same rules as downloadroms.py")
        print("  ✓ Asks for confirmation before proceeding")
        print("=" * 120)
        sys.exit(1)
    
    url = sys.argv[1]
    include_demos = '--demos' in sys.argv
    
    # Validate URL
    if not validate_url(url):
        print(f"{Colors.FAIL}❌ ERROR: Invalid URL '{url}'{Colors.ENDC}")
        print("URL must start with http:// or https://")
        sys.exit(1)
    
    print("=" * 120)
    print(f"{Colors.BOLD}🔍 DOWNLOAD PREVIEW - DOWNLOADROMS{Colors.ENDC}")
    print("=" * 120)
    print(f"📥 URL: {url}")
    print(f"🎮 Include Demos: {'Yes' if include_demos else 'No'}")
    print(f"🌍 Allowed regions: Spain, Europe (with Es or no languages), Japan")
    print(f"🏆 Priority: Spain > Europe > Japan")
    
    # Get listing
    files = fetch_directory_listing(url, include_demos)
    
    if not files:
        print(f"\n{Colors.FAIL}❌ No .zip files found at URL{Colors.ENDC}")
        sys.exit(1)
    
    print(f"✓ Found {Colors.BOLD}{len(files)}{Colors.ENDC} .zip files")
    
    # Analyze files
    print("\n⚙️  Analyzing files and applying filters...")
    valid_files, invalid_files = analyze_files(files, include_demos)
    
    # Group by title
    titles_dict = group_by_title(valid_files)
    
    # Select best files
    selected, discarded = select_best_files(titles_dict)
    
    # Show tables
    print_table(selected, discarded, invalid_files)
    
    # Show summary
    print_summary(selected, discarded, invalid_files)
    
    # Ask for confirmation
    if selected and ask_confirmation():
        print(f"\n{Colors.OKGREEN}✓ Proceeding to execute downloadroms.py...{Colors.ENDC}")
        
        # Build command
        import subprocess
        cmd = ['python', 'downloadroms.py', url, 'downloads']
        if include_demos:
            cmd.append('--demos')
        
        print(f"\n🚀 Executing: {' '.join(cmd)}\n")
        print("=" * 120)
        
        subprocess.run(cmd)
    else:
        print(f"\n{Colors.WARNING}⚠️  Download cancelled{Colors.ENDC}")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  Process interrupted by user{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
