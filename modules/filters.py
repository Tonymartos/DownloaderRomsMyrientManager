#!/usr/bin/env python3
# Copyright (C) 2025 Myrient ROM Manager Contributors
# This file is licensed under the GNU General Public License v3.0
# See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""
Filter and validation functions for ROM files
"""

import re


def is_demo_or_variant(filename):
    """
    Check if a filename contains demo or variant markers.
    Returns True if the file is a demo, revision, alternative, or special version.
    
    Patterns checked:
    - (Demo), (Demo 1), (Demo 2), etc.
    - (EDC) - Enhanced Data Correction
    - (Unl) - Unlicensed
    - (Alt) - Alternative version
    - (Rev 1), (Rev 2), (Rev 3), etc. - Revisions
    - (Beta) - Beta versions
    
    Args:
        filename: Name of the file to check
        
    Returns:
        bool: True if file is a demo/variant, False otherwise
    """
    demo_patterns = [
        r'\(Demo\s*\d*\)',      # (Demo), (Demo 1), (Demo 2), etc.
        r'\(EDC\)',              # Enhanced Data Correction
        r'\(Unl\)',              # Unlicensed
        r'\(Alt\)',              # Alternative version
        r'\(Rev\s*\d+\)',        # (Rev 1), (Rev 2), etc.
        r'\(Beta\)',             # Beta versions
    ]
    
    for pattern in demo_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            return True
    
    return False


def has_language_in_file(filename, language_code):
    """
    Check if a file contains a specific language code.
    
    Args:
        filename: Name of the file to check
        language_code: Language code to search for (e.g., 'Es', 'En', 'Fr')
        
    Returns:
        bool: True if language code is found, False otherwise
    """
    pattern = re.compile(rf'\b{re.escape(language_code)}\b', re.IGNORECASE)
    return bool(pattern.search(filename))


def is_valid_region_for_config(filename, config):
    """
    Validate if a file's region matches the configuration requirements.
    
    Args:
        filename: Name of the file to check
        config: Configuration dictionary with filter mode and language/region settings
        
    Returns:
        bool: True if file is valid for the config, False otherwise
    """
    from .extractor import extract_region
    
    filter_mode = config.get('filter_mode', 'none')
    
    if filter_mode == 'none':
        return True
    
    elif filter_mode == 'country':
        # Country-specific filter
        country = config.get('specific_country')
        country_pattern = fr'\({country}\)'
        return bool(re.search(country_pattern, filename, re.IGNORECASE))
    
    elif filter_mode == 'language':
        # Language-based filter
        language_code = config.get('language')
        region = extract_region(filename)
        
        # Check if Europe and has the language
        if region == 'Europe' and language_code:
            return has_language_in_file(filename, language_code)
        
        # Check if it's the specific country for that language
        language_countries = {
            'Es': 'Spain',
            'En': 'USA',
            'Fr': 'France',
            'De': 'Germany',
            'It': 'Italy',
            'Pt': 'Portugal'
        }
        
        country = language_countries.get(language_code)
        if country and region == country:
            return True
            
        # Japan is always allowed as fallback
        if region == 'Japan':
            return True
            
        return False
    
    elif filter_mode == 'region':
        # Region-based filter
        allowed_region = config.get('region')
        region = extract_region(filename)
        return region == allowed_region
    
    return False


def extract_key_words(title):
    """
    Extract key words from a title for duplicate detection.
    Normalizes the title and removes common patterns.
    
    CONSERVATIVE APPROACH: Keep ALL years as they indicate different game versions.
    Examples where years indicate DIFFERENT games:
    - "All Star Tennis" vs "All Star Tennis 2000" → Different games
    - "FIFA 99" vs "FIFA 2000" → Different annual releases
    - "Need for Speed '99" vs "Need for Speed 2000" → Different versions
    
    Args:
        title: Game title to extract keywords from
        
    Returns:
        list: List of normalized keywords
    """
    # Remove file extension if present
    title = re.sub(r'\.(zip|rar|7z)$', '', title, flags=re.IGNORECASE)
    
    # Remove disc information temporarily to focus on game title
    title_without_disc = re.sub(r'\(Disc \d+\)', '', title, flags=re.IGNORECASE)
    title_without_disc = re.sub(r'Disc \d+', '', title_without_disc, flags=re.IGNORECASE)
    
    # Remove common parenthetical information (languages, regions, etc.)
    title_clean = re.sub(r'\([^)]*\)', '', title_without_disc)
    
    # Remove common separators and normalize (including apostrophes for years like '99)
    title_clean = re.sub(r"[-_.:,'']", ' ', title_clean)
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
    
    # Keep words that are 2+ characters and not common words
    # Exception: single-digit numbers are kept (version numbers like 2, 3, 4)
    key_words = []
    for word in words:
        word_clean = word.lower().strip()
        # Keep if: (2+ chars OR single digit) AND not a common word
        if word_clean not in common_words:
            if (len(word_clean) >= 2 and (word_clean.isdigit() or word_clean.isalpha())) or \
               (len(word_clean) == 1 and word_clean.isdigit()):
                key_words.append(word_clean)
    
    return key_words


def extract_disc_info(filename):
    """
    Extract disc information from filename.
    
    Args:
        filename: Name of the file to extract disc info from
        
    Returns:
        int: Disc number or None if not found
    """
    disc_match = re.search(r'\(Disc (\d+)\)', filename, re.IGNORECASE)
    if disc_match:
        return int(disc_match.group(1))
    
    disc_match = re.search(r'Disc (\d+)', filename, re.IGNORECASE)
    if disc_match:
        return int(disc_match.group(1))
    
    return None


def get_priority_language_from_config(config):
    """
    Get the priority language from config for comparison.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        str: Priority language code or empty string
    """
    return config.get('primary_language', '')


def check_keywords_similarity(exclusive_title, valid_titles, threshold=0.7):
    """
    Check if an exclusive title is similar to any valid title.
    
    Args:
        exclusive_title: Title to check
        valid_titles: List of titles to compare against
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        tuple: (bool: True if similar title found, str: matched title or None)
    """
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
