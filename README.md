# Firebase Documentation Extractor

A Python tool that extracts data from Google Firebase documentation URLs and converts them into clean Markdown format with support for programming language filtering.

## Features

- ✅ Extracts main content from Firebase documentation pages
- ✅ Converts HTML to clean Markdown format
- ✅ Removes navigation, ads, and other unwanted elements
- ✅ **🆕 Language filtering** - Extract only specific programming language examples
- ✅ **🆕 Interactive language selection** - Choose languages after seeing what's available
- ✅ Generates meaningful filenames based on URL structure and selected languages
- ✅ Adds metadata (source URL, extraction date) to output files
- ✅ Supports command-line usage with customizable output directory

## Installation

1. Clone this repository:
```bash
git clone https://github.com/kavinduUdhara/extract-data-from-firebase-documenations.git
cd extract-data-from-firebase-documenations
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Extract complete documentation:
```bash
python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
```

### Language Filtering

Extract only specific programming languages:
```bash
# Swift and Web examples only
python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" --languages swift web

# Mobile platforms only
python firebase_docs_extractor.py "https://firebase.google.com/docs/auth/web/start" --languages swift kotlin dart

# Single language
python firebase_docs_extractor.py "https://firebase.google.com/docs/firestore/quickstart" --languages web
```

### Interactive Language Selection

Let the tool detect available languages and choose interactively:
```bash
python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" --interactive
```

### Custom Output Directory

```bash
python firebase_docs_extractor.py "https://firebase.google.com/docs/auth/web/start" --languages kotlin java --output ./extracted_docs
```

### Windows Batch Script

For Windows users:
```cmd
# Complete documentation
extract_docs.bat "https://firebase.google.com/docs/firestore/quickstart"

# With language filtering
extract_docs.bat "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" "swift web"
```

## Supported Languages

- **swift** (iOS development)
- **kotlin** (Android development)  
- **java** (Android development)
- **web** (JavaScript/Web development)
- **dart** (Flutter development)
- **unity** (Unity game development)
- **python** (Python development)
- **go** (Go development)
- **php** (PHP development)
- **ruby** (Ruby development)
- **node** (Node.js development)

## Examples

Here are some Firebase documentation URLs you can try:

- AI/ML: `https://firebase.google.com/docs/ai-logic/get-started?api=vertex`
- Authentication: `https://firebase.google.com/docs/auth/web/start`
- Firestore: `https://firebase.google.com/docs/firestore/quickstart`
- Realtime Database: `https://firebase.google.com/docs/database/web/start`
- Cloud Functions: `https://firebase.google.com/docs/functions/get-started`
- Hosting: `https://firebase.google.com/docs/hosting/quickstart`

## Output Examples

### Complete Documentation
```
ai-logic-get-started-api-vertex.md (471 lines)
```

### Language Filtered
```
ai-logic-get-started-api-vertex-swift-web.md (176 lines)
ai-logic-get-started-api-vertex-kotlin.md (107 lines)
```

The tool generates Markdown files with:
- Clean, formatted content
- Source URL reference
- Extraction timestamp
- Proper heading structure
- Preserved code blocks and formatting
- **Language-specific content only** (when filtering is used)

## Command Line Options

```
python firebase_docs_extractor.py <url> [options]

Options:
  -l, --languages LANG [LANG ...]  Specific programming languages to include
  -i, --interactive               Interactively select languages after fetching
  -o, --output DIR               Output directory (default: current directory)
  -h, --help                     Show help message
```

## Dependencies

- `requests` - For HTTP requests
- `beautifulsoup4` - For HTML parsing
- `html2text` - For HTML to Markdown conversion
- `lxml` - For fast XML/HTML processing

## Requirements

- Python 3.7+
- Internet connection for fetching documentation

## License

This project is open source and available under the MIT License.
