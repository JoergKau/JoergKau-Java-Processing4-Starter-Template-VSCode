#!/usr/bin/env python3
"""
Download Processing Javadoc and create a JAR file for VS Code integration.
This creates a proper javadoc JAR that VS Code can use for enhanced hover hints.
"""

import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
import zipfile
import shutil
import ssl

# Create an SSL context that doesn't verify certificates
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

BASE_URL = "https://processing.github.io/processing4-javadocs"
TEMP_DIR = "temp_javadoc"
OUTPUT_JAR = "core-4.4.8-javadoc.jar"

class JavadocLinkParser(HTMLParser):
    """Parse HTML to extract links to other javadoc pages."""
    def __init__(self):
        super().__init__()
        self.links = set()
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and value:
                    # Filter for javadoc-related files
                    if (value.endswith('.html') or 
                        value.endswith('.css') or 
                        value.endswith('.js')):
                        self.links.add(value)

def download_file(url, local_path):
    """Download a file from URL to local path."""
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Downloading: {url}")
        
        # Use urlopen with SSL context
        with urllib.request.urlopen(url, context=ssl_context) as response:
            with open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def get_links_from_html(html_content):
    """Extract links from HTML content."""
    parser = JavadocLinkParser()
    try:
        parser.feed(html_content)
    except:
        pass
    return parser.links

def download_javadoc():
    """Download the Processing Javadoc files."""
    print("Creating temporary directory...")
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Start with the main pages
    pages_to_download = {
        'index.html',
        'overview-summary.html',
        'overview-tree.html',
        'deprecated-list.html',
        'index-all.html',
        'help-doc.html',
        'stylesheet.css',
        'script.js',
        'processing/core/package-summary.html',
        'processing/core/PApplet.html',
        'processing/core/PGraphics.html',
        'processing/core/PImage.html',
        'processing/core/PVector.html',
        'processing/core/PShape.html',
        'processing/core/PFont.html',
        'processing/data/package-summary.html',
        'processing/event/package-summary.html',
        'processing/opengl/package-summary.html',
        'processing/awt/package-summary.html',
    }
    
    downloaded = set()
    
    while pages_to_download:
        page = pages_to_download.pop()
        
        if page in downloaded or page.startswith('http'):
            continue
            
        # Clean up the path
        page = page.split('#')[0]  # Remove anchors
        page = page.split('?')[0]  # Remove query strings
        
        if not page:
            continue
            
        url = f"{BASE_URL}/{page}"
        local_path = os.path.join(TEMP_DIR, page)
        
        if download_file(url, local_path):
            downloaded.add(page)
            
            # If it's an HTML file, parse it for more links
            if page.endswith('.html'):
                try:
                    with open(local_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        links = get_links_from_html(content)
                        
                        # Add new links relative to current page's directory
                        page_dir = os.path.dirname(page)
                        for link in links:
                            if not link.startswith('http'):
                                # Resolve relative paths
                                if link.startswith('../'):
                                    # Go up from current directory
                                    full_link = os.path.normpath(os.path.join(page_dir, link))
                                elif link.startswith('./'):
                                    full_link = os.path.join(page_dir, link[2:])
                                elif '/' in link:
                                    full_link = link
                                else:
                                    full_link = os.path.join(page_dir, link)
                                
                                pages_to_download.add(full_link)
                except Exception as e:
                    print(f"Error parsing {page}: {e}")
    
    print(f"\nDownloaded {len(downloaded)} files")
    return len(downloaded) > 0

def create_jar():
    """Create a JAR file from the downloaded content."""
    print("\nCreating JAR file...")
    
    try:
        with zipfile.ZipFile(OUTPUT_JAR, 'w', zipfile.ZIP_DEFLATED) as jar:
            for root, dirs, files in os.walk(TEMP_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, TEMP_DIR)
                    jar.write(file_path, arcname)
                    print(f"Added: {arcname}")
        
        print(f"\n✓ Successfully created {OUTPUT_JAR}")
        print(f"  Location: {os.path.abspath(OUTPUT_JAR)}")
        return True
    except Exception as e:
        print(f"Error creating JAR: {e}")
        return False

def cleanup():
    """Remove temporary directory."""
    print("\nCleaning up...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    print("Done!")

def main():
    """Main execution function."""
    print("Processing Javadoc JAR Creator")
    print("=" * 50)
    
    try:
        if download_javadoc():
            if create_jar():
                cleanup()
                print("\n" + "=" * 50)
                print("SUCCESS!")
                print(f"Your javadoc JAR is ready: {OUTPUT_JAR}")
                print("\nNext steps:")
                print("1. The .vscode/settings.json will be updated automatically")
                print("2. Reload VS Code window (Cmd+Shift+P -> 'Reload Window')")
                print("3. Hover over Processing methods to see enhanced documentation")
                return 0
            else:
                print("\nFailed to create JAR file")
                return 1
        else:
            print("\nFailed to download javadoc files")
            return 1
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        cleanup()
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        cleanup()
        return 1

if __name__ == "__main__":
    sys.exit(main())
