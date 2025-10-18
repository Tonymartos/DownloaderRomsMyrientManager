"""downloadroms.py - command-line download script (source code)

Copyright (C) 2025 Myrient ROM Manager Contributors
This file is licensed under the GNU General Public License v3.0
See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

REGION_PRIORITY = {
    'Spain': 1,
    'Europe': 2,
    'Japan': 3,
    'Es': 4,
}

def validate_url(url):
    """Validates that the URL is correct"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def extract_base_title(filename):
    match = re.match(r'^(.+?)\s*\([^)]+\)\.[^.]+$', filename)
    return match.group(1).strip() if match else filename

def extract_region(filename):
    """Extracts the region from the filename"""
    # Search for all parenthesis matches
    matches = re.findall(r'\(([^)]+)\)', filename)
    
    for match in matches:
        for key in REGION_PRIORITY:
            if key in match:
                return key
    
    return 'Unknown'

def has_spanish_language(filename):
    """
    Verifies if the Europe file contains Spanish (Es) in languages.
    Example: (Europe) (En,Fr,De,Es,It) → True
    If no languages defined → True (accept Europe without languages)
    """
    # Search for language patterns like (En,Fr,De,Es,It)
    lang_match = re.search(r'\([A-Z][a-z](?:,[A-Z][a-z])+\)', filename)
    if lang_match:
        languages = lang_match.group(0)
        return 'Es' in languages
    # If no languages specified, accept the file
    return True

def is_valid_region(filename):
    """
    Validates that the file only has allowed regions (Spain, Europe, Japan).
    Excludes individual regions like France, Germany, Italy, USA, etc.
    
    For Europe: ONLY accepts if it contains Spanish (Es) in languages.
    Valid example: (Europe) (En,Fr,De,Es,It)
    Invalid example: (Europe) (En,Fr,De)
    """
    # Allowed regions (multi-region)
    allowed_regions = ['Spain', 'Europe', 'Japan']
    
    # NOT allowed regions (individual)
    excluded_regions = [
        'France', 'Germany', 'Italy', 'USA', 'Asia', 'Australia',
        'Brazil', 'China', 'Korea', 'Netherlands', 'Poland', 'Russia',
        'Scandinavia', 'UK', 'World'
    ]
    
    # Search for all regions in filename
    matches = re.findall(r'\(([^)]+)\)', filename)
    
    has_europe = False
    
    for match in matches:
        # If it's Europe, verify it has Spanish
        if 'Europe' in match:
            has_europe = True
            if not has_spanish_language(filename):
                return False
        
        # Check if it contains any excluded region
        for excluded in excluded_regions:
            if excluded in match and not any(allowed in match for allowed in allowed_regions):
                return False
    
    return True

def get_priority(region):
    """Gets the numeric priority of a region"""
    return REGION_PRIORITY.get(region, 999)

def download_and_filter(url, output_dir='downloads', verbose=True, include_demos=False):
    # Validate URL
    if not validate_url(url):
        print(f"\n❌ ERROR: Invalid URL '{url}'")
        print("URL must start with http:// or https://")
        print("Example: https://myrient.erista.me/files/Redump/")
        sys.exit(1)
    
    temp_dir = Path('temp_downloads')
    final_dir = Path(output_dir)
    temp_dir.mkdir(exist_ok=True)
    final_dir.mkdir(exist_ok=True)
    
    print("\n🔽 STARTING DOWNLOAD...")
    print(f"📍 URL: {url}")
    print(f"📂 Temporary directory: {temp_dir}")
    print(f"📂 Final directory: {final_dir}")
    print(f"🎮 Include Demos: {'Yes' if include_demos else 'No'}")
    print("=" * 80)
    
    # Build acceptance filter
    # Only download Spain, Europe, Japan (not individual regions like France, Germany, etc.)
    accept_patterns = '*(Spain)*,*(Europe)*,*(Japan)*'
    
    if include_demos:
        accept_patterns += ',*(Demo)*'
    
    # Download with wget (verbose mode)
    wget_cmd = [
        'wget',
        '-m',           # mirror
        '-np',          # no parent
        '-c',           # continue
        '-v',           # verbose
        '-nH',          # no host directories
        '-e', 'robots=off',
        '--no-http-keep-alive',
        '--waitretry=900',
        '--tries=infinite',
        '--no-if-modified-since',
        '-N',           # timestamping
        '-A', accept_patterns,
        '-P', str(temp_dir),
        '--progress=bar:force',  # show progress bar
        url
    ]
    
    if verbose:
        print("\n📡 Executing wget...")
        print(f"🔧 Command: {' '.join(wget_cmd)}")
        print("-" * 80)
    
    # Execute wget and show output in real-time
    try:
        process = subprocess.Popen(
            wget_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Show output line by line
        for line in process.stdout:
            if verbose:
                print(line.rstrip())
        
        process.wait()
        
        if process.returncode != 0:
            print(f"\n⚠️  wget finished with exit code: {process.returncode}")
    
    except Exception as e:
        print(f"\n❌ Error during download: {e}")
        return
    
    print("\n" + "=" * 80)
    print("🔍 ANALYZING DOWNLOADED FILES...")
    print("=" * 80)
    
    titles_dict = defaultdict(list)
    total_files = 0
    
    # Search for all .zip files
    skipped_files = 0
    for file_path in temp_dir.glob('**/*.zip'):
        total_files += 1
        
        # Validate that it only has allowed regions
        if not is_valid_region(file_path.name):
            skipped_files += 1
            if verbose:
                print(f"  ⏭️  SKIPPED (region not allowed): {file_path.name}")
            continue
        
        base_title = extract_base_title(file_path.name)
        region = extract_region(file_path.name)
        priority = get_priority(region)
        
        titles_dict[base_title].append({
            'path': file_path,
            'region': region,
            'priority': priority
        })
        
        if verbose:
            print(f"  📄 Found: {file_path.name}")
            print(f"     └─ Title: {base_title}")
            print(f"     └─ Region: {region} (Priority: {priority})")
    
    print(f"\n📊 Total files found: {total_files}")
    print(f"📊 Files skipped (regions not allowed): {skipped_files}")
    print(f"📊 Valid files: {total_files - skipped_files}")
    print(f"📊 Total unique titles: {len(titles_dict)}")
    
    if total_files == 0:
        print("\n⚠️  No .zip files found")
        print("Verify that the URL is correct and contains files with the specified regions")
        return
    
    print("\n" + "=" * 80)
    print("🎯 SELECTING BEST VERSIONS...")
    print("=" * 80)
    
    copied_count = 0
    discarded_count = 0
    
    for base_title, files in titles_dict.items():
        # If there's Spain and Europe, remove Europe even if it has Es
        has_spain = any(f['region'] == 'Spain' for f in files)
        
        if has_spain:
            # Filter Europe if Spain exists
            files_filtered = [f for f in files if f['region'] != 'Europe']
            if len(files_filtered) < len(files):
                discarded_europe = [f for f in files if f['region'] == 'Europe']
                if verbose and discarded_europe:
                    for disc in discarded_europe:
                        print(f"\n⚠️  {base_title}")
                        print(f"  ℹ️  Europe (with Es) discarded in favor of Spain")
                        print(f"  ❌ {disc['path'].name}")
                discarded_count += len(discarded_europe)
            files = files_filtered
        
        # Select the best file by priority
        best_file = min(files, key=lambda x: x['priority'])
        
        dest = final_dir / best_file['path'].name
        
        if verbose:
            print(f"\n✓ {base_title}")
            print(f"  ✅ SELECTED → {best_file['region']}: {best_file['path'].name}")
        
        # Copy file
        try:
            dest.write_bytes(best_file['path'].read_bytes())
            copied_count += 1
            if verbose:
                file_size = best_file['path'].stat().st_size / (1024 * 1024)  # MB
                print(f"     └─ Copied: {file_size:.2f} MB")
        except Exception as e:
            print(f"     └─ ❌ Copy error: {e}")
        
        # Show discarded alternatives
        for file_info in files:
            if file_info['path'] != best_file['path']:
                discarded_count += 1
                if verbose:
                    print(f"  ❌ DISCARDED → {file_info['region']}: {file_info['path'].name}")

    print("\n" + "=" * 80)
    print("📈 FINAL SUMMARY")
    print("=" * 80)
    print(f"✅ Files copied: {copied_count}")
    print(f"❌ Files discarded: {discarded_count}")
    print(f"📂 Final location: {final_dir.absolute()}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("=" * 80)
        print("🎮 ROM DOWNLOADER WITH REGION PRIORITY")
        print("=" * 80)
        print("\nUsage: python downloadroms.py <URL> [output_directory] [options]")
        print("\nOptions:")
        print("  --demos      Include Demo files")
        print("  --quiet      Quiet mode (no details)")
        print("\nExamples:")
        print("  python downloadroms.py 'https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/' 'psx'")
        print("  python downloadroms.py 'https://example.com/roms/' downloads --demos")
        print("  python downloadroms.py 'https://example.com/roms/' downloads --demos --quiet")
        print("\nNote:")
        print("  - URL must start with http:// or https://")
        print("  - Only downloads regions: Spain, Europe, Japan")
        print("  - Excludes individual regions: France, Germany, USA, etc.")
        print("=" * 80)
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = 'downloads'
    verbose = True
    include_demos = False
    
    # Process arguments
    for i in range(2, len(sys.argv)):
        arg = sys.argv[i]
        if arg == '--quiet':
            verbose = False
        elif arg == '--demos':
            include_demos = True
        elif not arg.startswith('--'):
            output_dir = arg
    
    print("=" * 80)
    print("🎮 ROM DOWNLOADER WITH REGION PRIORITY")
    print("=" * 80)
    print(f"📥 Download URL: {url}")
    print(f"📂 Output directory: {output_dir}")
    print(f"🌍 Allowed regions: Spain, Europe, Japan")
    print(f"🌍 Region priority: Spain > Europe > Japan")
    print(f"🎮 Include Demos: {'Yes' if include_demos else 'No'}")
    print(f"📢 Verbose mode: {'Enabled' if verbose else 'Disabled'}")
    
    download_and_filter(url, output_dir, verbose, include_demos)
    
    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)