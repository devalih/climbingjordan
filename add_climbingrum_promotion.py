#!/usr/bin/env python3
"""
Script to add ClimbingRum.com promotional banner and menu links to all HTML pages.
"""

import os
import re
from pathlib import Path

# ClimbingRum.com promotional banner HTML
CLIMBINGRUM_BANNER = '''
<!-- ClimbingRum.com Promotional Banner -->
<div id="climbingrum-banner" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px 0; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
  <div class="container_12" style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 15px;">
    <span style="color: white; font-size: 15px; font-weight: 500;">🏔️ Discover Wadi Rum:</span>
    <a href="https://www.climbingrum.com/climbing/" target="_blank" style="color: #fff; text-decoration: none; padding: 6px 15px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 13px; transition: all 0.3s; display: inline-block;">Climbing</a>
    <a href="https://www.climbingrum.com/mountains/" target="_blank" style="color: #fff; text-decoration: none; padding: 6px 15px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 13px; transition: all 0.3s; display: inline-block;">Mountains</a>
    <a href="https://www.climbingrum.com/guides/" target="_blank" style="color: #fff; text-decoration: none; padding: 6px 15px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 13px; transition: all 0.3s; display: inline-block;">Guides</a>
    <a href="https://www.climbingrum.com/blog/" target="_blank" style="color: #fff; text-decoration: none; padding: 6px 15px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 13px; transition: all 0.3s; display: inline-block;">Blog</a>
    <a href="https://www.climbingrum.com/" target="_blank" style="color: #ffd700; text-decoration: none; font-weight: 600; font-size: 14px; margin-left: 10px;">Visit ClimbingRum.com →</a>
  </div>
</div>
<style>
  #climbingrum-banner a:hover {
    background: rgba(255,255,255,0.3) !important;
    transform: translateY(-2px);
  }
</style>

'''

# Menu item to add
MENU_ITEM = '<li class="item-150 deeper parent"><a href="https://www.climbingrum.com/" target="_blank" style="color: #e67e22;">Wadi Rum ↗</a><ul><li class="item-151"><a href="https://www.climbingrum.com/climbing/" target="_blank">Climbing</a></li><li class="item-152"><a href="https://www.climbingrum.com/mountains/" target="_blank">Mountains</a></li><li class="item-153"><a href="https://www.climbingrum.com/guides/" target="_blank">Guides</a></li><li class="item-154"><a href="https://www.climbingrum.com/blog/" target="_blank">Blog</a></li></ul></li>'

def has_climbingrum_content(content):
    """Check if the file already has ClimbingRum.com content."""
    return 'climbingrum-banner' in content or 'climbingrum.com' in content.lower()

def add_banner(content):
    """Add promotional banner after mainmenu div."""
    # Look for the pattern: </div>\n<div class="clear"></div>\n<div id="banner">
    # This appears after the mainmenu closes
    pattern = re.compile(
        r'(</div>\s*<div class="clear"></div>\s*)(<div id="banner">)',
        re.IGNORECASE | re.DOTALL
    )
    
    if pattern.search(content):
        new_content = pattern.sub(r'\1' + CLIMBINGRUM_BANNER + r'\2', content, count=1)
        return new_content, True
    
    return content, False

def add_menu_item(content):
    """Add ClimbingRum.com menu item before closing </ul> in main menu."""
    # Find the main menu and add the item before the closing </ul>
    # Look for pattern: <li class="item-147"><a href="/links" >Links</a></li></ul>
    pattern = re.compile(
        r'(<li class="item-147"><a href="/links"[^>]*>Links</a></li>)(</ul>)',
        re.IGNORECASE
    )
    
    if pattern.search(content):
        new_content = pattern.sub(r'\1' + MENU_ITEM + r'\2', content, count=1)
        return new_content, True
    
    return content, False

def process_html_file(file_path):
    """Process a single HTML file to add ClimbingRum.com promotion."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if already has ClimbingRum content
        if has_climbingrum_content(content):
            return False, "Already has ClimbingRum content"
        
        # Check if file has required structure
        if '<div id="banner">' not in content.lower():
            return False, "No banner div found"
        
        original_content = content
        banner_added = False
        menu_added = False
        
        # Add banner
        content, banner_added = add_banner(content)
        
        # Add menu item
        content, menu_added = add_menu_item(content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            changes = []
            if banner_added:
                changes.append("banner")
            if menu_added:
                changes.append("menu")
            
            return True, f"Added: {', '.join(changes)}"
        
        return False, "No changes needed"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main function to process all HTML files."""
    project_root = Path(__file__).parent
    
    # Find all HTML files
    html_files = list(project_root.rglob('*.html'))
    
    print(f"Found {len(html_files)} HTML files")
    print("-" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for html_file in html_files:
        relative_path = html_file.relative_to(project_root)
        success, message = process_html_file(html_file)
        
        if success:
            print(f"✓ {relative_path}: {message}")
            success_count += 1
        elif "Already has" in message:
            print(f"⊘ {relative_path}: {message}")
            skip_count += 1
        else:
            # Only show errors for files that should have been updated
            if "No banner div found" not in message:
                print(f"✗ {relative_path}: {message}")
                error_count += 1
    
    print("-" * 60)
    print(f"\nSummary:")
    print(f"  Successfully updated: {success_count}")
    print(f"  Skipped (already has content): {skip_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total files: {len(html_files)}")

if __name__ == "__main__":
    main()
