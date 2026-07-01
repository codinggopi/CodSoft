import os
import glob
import re

html_files = glob.glob('../frontend/*.html')

viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
menu_btn = '\n            <button class="mobile-menu-toggle" id="mobile-menu-btn"><i class="fas fa-bars"></i></button>'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False

    # Check and insert viewport
    if 'name="viewport"' not in content:
        content = re.sub(r'(<head[^>]*>)', r'\1\n    ' + viewport_meta, content, count=1, flags=re.IGNORECASE)
        modified = True

    # Check and insert mobile menu toggle in nav
    if 'mobile-menu-toggle' not in content and 'class="navbar"' in content:
        # Find the logo anchor and insert after it
        # Usually it looks like: </a>\n            <div class="nav-links">
        pattern = re.compile(r'(<a[^>]*class="logo"[^>]*>.*?</a>)', re.DOTALL)
        content = pattern.sub(r'\1' + menu_btn, content)
        modified = True
    
    # Check tables for leaderboard and result
    if file in ['leaderboard.html', 'result.html']:
        if 'table-responsive' not in content and '<table' in content:
            # Wrap table
            pattern = re.compile(r'(<table[^>]*>.*?</table>)', re.DOTALL)
            content = pattern.sub(r'<div class="table-responsive">\n\1\n</div>', content)
            modified = True

    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
    else:
        print(f"Skipped {file}")

