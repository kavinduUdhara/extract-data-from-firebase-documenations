#!/usr/bin/env python3
"""
Enhanced debug script to find all content on Firebase docs page
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_full_content(url):
    """Analyze the full content structure of the Firebase docs page."""
    
    print(f"🔍 Analyzing full content for: {url}")
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
    
    # Look for all potential content containers
    print("\n📋 Analyzing all div elements with substantial content:")
    print("-" * 60)
    
    all_elements = soup.find_all(['div', 'section', 'article', 'main'])
    content_elements = []
    
    for element in all_elements:
        text_content = element.get_text(strip=True)
        if len(text_content) > 1000:  # Look for elements with substantial content
            classes = element.get('class', [])
            element_id = element.get('id', '')
            tag_name = element.name
            
            # Calculate unique text (not including nested elements)
            direct_text = ""
            for string in element.strings:
                if string.strip():
                    direct_text += string.strip() + " "
            
            content_elements.append({
                'element': element,
                'tag': tag_name,
                'classes': classes,
                'id': element_id,
                'total_text_length': len(text_content),
                'direct_text_length': len(direct_text.strip()),
                'text_preview': text_content[:200]
            })
    
    # Sort by total text length
    content_elements.sort(key=lambda x: x['total_text_length'], reverse=True)
    
    print(f"Found {len(content_elements)} elements with substantial content:")
    print()
    
    for i, elem_info in enumerate(content_elements[:10]):  # Show top 10
        print(f"{i+1:2d}. {elem_info['tag']:<8} | {elem_info['total_text_length']:>6} chars | Classes: {elem_info['classes']}")
        print(f"    ID: {elem_info['id']}")
        print(f"    Preview: {elem_info['text_preview']}...")
        print()
    
    # Look for specific patterns that might indicate the main content
    print("\n🎯 Looking for complete documentation patterns:")
    print("-" * 50)
    
    # Check if there are multiple sections or steps
    steps = soup.find_all(text=re.compile(r'Step \d+|## Step|###\s*Step', re.IGNORECASE))
    print(f"Found {len(steps)} step indicators")
    
    # Look for headings to understand document structure
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    print(f"Found {len(headings)} headings")
    
    print("\nDocument structure (headings):")
    for i, heading in enumerate(headings[:15]):  # Show first 15 headings
        level = heading.name
        text = heading.get_text(strip=True)
        print(f"  {level}: {text}")
    
    # Check for the largest single container
    if content_elements:
        largest = content_elements[0]
        print(f"\n📄 Largest content container:")
        print(f"   Tag: {largest['tag']}")
        print(f"   Classes: {largest['classes']}")
        print(f"   ID: {largest['id']}")
        print(f"   Total text: {largest['total_text_length']} characters")
        
        # Extract and show more of this content
        full_text = largest['element'].get_text(strip=True)
        
        # Look for common Firebase doc sections
        if 'Prerequisites' in full_text:
            print("   ✅ Contains Prerequisites section")
        if 'Step 1' in full_text or 'Step 2' in full_text:
            print("   ✅ Contains Step sections")
        if 'Before you begin' in full_text:
            print("   ✅ Contains 'Before you begin' section")
        if 'Add the dependency' in full_text or 'Install' in full_text:
            print("   ✅ Contains installation instructions")
        if 'Initialize' in full_text:
            print("   ✅ Contains initialization instructions")
        
        # Show where the content ends
        words = full_text.split()
        if len(words) > 100:
            print(f"\n   Last 50 words: ...{' '.join(words[-50:])}")

if __name__ == "__main__":
    url = "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
    analyze_full_content(url)
