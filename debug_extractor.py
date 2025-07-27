#!/usr/bin/env python3
"""
Debug script to analyze Firebase documentation page structure
"""

import requests
from bs4 import BeautifulSoup

def debug_page_structure(url):
    """Debug the page structure to understand content extraction issues."""
    
    print(f"🔍 Debugging page structure for: {url}")
    print("=" * 80)
    
    # Fetch the page
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        html_content = response.text
        print(f"✅ Successfully fetched {len(html_content)} characters")
    except Exception as e:
        print(f"❌ Error fetching URL: {e}")
        return
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check different content selectors
    selectors_to_test = [
        'main[role="main"]',
        'main',
        '.devsite-article-body',
        '.devsite-main-content', 
        'article',
        '.documentation-content',
        '#main-content',
        '.devsite-article',
        '.devsite-doc-content',
        '[role="main"]',
        '.content',
        '#content'
    ]
    
    print("\n📋 Testing content selectors:")
    print("-" * 40)
    
    for selector in selectors_to_test:
        elements = soup.select(selector)
        if elements:
            element = elements[0]
            text_length = len(element.get_text(strip=True))
            print(f"✅ {selector:<25} -> {text_length:>6} chars")
            
            # Show first few words
            text_preview = element.get_text(strip=True)[:100]
            print(f"   Preview: {text_preview}...")
            print()
        else:
            print(f"❌ {selector:<25} -> Not found")
    
    # Check for any elements that might contain the full content
    print("\n🔍 Looking for large content blocks:")
    print("-" * 40)
    
    # Find all div elements and check their text length
    all_divs = soup.find_all('div')
    large_divs = []
    
    for div in all_divs:
        text_length = len(div.get_text(strip=True))
        if text_length > 5000:  # Arbitrary threshold for "large" content
            classes = div.get('class', [])
            div_id = div.get('id', '')
            large_divs.append((div, text_length, classes, div_id))
    
    # Sort by text length (descending)
    large_divs.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(large_divs)} large content blocks:")
    for i, (div, text_length, classes, div_id) in enumerate(large_divs[:5]):  # Show top 5
        print(f"{i+1}. {text_length:>6} chars - Classes: {classes} - ID: {div_id}")
        
        # Show a preview
        text_preview = div.get_text(strip=True)[:150]
        print(f"   Preview: {text_preview}...")
        print()
    
    # Look for specific Firebase documentation patterns
    print("\n🔥 Looking for Firebase-specific patterns:")
    print("-" * 40)
    
    firebase_patterns = [
        ('.firebase-article', 'Firebase article container'),
        ('.documentation', 'Documentation container'),
        ('[data-module="article"]', 'Article module'),
        ('.article-content', 'Article content'),
        ('.guide-content', 'Guide content'),
        ('.doc-content', 'Doc content')
    ]
    
    for pattern, description in firebase_patterns:
        elements = soup.select(pattern)
        if elements:
            text_length = len(elements[0].get_text(strip=True))
            print(f"✅ {description:<25} -> {text_length:>6} chars")
        else:
            print(f"❌ {description:<25} -> Not found")

if __name__ == "__main__":
    url = "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
    debug_page_structure(url)
