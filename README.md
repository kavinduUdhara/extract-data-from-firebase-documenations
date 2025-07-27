# Firebase Documentation Extractor

🔥 A powerful Python tool to extract Firebase documentation from URLs and convert them to clean Markdown format with intelligent language filtering.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🤖 Why This Tool Exists

**Problem**: Most AI models (ChatGPT, GitHub Copilot, etc.) don't have access to the latest Firebase documentation. Firebase is a rapidly evolving platform with frequent updates, new features, and API changes. This creates a gap when trying to implement modern Firebase applications with AI assistance.

**Solution**: This tool extracts the latest Firebase documentation in a clean, AI-friendly format that you can:
- 📋 **Copy-paste into AI conversations** for accurate, up-to-date context
- 🧠 **Feed into AI models** as reference material for code generation
- 📚 **Use as training data** or examples for your AI workflows
- 🔄 **Keep synchronized** with Firebase's latest features and changes

**Result**: Get accurate, current Firebase implementation guidance from AI models using the latest official documentation!

## ✨ Features

- 🌐 **Web Scraping**: Extracts content from Firebase documentation URLs
- 📝 **Markdown Conversion**: Converts HTML to clean, formatted Markdown
- 🎯 **Language Filtering**: Selectively include specific programming languages (Swift, Kotlin, Java, Web, Dart, Unity, Python, Go, PHP, Ruby, Node.js)
- 🎨 **Interactive Selection**: Beautiful color-coded arrow key navigation for language selection
- 🧹 **Smart Content Cleaning**: Removes navigation, ads, and irrelevant content
- 📦 **Proper Code Blocks**: Converts code snippets to standard markdown format with triple backticks
- 🚀 **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎥 Demo

The tool features an interactive language selection interface with:
- **↑/↓** Arrow key navigation
- **Space** to select/deselect languages
- **Enter** to confirm selection
- **Beautiful colors** for better visual feedback

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kavinduUdhara/extract-data-from-firebase-documenations.git
   cd extract-data-from-firebase-documenations
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

```bash
# Extract with interactive language selection (default)
python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"

# Extract specific languages only
python firebase_docs_extractor.py "https://firebase.google.com/docs/auth" --languages swift kotlin

# Save to specific directory
python firebase_docs_extractor.py "https://firebase.google.com/docs/firestore" --output ./docs
```

## 🤖 AI Integration Use Cases

### Perfect for AI Development Workflows
```bash
# Extract latest Firebase Auth documentation for AI context
python firebase_docs_extractor.py "https://firebase.google.com/docs/auth/web/start" --languages web

# Get current Firestore examples for your preferred language
python firebase_docs_extractor.py "https://firebase.google.com/docs/firestore/quickstart" --languages swift

# Extract comprehensive AI Logic documentation for modern AI features
python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
```

**How to use with AI models:**
1. 📄 Extract the latest documentation for your Firebase feature
2. 📋 Copy the relevant sections from the generated Markdown
3. 🤖 Paste into ChatGPT, Claude, or GitHub Copilot with your question
4. ✨ Get accurate answers based on current Firebase documentation!

Example prompt:
```
Based on this latest Firebase documentation:
[paste extracted markdown here]

Help me implement Firebase Authentication in my React app with error handling.
```

## 📚 Usage Examples

### Interactive Language Selection
```bash
python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
```
This will show an interactive menu where you can:
- Navigate with arrow keys
- Select languages with space bar
- Confirm with Enter

### Pre-selected Languages
```bash
# Extract only Swift and Web examples
python firebase_docs_extractor.py "https://firebase.google.com/docs/auth" --languages swift web

# Extract multiple languages
python firebase_docs_extractor.py "https://firebase.google.com/docs/firestore" --languages kotlin java dart
```

### Advanced Options
```bash
# Force interactive mode (same as default)
python firebase_docs_extractor.py "URL" --interactive

# Custom output directory
python firebase_docs_extractor.py "URL" --languages web --output ./my-docs
```

## 🎯 Supported Languages

The tool can detect and filter the following programming languages:

| Language | Aliases | Example Use Case |
|----------|---------|------------------|
| **Swift** | `swift`, `ios` | iOS app development |
| **Kotlin** | `kotlin`, `android` | Android app development |
| **Java** | `java` | Android/Server development |
| **Web** | `web`, `javascript`, `js` | Web development |
| **Dart** | `dart`, `flutter` | Flutter development |
| **Unity** | `unity`, `c#`, `csharp` | Game development |
| **Python** | `python` | Server-side development |
| **Go** | `go`, `golang` | Server-side development |
| **PHP** | `php` | Web backend development |
| **Ruby** | `ruby` | Web development |
| **Node.js** | `node`, `nodejs` | Server-side JavaScript |

## 📖 Command Line Options

```
python firebase_docs_extractor.py <URL> [OPTIONS]

Arguments:
  URL                   Firebase documentation URL to extract

Options:
  -l, --languages       Specific languages to include (e.g., swift web kotlin)
  -i, --interactive     Force interactive language selection
  -o, --output          Output directory for the Markdown file (default: current directory)
  -h, --help           Show help message and exit

Examples:
  python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
  python firebase_docs_extractor.py "URL" --languages swift web
  python firebase_docs_extractor.py "URL" --output ./docs --languages kotlin
```

## 🛠️ How It Works

1. **Content Extraction**: Uses intelligent selectors to find main documentation content
2. **Language Detection**: Scans headings, code blocks, and class names to identify available languages
3. **Interactive Selection**: Presents a color-coded menu for language selection
4. **Content Filtering**: Removes sections for unselected languages
5. **Markdown Conversion**: Converts HTML to clean Markdown with proper code block formatting
6. **File Generation**: Saves with descriptive filenames including selected languages

## 📁 Project Structure

```
extract-data-from-firebase-documenations/
├── firebase_docs_extractor.py    # Main extractor script
├── requirements.txt               # Python dependencies
├── extract_docs.bat              # Windows batch script
├── example_usage.py              # Usage examples
├── help.py                       # Help and documentation
├── ENHANCEMENT_SUMMARY.md        # Feature documentation
├── examples/                     # Sample extracted files
│   ├── ai-logic-get-started-api-vertex-web.md
│   └── ai-logic-get-started-api-vertex.md
└── README.md                     # This file
```

## 🎨 Color Scheme

The interactive interface features:
- **Blue highlight**: Current navigation position
- **Green highlight**: Current position when selected
- **Green text**: Selected languages
- **Cyan text**: Control instructions
- **Yellow text**: Help messages
- **Red text**: Error messages

## ⚡ Performance

- **Content Extraction**: 6.9x improvement over basic extraction (68 → 471 lines)
- **Language Filtering**: Up to 77% size reduction when filtering specific languages
- **Smart Cleaning**: Removes navigation and irrelevant content while preserving documentation

## 🌟 Open Source Philosophy

This tool is **100% open source** and built for the community! 

**Why Open Source?**
- 🤝 **Community-Driven**: Everyone benefits from improvements and new features
- 🔍 **Transparency**: You can see exactly how your documentation is processed
- 🚀 **Innovation**: Developers can extend and customize for their specific needs
- 📚 **Learning**: Study the code to understand web scraping and content extraction
- 🔧 **Reliability**: Community testing ensures robustness across different systems

**Built by developers, for developers** - because keeping up with Firebase's rapid evolution shouldn't be a barrier to building great applications with AI assistance.

## 🤝 Contributing

We welcome contributions from the community! Whether you're:
- 🐛 **Fixing bugs** in content extraction
- ✨ **Adding new features** like support for more languages
- 📚 **Improving documentation** and examples
- 🎨 **Enhancing the UI** with better colors or interactions
- 🔧 **Optimizing performance** for faster extraction

Every contribution helps make Firebase development more accessible to everyone.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Firebase team for their comprehensive and regularly updated documentation
- BeautifulSoup and html2text libraries for excellent HTML processing
- The AI/ML community for highlighting the need for current documentation in AI workflows
- Open source contributors who help make this tool better

## 📧 Support

If you encounter any issues or have questions:
1. Check the [examples](./examples/) directory for sample outputs
2. Review the [ENHANCEMENT_SUMMARY.md](./ENHANCEMENT_SUMMARY.md) for detailed features
3. Open an issue on GitHub with details about your use case

**Special thanks to the AI development community** - this tool exists because we all face the same challenge of keeping AI models updated with the latest Firebase features!

---

**Made with ❤️ for the Firebase developer community**  
**Bridging the gap between Firebase's rapid innovation and AI-assisted development** 🔥🤖
