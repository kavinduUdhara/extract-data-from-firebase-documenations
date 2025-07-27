#!/usr/bin/env python3
"""
Enhanced Firebase Documentation Extractor - Version 2.0

Improved version that extracts complete documentation content while filtering out unwanted elements.
"""

import argparse
import sys
import re
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import html2text


class EnhancedFirebaseDocsExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def fetch_page(self, url):
        """Fetch the HTML content from the given URL."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None
    
    def extract_title(self, soup):
        """Extract the page title."""
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            # Clean up the title (remove Firebase branding)
            title_text = re.sub(r'\s*\|\s*Firebase.*$', '', title_text)
            return title_text
        
        # Fallback to h1 tag
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        return "Firebase Documentation"
    
    def find_documentation_content(self, soup):
        """Find the main documentation content with intelligent selection."""
        
        # Strategy: Try different approaches and pick the best one
        candidates = []
        
        # Try specific selectors first
        specific_selectors = [
            '.devsite-article-body',
            '.devsite-main-content', 
            'main[role="main"]',
            'main',
            'article',
            '.documentation-content',
            '#main-content'
        ]
        
        for selector in specific_selectors:
            elements = soup.select(selector)
            if elements:
                element = elements[0]
                # Clone the element to avoid modifying original
                test_element = soup.new_tag('div')
                test_element.append(element.__copy__())
                self.clean_content_intelligent(test_element)
                text_length = len(test_element.get_text(strip=True))
                if text_length > 1000:  # Must have substantial content
                    candidates.append((element, text_length, selector))
        
        # Try broader selectors if specific ones don't work well
        broad_selectors = [
            '.devsite-wrapper',
            'body'
        ]
        
        for selector in broad_selectors:
            elements = soup.select(selector)
            if elements:
                element = elements[0]
                # Clone the element to avoid modifying original
                test_element = soup.new_tag('div')
                test_element.append(element.__copy__())
                self.clean_content_intelligent(test_element)
                text_length = len(test_element.get_text(strip=True))
                if text_length > 3000:  # Higher threshold for broader selectors
                    candidates.append((element, text_length, selector))
        
        # Pick the candidate with the most content
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            best_element, content_length, selector = candidates[0]
            print(f"Using content selector: {selector}")
            print(f"Extracted content length: {content_length} characters")
            return best_element
        
        return None
    
    def clean_content_intelligent(self, content):
        """Intelligently clean content to remove navigation while preserving documentation."""
        if not content:
            return None
        
        # Remove script and style elements
        for element in content.find_all(['script', 'style']):
            element.decompose()
        
        # Remove navigation elements
        nav_selectors = [
            'nav',
            'header',
            'footer',
            '[role="navigation"]',
            '.devsite-nav',
            '.devsite-footer',
            '.devsite-header',
            '.devsite-banner',
            '.devsite-book-nav',
            '.devsite-book-nav-wrapper',
            '.devsite-mobile-nav',
            '.devsite-mobile-nav-bottom',
            '.devsite-top-logo-row',
            '.devsite-utility-nav',
            '.devsite-searchbox',
            '.devsite-footer-promos',
            '.devsite-footer-utility',
            '.breadcrumb',
            '.banner',
            '.advertisement'
        ]
        
        for selector in nav_selectors:
            for element in content.select(selector):
                element.decompose()
        
        # Remove elements that are likely navigation based on content
        for element in content.find_all():
            text = element.get_text(strip=True).lower()
            # Skip if this element contains substantial content
            if len(text) > 200:
                continue
                
            # Remove if it looks like navigation
            nav_keywords = [
                'build more run more', 'solutions pricing docs', 'overview fundamentals',
                'go to console', 'send feedback', 'firebase console', 'get started more',
                'firebase studio', 'samples community', 'support blog'
            ]
            
            if any(keyword in text for keyword in nav_keywords):
                if element.name in ['div', 'section', 'aside', 'nav']:
                    element.decompose()
        
        return content
    
    def convert_to_markdown(self, html_content, title):
        """Convert HTML content to Markdown with improved formatting."""
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        h.body_width = 0  # Don't wrap lines
        h.unicode_snob = True
        h.protect_links = True
        h.mark_code = True
        h.escape_snob = True
        
        markdown_content = h.handle(str(html_content))
        
        # Clean up the markdown
        import re
        
        # Replace multiple newlines with maximum of 2
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # Clean up excessive spaces
        markdown_content = re.sub(r' {3,}', '  ', markdown_content)
        
        # Fix common formatting issues
        markdown_content = re.sub(r'\\(.)', r'\1', markdown_content)  # Remove excessive escaping
        
        # Add title and metadata at the beginning
        metadata = f"""# {title}

**Source:** [Firebase Documentation]({self.current_url})  
**Extracted on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        return metadata + markdown_content
    
    def generate_filename(self, url, title):
        """Generate a safe filename from the URL and title."""
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        
        # Extract meaningful parts from the URL
        if 'docs' in path_parts:
            docs_index = path_parts.index('docs')
            relevant_parts = path_parts[docs_index + 1:]
        else:
            relevant_parts = path_parts
        
        # Create base filename from URL parts
        if relevant_parts:
            base_name = '-'.join(relevant_parts)
        else:
            # Fallback to title
            base_name = re.sub(r'[^\w\s-]', '', title.lower())
            base_name = re.sub(r'[-\s]+', '-', base_name)
        
        # Clean filename
        base_name = re.sub(r'[^\w\s-]', '', base_name)
        base_name = re.sub(r'[-\s]+', '-', base_name).strip('-')
        
        # Add query parameters if present
        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            for key, values in query_params.items():
                if values:
                    base_name += f"-{key}-{values[0]}"
        
        return f"{base_name}.md"
    
    def extract_and_save(self, url, output_dir="."):
        """Main method to extract documentation and save as Markdown."""
        self.current_url = url
        print(f"Fetching content from: {url}")
        
        # Fetch the page
        html_content = self.fetch_page(url)
        if not html_content:
            return False
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title = self.extract_title(soup)
        print(f"Page title: {title}")
        
        # Find main content
        main_content = self.find_documentation_content(soup)
        if not main_content:
            print("No main content found!")
            return False
        
        # Clean content
        cleaned_content = self.clean_content_intelligent(main_content)
        
        # Convert to Markdown
        markdown = self.convert_to_markdown(cleaned_content, title)
        
        # Generate filename
        filename = self.generate_filename(url, title)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        # Save to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"Documentation saved to: {filepath}")
            return True
        except IOError as e:
            print(f"Error saving file: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Extract Firebase documentation and convert to Markdown (Enhanced Version)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
  python enhanced_extractor.py "https://firebase.google.com/docs/auth" --output ./docs
        """
    )
    
    parser.add_argument(
        'url',
        help='Firebase documentation URL to extract'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory for the Markdown file (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    # Extract documentation
    extractor = EnhancedFirebaseDocsExtractor()
    success = extractor.extract_and_save(args.url, args.output)
    
    if success:
        print("✅ Documentation extracted successfully!")
    else:
        print("❌ Failed to extract documentation")
        sys.exit(1)


if __name__ == "__main__":
    main()
