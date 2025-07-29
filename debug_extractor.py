#!/usr/bin/env python3
"""
Debug version of the Firebase Documentation Extractor to understand filtering issues.
"""

import requests
from bs4 import BeautifulSoup
from firebase_docs_extractor import FirebaseDocsExtractor

def debug_filtering_issue():
    """Debug the filtering issue with web language selection."""
    
    url = "https://firebase.google.com/docs/ai-logic/solutions/remote-config?api=vertex"
    extractor = FirebaseDocsExtractor(selected_languages=['web'])
    
    print(f"Fetching content from: {url}")
    html_content = extractor.fetch_page(url)
    if not html_content:
        return
    
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = extractor.extract_main_content(soup)
    
    print(f"Original content length: {len(str(main_content))}")
    
    # Check headings before filtering
    headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    print(f"\nFound {len(headings)} headings before filtering:")
    for i, heading in enumerate(headings[:20]):  # Show first 20
        heading_text = heading.get_text().strip()
        print(f"  {i+1}. {heading.name}: {heading_text}")
    
    # Apply filtering
    filtered_content = extractor.filter_content_by_languages(main_content)
    
    print(f"\nFiltered content length: {len(str(filtered_content))}")
    
    # Check headings after filtering
    filtered_headings = filtered_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    print(f"\nFound {len(filtered_headings)} headings after filtering:")
    for i, heading in enumerate(filtered_headings):
        heading_text = heading.get_text().strip()
        print(f"  {i+1}. {heading.name}: {heading_text}")
    
    # Show first few paragraphs of filtered content
    paragraphs = filtered_content.find_all('p')
    print(f"\nFirst few paragraphs in filtered content:")
    for i, p in enumerate(paragraphs[:5]):
        text = p.get_text().strip()[:100]
        print(f"  {i+1}. {text}...")

if __name__ == "__main__":
    debug_filtering_issue()
