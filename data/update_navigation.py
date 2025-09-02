import os
import re

def update_navigation_in_file(file_path):
    """Update navigation in HTML file to have only one 'Hồ sơ' menu item"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove duplicate profile menu items
        # Look for patterns like "Hồ sơ" and "Hồ sơ cá nhân" and keep only one
        lines = content.split('\n')
        updated_lines = []
        profile_found = False
        
        for line in lines:
            # Skip duplicate profile menu items
            if 'Hồ sơ cá nhân' in line or 'Personal Profile' in line:
                continue
            elif 'Hồ sơ' in line and 'nav-link' in line and not profile_found:
                profile_found = True
                updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        updated_content = '\n'.join(updated_lines)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated navigation in {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Update navigation in all HTML files"""
    template_dir = "templates"
    html_files = [
        "index.html",
        "profile.html", 
        "symptom_diagnosis_ai.html",
        "guides.html",
        "library.html",
        "news.html",
        "support.html",
        "admin_dashboard.html"
    ]
    
    for html_file in html_files:
        file_path = os.path.join(template_dir, html_file)
        if os.path.exists(file_path):
            update_navigation_in_file(file_path)
        else:
            print(f"⚠️ File not found: {file_path}")

if __name__ == "__main__":
    main()


