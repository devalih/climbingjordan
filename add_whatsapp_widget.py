#!/usr/bin/env python3
"""
Script to add WhatsApp chat widget to all HTML pages in the project.
"""

import os
import re
from pathlib import Path

# WhatsApp widget HTML code
WHATSAPP_WIDGET = '''
<!-- WhatsApp Chat Widget -->
<a href="https://wa.me/962788450926" target="_blank" id="whatsapp-chat-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; background-color: #25D366; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3); transition: transform 0.3s ease, box-shadow 0.3s ease; text-decoration: none;">
  <svg width="35" height="35" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 0C7.164 0 0 7.164 0 16c0 2.828.744 5.484 2.04 7.78L0 32l8.384-2.196A15.934 15.934 0 0016 32c8.836 0 16-7.164 16-16S24.836 0 16 0zm0 29.333c-2.456 0-4.784-.664-6.776-1.82l-.488-.288-5.056 1.324 1.348-4.932-.316-.504A13.268 13.268 0 012.667 16c0-7.364 5.968-13.333 13.333-13.333S29.333 8.636 29.333 16 23.364 29.333 16 29.333z" fill="white"/>
    <path d="M23.572 19.52c-.396-.2-2.344-1.156-2.708-1.288-.364-.132-.628-.2-.892.2-.264.396-1.024 1.288-1.256 1.552-.232.264-.464.296-.86.096-.396-.2-1.672-.616-3.184-1.964-1.176-1.048-1.972-2.344-2.204-2.74-.232-.396-.024-.612.176-.808.18-.18.396-.464.596-.696.2-.232.264-.396.396-.66.132-.264.068-.496-.032-.696-.1-.2-.892-2.148-1.224-2.94-.324-.772-.652-.668-.892-.68-.232-.012-.496-.016-.76-.016-.264 0-.692.1-1.056.496-.364.396-1.388 1.356-1.388 3.308s1.42 3.836 1.62 4.1c.2.264 2.808 4.288 6.804 6.012.952.412 1.696.656 2.276.84.956.304 1.824.26 2.512.156.764-.116 2.344-.96 2.676-1.884.332-.924.332-1.716.232-1.884-.1-.168-.364-.268-.76-.468z" fill="white"/>
  </svg>
</a>
<style>
  #whatsapp-chat-widget:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 12px rgba(0,0,0,0.4);
  }
</style>

'''

def has_whatsapp_widget(content):
    """Check if the file already has the WhatsApp widget."""
    return 'whatsapp-chat-widget' in content

def add_widget_to_html(file_path):
    """Add WhatsApp widget to an HTML file if it doesn't already have it."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if widget already exists
        if has_whatsapp_widget(content):
            return False, "Already has widget"
        
        # Check if file has closing body tag
        if '</body>' not in content.lower():
            return False, "No closing body tag found"
        
        # Add widget before closing body tag (case-insensitive)
        pattern = re.compile(r'(</body>)', re.IGNORECASE)
        new_content = pattern.sub(WHATSAPP_WIDGET + r'\1', content, count=1)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Widget added successfully"
    
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
        success, message = add_widget_to_html(html_file)
        
        if success:
            print(f"✓ {relative_path}: {message}")
            success_count += 1
        elif "Already has widget" in message:
            print(f"⊘ {relative_path}: {message}")
            skip_count += 1
        else:
            print(f"✗ {relative_path}: {message}")
            error_count += 1
    
    print("-" * 60)
    print(f"\nSummary:")
    print(f"  Successfully updated: {success_count}")
    print(f"  Skipped (already has widget): {skip_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total files: {len(html_files)}")

if __name__ == "__main__":
    main()
