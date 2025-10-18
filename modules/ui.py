"""UI Module - User interface functions
Contains banners, menus, tables, and user interaction functions

Copyright (C) 2025 Myrient ROM Manager Contributors
This file is licensed under the GNU General Public License v3.0
See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""

from .utils import Colors, convert_bytes_to_readable


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


def ask_confirmation():
    """Asks for confirmation before download"""
    while True:
        response = input(f"\n{Colors.BOLD}Do you want to proceed with the download? (yes/no): {Colors.END}").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please answer 'yes' or 'no'")


def show_search_mode_menu():
    """Shows the search mode selection menu"""
    print(f"\n{Colors.BOLD}🔍 SEARCH MODE:{Colors.END}")
    print(f"  1. {Colors.GREEN}Analyze entire collection{Colors.END} (default)")
    print(f"  2. {Colors.CYAN}Search for specific title{Colors.END}")
    print()


def show_step_separator(step_number, title):
    """Shows a visual separator for each step"""
    separator = f"{Colors.BLUE}{'🟦' * 44}{Colors.END}"
    print(f"\n{separator}")
    print(f"{Colors.BOLD}🔻 STEP {step_number}: {title} 🔻{Colors.END}")
