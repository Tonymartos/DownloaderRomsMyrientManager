"""Utils Module - Utility functions and constants
Contains color codes, size conversions, and helper functions

Copyright (C) 2025 Myrient ROM Manager Contributors
This file is licensed under the GNU General Public License v3.0
See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""

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


def convert_bytes_to_readable(bytes_size):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PiB"


def validate_url(url):
    """Validate if URL is a valid Myrient URL"""
    if not url:
        return False
    if not url.startswith('https://myrient.erista.me/'):
        return False
    return True


def ask_yes_no(question):
    """Ask a yes/no question and return boolean. Defaults to 'no' on empty input."""
    while True:
        answer = input(f"{question} (yes/no) [default: no]: ").strip().lower()
        if answer == '':
            return False  # Default to "no"
        if answer in ['yes', 'y']:
            return True
        elif answer in ['no', 'n']:
            return False
        else:
            print("Please answer 'yes' or 'no'")
