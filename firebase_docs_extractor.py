#!/usr/bin/env python3
"""
Firebase Documentation Extractor

A tool to fetch Firebase documentation from URLs and convert them to Markdown format.
Supports filtering by programming languages to show only relevant code examples.

Usage:
    python firebase_docs_extractor.py <url>
    python firebase_docs_extractor.py <url> --languages swift web
    python firebase_docs_extractor.py <url> --interactive

Example:
    python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
    python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" --languages swift kotlin web
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

# For interactive menu
try:
    import msvcrt  # Windows
    import os as term_os
except ImportError:
    try:
        import termios  # Unix/Linux/Mac
        import tty
        import select
    except ImportError:
        pass


class FirebaseDocsExtractor:
    def __init__(self, selected_languages=None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.selected_languages = selected_languages or []
        
        # Define language mappings (case-insensitive)
        self.language_mappings = {
            'swift': ['swift', 'ios'],
            'kotlin': ['kotlin', 'android'],
            'java': ['java'],
            'web': ['web', 'javascript', 'js'],
            'dart': ['dart', 'flutter'],
            'unity': ['unity', 'c#', 'csharp'],
            'python': ['python'],
            'go': ['go'],
            'php': ['php'],
            'ruby': ['ruby'],
            'node': ['node', 'nodejs', 'node.js']
        }
        
    def normalize_language(self, lang):
        """Normalize language name to standard form."""
        lang_lower = lang.lower().strip()
        for standard_lang, variants in self.language_mappings.items():
            if lang_lower in variants:
                return standard_lang
        return lang_lower
        
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
    
    def extract_main_content(self, soup):
        """Extract the main documentation content from the page."""
        
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
                # Create a test copy to check content length
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
                # Create a test copy to check content length
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
        
        # Final fallback
        print("Using fallback selector: body")
        return soup.find('body')
    
    def clean_content(self, content):
        """Clean the content by removing unwanted elements."""
        return self.clean_content_intelligent(content)
    
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
    
    def detect_available_languages(self, soup):
        """Detect available programming languages in the documentation."""
        languages = set()
        
        # Look for common language indicators
        language_indicators = [
            ('swift', ['swift', 'ios', 'xcode']),
            ('kotlin', ['kotlin', 'android studio']),
            ('java', ['java']),
            ('web', ['web', 'javascript', 'npm', 'node.js']),
            ('dart', ['dart', 'flutter']),
            ('unity', ['unity', 'c#']),
            ('python', ['python', 'pip']),
            ('go', ['go', 'golang']),
            ('php', ['php']),
            ('ruby', ['ruby']),
            ('node', ['node.js', 'nodejs'])
        ]
        
        # Search in headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            text = heading.get_text().lower()
            for lang, indicators in language_indicators:
                if any(indicator in text for indicator in indicators):
                    languages.add(lang)
        
        # Search in code blocks and sections
        code_sections = soup.find_all(['code', 'pre'])
        for section in code_sections:
            text = section.get_text().lower()
            for lang, indicators in language_indicators:
                if any(indicator in text for indicator in indicators):
                    languages.add(lang)
        
        # Search in class names and data attributes
        for element in soup.find_all():
            classes = element.get('class', [])
            if isinstance(classes, list):
                class_text = ' '.join(classes).lower()
                for lang, indicators in language_indicators:
                    if any(indicator in class_text for indicator in indicators):
                        languages.add(lang)
        
        return sorted(list(languages))
    
    def filter_content_by_languages(self, content):
        """Filter content to show only selected language sections."""
        if not self.selected_languages or not content:
            return content
        
        # Create a copy to modify
        filtered_content = content.__copy__()
        
        # Find language-specific sections
        language_sections = []
        
        # Look for headings that indicate language sections
        headings = filtered_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading in headings:
            heading_text = heading.get_text().strip().lower()
            
            # Check if this heading is for a specific language
            matched_lang = None
            for selected_lang in self.selected_languages:
                lang_variants = self.language_mappings.get(selected_lang, [selected_lang])
                if any(variant in heading_text for variant in lang_variants):
                    matched_lang = selected_lang
                    break
            
            if matched_lang:
                # Keep this section
                language_sections.append((heading, matched_lang, True))
            else:
                # Check if this is a language section we should remove
                is_language_section = False
                for lang, variants in self.language_mappings.items():
                    if lang not in self.selected_languages:
                        if any(variant in heading_text for variant in variants):
                            is_language_section = True
                            break
                
                if is_language_section:
                    language_sections.append((heading, None, False))
        
        # Remove unwanted language sections
        for heading, lang, keep in language_sections:
            if not keep:
                # Find the content between this heading and the next heading of same level
                current_element = heading
                elements_to_remove = [heading]
                
                # Get all elements until next heading of same or higher level
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        # Check if this is same or higher level heading
                        current_level = int(heading.name[1])
                        sibling_level = int(sibling.name[1])
                        if sibling_level <= current_level:
                            break
                    elements_to_remove.append(sibling)
                
                # Remove all elements in this section
                for element in elements_to_remove:
                    if element.parent:
                        element.decompose()
        
        return filtered_content
    
    def get_key_press(self):
        """Get a single key press from user (cross-platform)."""
        try:
            if sys.platform == "win32":
                # Windows
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key == b'\xe0':  # Special key prefix on Windows
                            key = msvcrt.getch()
                            if key == b'H':  # Up arrow
                                return 'up'
                            elif key == b'P':  # Down arrow
                                return 'down'
                        elif key == b' ':  # Space
                            return 'space'
                        elif key == b'\r':  # Enter
                            return 'enter'
                        elif key == b'\x1b':  # Escape
                            return 'escape'
                        elif key in [b'q', b'Q']:
                            return 'quit'
            else:
                # Unix/Linux/Mac
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                    if key == '\x1b':  # Escape sequence
                        key += sys.stdin.read(2)
                        if key == '\x1b[A':  # Up arrow
                            return 'up'
                        elif key == '\x1b[B':  # Down arrow
                            return 'down'
                    elif key == ' ':  # Space
                        return 'space'
                    elif key == '\n' or key == '\r':  # Enter
                        return 'enter'
                    elif key == '\x1b':  # Escape
                        return 'escape'
                    elif key.lower() == 'q':
                        return 'quit'
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except:
            # Fallback to simple input if key detection fails
            return 'fallback'
        
        return None

    def clear_lines(self, num_lines):
        """Clear the last num_lines from terminal."""
        if num_lines <= 0:
            return
        try:
            if sys.platform == "win32":
                # Windows - Move cursor up and clear each line
                for _ in range(num_lines):
                    print('\033[1A\033[2K', end='', flush=True)  # Move up one line and clear it
            else:
                # Unix/Linux/Mac - Move up and clear from cursor to end
                print(f'\033[{num_lines}A\033[0J', end='', flush=True)
        except:
            # Fallback: just print newlines to push content up
            pass

    def get_colored_text(self, text, color_code):
        """Apply color to text with ANSI escape codes."""
        return f"\033[{color_code}m{text}\033[0m"

    def format_language_item(self, lang, is_current, is_selected):
        """Format a language item with appropriate colors and symbols."""
        # Color codes
        RESET = "0"
        BRIGHT_GREEN = "92"
        BRIGHT_BLUE = "94"
        BRIGHT_CYAN = "96"
        BRIGHT_YELLOW = "93"
        BRIGHT_MAGENTA = "95"
        WHITE_BG = "47"
        GREEN_BG = "42"
        BLUE_BG = "44"
        
        # Choose prefix and checkbox
        prefix = "→ " if is_current else "  "
        checkbox = "[✓] " if is_selected else "[ ] "
        
        # Apply colors based on state
        if is_current and is_selected:
            # Current item that is selected: bright green background with white text
            colored_prefix = self.get_colored_text(prefix, f"{GREEN_BG};97")
            colored_checkbox = self.get_colored_text(checkbox, f"{GREEN_BG};97")
            colored_lang = self.get_colored_text(lang.capitalize(), f"{GREEN_BG};97;1")
            return f"{colored_prefix}{colored_checkbox}{colored_lang}"
        elif is_current:
            # Current item not selected: blue background with white text
            colored_prefix = self.get_colored_text(prefix, f"{BLUE_BG};97")
            colored_checkbox = self.get_colored_text(checkbox, f"{BLUE_BG};97")
            colored_lang = self.get_colored_text(lang.capitalize(), f"{BLUE_BG};97;1")
            return f"{colored_prefix}{colored_checkbox}{colored_lang}"
        elif is_selected:
            # Selected item not current: bright green text
            colored_prefix = prefix
            colored_checkbox = self.get_colored_text(checkbox, BRIGHT_GREEN)
            colored_lang = self.get_colored_text(lang.capitalize(), f"{BRIGHT_GREEN};1")
            return f"{colored_prefix}{colored_checkbox}{colored_lang}"
        else:
            # Normal item: default colors
            return f"{prefix}{checkbox}{lang.capitalize()}"

    def interactive_language_selection(self, available_languages):
        """Allow user to interactively select languages with arrow key navigation."""
        if not available_languages:
            print("No specific programming languages detected in this documentation.")
            return []
        
        print(f"\n🔧 Select programming languages for this documentation:\n")
        
        # Check if we can use interactive mode
        can_use_interactive = True
        try:
            if sys.platform == "win32":
                import msvcrt
            else:
                import termios, tty
        except ImportError:
            can_use_interactive = False
        
        if not can_use_interactive:
            # Fallback to old method
            return self.fallback_language_selection(available_languages)
        
        current_index = 0
        selected = set()  # Track selected languages
        last_menu_lines = 0  # Track how many lines the last menu took
        
        def display_menu():
            """Display the current menu state with colors."""
            nonlocal last_menu_lines
            menu_lines = 0
            
            # Display language options
            for i, lang in enumerate(available_languages):
                is_current = i == current_index
                is_selected = lang in selected
                formatted_item = self.format_language_item(lang, is_current, is_selected)
                print(formatted_item)
                menu_lines += 1
            
            # Empty line before controls
            print()
            menu_lines += 1
            
            # Display controls
            print(f"💡 Controls:")
            menu_lines += 1
            controls_text = "   ↑/↓  Navigate    SPACE  Select/Deselect    ENTER  Confirm"
            print(self.get_colored_text(controls_text, "96"))  # Bright cyan
            menu_lines += 1
            
            # Display status
            if selected:
                selected_langs = ', '.join(sorted(selected))
                selected_text = f"   Selected: {selected_langs}"
                print(self.get_colored_text(selected_text, "92;1"))  # Bright green bold
            else:
                help_text = "   No languages selected (will include all if you press ENTER)"
                print(self.get_colored_text(help_text, "93"))  # Bright yellow
            menu_lines += 1
            
            last_menu_lines = menu_lines
            return menu_lines
        
        # Initial display
        display_menu()
        
        while True:
            try:
                key = self.get_key_press()
                
                if key == 'fallback':
                    # Clear display and use fallback
                    self.clear_lines(last_menu_lines)
                    return self.fallback_language_selection(available_languages)
                
                # Clear previous menu (only the exact number of lines we used)
                self.clear_lines(last_menu_lines)
                
                if key == 'up':
                    current_index = (current_index - 1) % len(available_languages)
                elif key == 'down':
                    current_index = (current_index + 1) % len(available_languages)
                elif key == 'space':
                    current_lang = available_languages[current_index]
                    if current_lang in selected:
                        selected.remove(current_lang)
                    else:
                        selected.add(current_lang)
                elif key == 'enter':
                    if selected:
                        result = sorted(list(selected))
                        success_msg = f"✅ Selected languages: {', '.join(lang.capitalize() for lang in result)}"
                        print(self.get_colored_text(success_msg, "92;1"))  # Bright green bold
                        print()  # Empty line
                        return result
                    else:
                        success_msg = f"✅ No languages selected - including all languages"
                        print(self.get_colored_text(success_msg, "93;1"))  # Bright yellow bold
                        print()  # Empty line
                        return available_languages
                elif key in ['escape', 'quit']:
                    cancel_msg = f"❌ Operation cancelled."
                    print(self.get_colored_text(cancel_msg, "91;1"))  # Bright red bold
                    print()  # Empty line
                    return []
                
                # Redisplay menu
                display_menu()
                
            except KeyboardInterrupt:
                cancel_msg = f"❌ Operation cancelled."
                print(self.get_colored_text(cancel_msg, "91;1"))  # Bright red bold
                print()  # Empty line
                return []
            except Exception as e:
                # Clear display and use fallback
                self.clear_lines(last_menu_lines)
                warning_msg = f"⚠️  Interactive mode failed ({e}), using fallback..."
                print(self.get_colored_text(warning_msg, "93;1"))  # Bright yellow bold
                return self.fallback_language_selection(available_languages)
    
    def fallback_language_selection(self, available_languages):
        """Fallback language selection method for when interactive mode fails."""
        print(f"🔧 Available programming languages in this documentation:")
        for i, lang in enumerate(available_languages, 1):
            print(f"  {i}. {lang.capitalize()}")
        
        print(f"\n📝 Options:")
        print(f"  • Enter numbers (e.g., '1 3 5') to select specific languages")
        print(f"  • Enter 'all' to include all languages")
        print(f"  • Press Enter to include all languages")
        
        while True:
            try:
                selection = input("\nYour choice: ").strip().lower()
                
                if not selection or selection == 'all':
                    return available_languages
                
                # Parse number selection
                selected_indices = []
                for part in selection.split():
                    if part.isdigit():
                        idx = int(part) - 1
                        if 0 <= idx < len(available_languages):
                            selected_indices.append(idx)
                        else:
                            print(f"Invalid selection: {part}. Please choose numbers between 1 and {len(available_languages)}.")
                            break
                    else:
                        print(f"Invalid input: '{part}'. Please enter numbers or 'all'.")
                        break
                else:
                    # All selections were valid
                    if selected_indices:
                        selected_languages = [available_languages[i] for i in selected_indices]
                        print(f"Selected languages: {', '.join(lang.capitalize() for lang in selected_languages)}")
                        return selected_languages
                    else:
                        print("No valid selections made. Including all languages.")
                        return available_languages
                        
            except KeyboardInterrupt:
                print("\n\nOperation cancelled.")
                return []
            except Exception as e:
                print(f"Error: {e}. Please try again.")
    
    def convert_to_markdown(self, html_content, title):
        """Convert HTML content to Markdown."""
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
        
        # Fix code blocks: Replace [code] and [/code] with proper markdown code fences
        markdown_content = re.sub(r'\[code\]\s*', '```\n', markdown_content, flags=re.IGNORECASE)
        markdown_content = re.sub(r'\s*\[/code\]', '\n```', markdown_content, flags=re.IGNORECASE)
        
        # Fix inline code patterns that might have been converted incorrectly
        markdown_content = re.sub(r'\[code\]([^\n]*?)\[/code\]', r'`\1`', markdown_content, flags=re.IGNORECASE)
        
        # Clean up any remaining malformed code block patterns
        markdown_content = re.sub(r'```\s*\n\s*```', '```\n\n```', markdown_content)
        
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
    
    def extract_and_save(self, url, output_dir=".", interactive=False):
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
        
        # Extract main content
        main_content = self.extract_main_content(soup)
        if not main_content:
            print("No main content found!")
            return False
        
        # Detect available languages
        available_languages = self.detect_available_languages(soup)
        if available_languages:
            print(f"Detected languages: {', '.join(lang.capitalize() for lang in available_languages)}")
        
        # Handle language selection
        if interactive and available_languages:
            self.selected_languages = self.interactive_language_selection(available_languages)
        elif self.selected_languages and available_languages:
            # Normalize user-provided languages
            normalized_languages = []
            for lang in self.selected_languages:
                normalized = self.normalize_language(lang)
                if normalized in available_languages:
                    normalized_languages.append(normalized)
                else:
                    print(f"Warning: Language '{lang}' not found in documentation. Available: {', '.join(available_languages)}")
            self.selected_languages = normalized_languages
        elif available_languages and not self.selected_languages:
            # Auto-prompt for language selection when no languages specified
            self.selected_languages = self.interactive_language_selection(available_languages)
        
        # Filter content by selected languages
        if self.selected_languages:
            print(f"Filtering content for: {', '.join(lang.capitalize() for lang in self.selected_languages)}")
            main_content = self.filter_content_by_languages(main_content)
        
        # Clean content
        cleaned_content = self.clean_content(main_content)
        
        # Convert to Markdown
        markdown = self.convert_to_markdown(cleaned_content, title)
        
        # Generate filename
        filename = self.generate_filename(url, title)
        
        # Add language suffix to filename if filtering
        if self.selected_languages:
            lang_suffix = "-" + "-".join(self.selected_languages)
            name, ext = os.path.splitext(filename)
            filename = f"{name}{lang_suffix}{ext}"
        
        filepath = os.path.join(output_dir, filename)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
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
        description="Extract Firebase documentation and convert to Markdown with language filtering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract documentation with interactive language selection
  python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
  
  # Extract only Swift and Web examples (skip interactive selection)
  python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" --languages swift web
  
  # Force interactive language selection (same as default behavior)
  python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" --interactive
  
  # Save to specific directory with language filtering
  python firebase_docs_extractor.py "https://firebase.google.com/docs/auth" --languages kotlin java --output ./docs

Supported languages: swift, kotlin, java, web, dart, unity, python, go, php, ruby, node
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
    
    parser.add_argument(
        '-l', '--languages',
        nargs='*',
        help='Specific programming languages to include (e.g., swift web kotlin). If not specified, you will be prompted to select languages interactively.'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Interactively select languages after fetching the documentation'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: Please provide a valid URL starting with http:// or https://")
        sys.exit(1)
    
    # Validate language options
    if args.languages and args.interactive:
        print("Error: Cannot use both --languages and --interactive options together")
        sys.exit(1)
    
    # Extract documentation
    extractor = FirebaseDocsExtractor(selected_languages=args.languages or [])
    success = extractor.extract_and_save(args.url, args.output, interactive=args.interactive)
    
    if success:
        print("✅ Documentation extracted successfully!")
    else:
        print("❌ Failed to extract documentation")
        sys.exit(1)


if __name__ == "__main__":
    main()
