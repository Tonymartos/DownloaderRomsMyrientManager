#!/usr/bin/env python3
"""
Display module - UI elements, banners, menus, and tables
"""
import os


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
    os.system('clear' if os.name != 'nt' else 'cls')
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
{Colors.BOLD}📋 Main Menu:{Colors.END}
{Colors.GREEN}1.{Colors.END} Download with language priority (Spain, Europe, etc.)
{Colors.GREEN}2.{Colors.END} Preview files before downloading
{Colors.GREEN}3.{Colors.END} Extract downloaded ZIP files
{Colors.GREEN}4.{Colors.END} Exit

{Colors.YELLOW}Select an option:{Colors.END} """
    print(menu, end='')


def convert_bytes_to_readable(bytes_size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def print_preview_table(selected, discarded, invalid, config):
    """
    Display a table with selected, discarded and invalid files
    """
    total_size = sum(f['size'] for f in selected)
    
    print(f"\n{Colors.BOLD}{'='*100}")
    print(f"📊 DOWNLOAD PREVIEW - Configuration: {config.get('name', 'Custom')}")
    print(f"{'='*100}{Colors.END}\n")
    
    # Selected files
    if selected:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ FILES TO DOWNLOAD ({len(selected)}) - Total: {convert_bytes_to_readable(total_size)}{Colors.END}")
        print(f"{Colors.CYAN}{'─'*100}{Colors.END}")
        
        for i, file in enumerate(selected, 1):
            size_str = convert_bytes_to_readable(file['size'])
            print(f"{i:3}. {Colors.GREEN}[{size_str:>10}]{Colors.END} {file['name']}")
    
    # Discarded files
    if discarded:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⊘ DISCARDED FILES ({len(discarded)}){Colors.END}")
        print(f"{Colors.CYAN}{'─'*100}{Colors.END}")
        
        for i, file in enumerate(discarded[:20], 1):  # Show first 20
            reason = file.get('reason', 'Unknown')
            size_str = convert_bytes_to_readable(file['size'])
            print(f"{i:3}. {Colors.YELLOW}[{size_str:>10}]{Colors.END} {file['name']}")
            print(f"     {Colors.YELLOW}└─ Reason: {reason}{Colors.END}")
        
        if len(discarded) > 20:
            print(f"\n     {Colors.YELLOW}... and {len(discarded) - 20} more discarded files{Colors.END}")
    
    # Invalid files
    if invalid:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ INVALID FILES ({len(invalid)}){Colors.END}")
        print(f"{Colors.CYAN}{'─'*100}{Colors.END}")
        
        for i, file in enumerate(invalid[:10], 1):  # Show first 10
            reason = file.get('reason', 'Unknown')
            print(f"{i:3}. {Colors.RED}{file['name']}{Colors.END}")
            print(f"     {Colors.RED}└─ Reason: {reason}{Colors.END}")
        
        if len(invalid) > 10:
            print(f"\n     {Colors.RED}... and {len(invalid) - 10} more invalid files{Colors.END}")
    
    print(f"\n{Colors.BOLD}{'='*100}{Colors.END}")


def show_available_options(analysis):
    """Display available languages and regions"""
    print(f"\n{Colors.BOLD}{'='*80}")
    print(f"📊 AVAILABLE OPTIONS IN THE CATALOG")
    print(f"{'='*80}{Colors.END}\n")
    
    # Regions
    if analysis['regions']:
        print(f"{Colors.CYAN}🌍 Regions found:{Colors.END}")
        for region, count in sorted(analysis['regions'].items(), key=lambda x: x[1], reverse=True):
            print(f"  • {region}: {count} files")
    
    # Languages
    if analysis['languages']:
        print(f"\n{Colors.CYAN}🗣️  Languages found:{Colors.END}")
        for lang, count in sorted(analysis['languages'].items(), key=lambda x: x[1], reverse=True):
            print(f"  • {lang}: {count} files")
    
    # Multi-disc games
    if analysis.get('multi_disc'):
        print(f"\n{Colors.CYAN}💿 Multi-disc games: {analysis['multi_disc']}{Colors.END}")
    
    print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")


def show_exclusive_games_options(exclusive_games):
    """Display exclusive games organized by region/language"""
    print(f"\n{Colors.BOLD}{'='*80}")
    print(f"🎮 EXCLUSIVE GAMES DETECTED")
    print(f"{'='*80}{Colors.END}\n")
    
    for category, games in exclusive_games.items():
        if games:
            print(f"{Colors.GREEN}{Colors.BOLD}{category.upper()} ({len(games)} games){Colors.END}")
            print(f"{Colors.CYAN}{'─'*80}{Colors.END}")
            
            for i, game in enumerate(games[:15], 1):  # Show first 15
                print(f"  {i:2}. {game['name']}")
            
            if len(games) > 15:
                print(f"     {Colors.YELLOW}... and {len(games) - 15} more{Colors.END}")
            print()
    
    print(f"{Colors.BOLD}{'='*80}{Colors.END}")


def ask_confirmation():
    """Ask user for confirmation to proceed with download"""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  WARNING: This will download the selected files{Colors.END}")
    response = input(f"{Colors.YELLOW}Do you want to proceed? (yes/no): {Colors.END}").strip().lower()
    return response == 'yes'


def ask_yes_no(question):
    """Ask a yes/no question"""
    response = input(f"{Colors.YELLOW}{question} (yes/no): {Colors.END}").strip().lower()
    return response == 'yes'


def print_progress(current, total, file_name, speed=""):
    """Print download progress"""
    percentage = (current / total) * 100 if total > 0 else 0
    bar_length = 40
    filled = int(bar_length * current / total) if total > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    
    print(f"\r{Colors.CYAN}[{bar}] {percentage:.1f}%{Colors.END} {file_name[:50]} {speed}", end='', flush=True)
