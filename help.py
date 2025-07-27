#!/usr/bin/env python3
"""
Help and Examples for Firebase Documentation Extractor with Language Filtering
"""

def show_help():
    """Display comprehensive help information."""
    
    help_text = """
🔥 Firebase Documentation Extractor - Help & Examples
=====================================================

DESCRIPTION:
    A Python tool that extracts Firebase documentation from URLs and converts 
    them into clean Markdown files with support for programming language filtering.

BASIC USAGE:
    python firebase_docs_extractor.py <URL> [OPTIONS]

LANGUAGE FILTERING EXAMPLES:
    # Extract complete documentation (all languages)
    python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
    
    # Extract only Swift and Web examples
    python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" --languages swift web
    
    # Extract mobile platforms only
    python firebase_docs_extractor.py "https://firebase.google.com/docs/auth" --languages swift kotlin dart
    
    # Interactive language selection
    python firebase_docs_extractor.py "https://firebase.google.com/docs/firestore/quickstart" --interactive
    
    # Single language with custom output directory
    python firebase_docs_extractor.py "https://firebase.google.com/docs/functions" --languages web --output ./docs

SUPPORTED LANGUAGES:
    • swift      - iOS development with Xcode
    • kotlin     - Android development  
    • java       - Android development
    • web        - JavaScript/Web development
    • dart       - Flutter development
    • unity      - Unity game development
    • python     - Python development
    • go         - Go development
    • php        - PHP development
    • ruby       - Ruby development
    • node       - Node.js development

USEFUL FIREBASE DOCUMENTATION URLS:

📚 Getting Started:
    • General: https://firebase.google.com/docs/guides
    • Web: https://firebase.google.com/docs/web/setup
    • iOS: https://firebase.google.com/docs/ios/setup
    • Android: https://firebase.google.com/docs/android/setup

🤖 AI/ML:
    • AI Logic: https://firebase.google.com/docs/ai-logic/get-started?api=vertex
    • Gemini API: https://firebase.google.com/docs/ai-logic/get-started?api=gemini
    • Image Generation: https://firebase.google.com/docs/ai-logic/generate-images-imagen

🔐 Authentication:
    • Web Start: https://firebase.google.com/docs/auth/web/start
    • Email/Password: https://firebase.google.com/docs/auth/web/password-auth
    • Google Sign-In: https://firebase.google.com/docs/auth/web/google-signin
    • Multi-factor: https://firebase.google.com/docs/auth/web/multi-factor

🗄️ Database:
    • Firestore: https://firebase.google.com/docs/firestore/quickstart
    • Realtime Database: https://firebase.google.com/docs/database/web/start
    • Firestore Security: https://firebase.google.com/docs/firestore/security/get-started

⚡ Functions:
    • Get Started: https://firebase.google.com/docs/functions/get-started
    • Write Functions: https://firebase.google.com/docs/functions/write-firebase-functions
    • HTTP Functions: https://firebase.google.com/docs/functions/http-events

🌐 Hosting:
    • Quickstart: https://firebase.google.com/docs/hosting/quickstart
    • Custom Domain: https://firebase.google.com/docs/hosting/custom-domain

📱 Cloud Messaging:
    • Web: https://firebase.google.com/docs/cloud-messaging/js/client
    • iOS: https://firebase.google.com/docs/cloud-messaging/ios/client
    • Android: https://firebase.google.com/docs/cloud-messaging/android/client

📊 Analytics:
    • Get Started: https://firebase.google.com/docs/analytics/get-started
    • Events: https://firebase.google.com/docs/analytics/events

💾 Storage:
    • Web: https://firebase.google.com/docs/storage/web/start
    • Upload Files: https://firebase.google.com/docs/storage/web/upload-files

COMMAND LINE OPTIONS:
    URL                         Firebase documentation URL to extract (required)
    -l, --languages LANG [...]  Specific programming languages to include
    -i, --interactive           Interactively select languages after fetching
    -o, --output DIR            Output directory for Markdown file (default: current directory)
    -h, --help                  Show help message

LANGUAGE FILTERING BENEFITS:
    📄 Smaller, focused files (e.g., 107 lines vs 471 lines for complete docs)
    🎯 Only relevant code examples for your platform
    📁 Organized by language with automatic filename suffixes
    ⚡ Faster reading and implementation

WINDOWS USERS:
    Use the included batch script for easier execution:
    extract_docs.bat "https://firebase.google.com/docs/..." "swift web"

OUTPUT:
    The tool creates Markdown files with:
    • Clean, formatted content with language-specific examples only
    • Source URL and extraction timestamp
    • Meaningful filename with language suffix (e.g., file-swift-web.md)
    • Preserved code blocks and formatting

CONTENT SIZE COMPARISON:
    Complete docs:    471 lines (all languages)
    Swift + Web:      176 lines (2 languages)
    Kotlin only:      107 lines (1 language)

TROUBLESHOOTING:
    • Ensure you have an internet connection
    • Check that the URL is accessible in a web browser
    • Verify all dependencies are installed: pip install -r requirements.txt
    • For Windows PowerShell, use quotes around URLs with special characters
    • Use --interactive to see what languages are available in a document

REPOSITORY:
    https://github.com/kavinduUdhara/extract-data-from-firebase-documenations
"""
    
    print(help_text)

if __name__ == "__main__":
    show_help()
