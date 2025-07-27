# Configuration file for Firebase Documentation Extractor

# Output settings
DEFAULT_OUTPUT_DIR = "./extracted_docs"

# HTTP settings
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Content extraction settings
CONTENT_SELECTORS = [
    'main[role="main"]',
    'main',
    '.devsite-article-body',
    '.devsite-main-content',
    'article',
    '.documentation-content',
    '#main-content'
]

# Elements to remove during cleaning
UNWANTED_CLASSES = [
    'devsite-nav',
    'devsite-footer',
    'devsite-header',
    'banner',
    'advertisement',
    'breadcrumb',
    'table-of-contents',
    'feedback',
    'devsite-page-navigation'
]

UNWANTED_TAGS = ['script', 'style', 'nav', 'header', 'footer']

# Markdown conversion settings
HTML2TEXT_CONFIG = {
    'ignore_links': False,
    'ignore_images': False,
    'ignore_emphasis': False,
    'body_width': 0,  # Don't wrap lines
    'unicode_snob': True
}
