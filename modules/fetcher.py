"""Fetcher Module - Functions to fetch data from Myrient
Handles HTTP requests and HTML parsing

Copyright (C) 2025 Myrient ROM Manager Contributors
This file is licensed under the GNU General Public License v3.0
See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
from .utils import Colors


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
