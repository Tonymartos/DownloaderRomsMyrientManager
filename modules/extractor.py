"""Extractor Module - File extraction functions
Handles ZIP file extraction with progress tracking

Copyright (C) 2025 Myrient ROM Manager Contributors
This file is licensed under the GNU General Public License v3.0
See LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt for details.
"""

import zipfile
from pathlib import Path
from .utils import Colors


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
