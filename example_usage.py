"""
Example usage script for Firebase Documentation Extractor with Language Filtering

This script demonstrates how to use the firebase_docs_extractor tool with language filtering.
"""

import subprocess
import sys
import os

def run_extractor(url, output_dir="./extracted_docs", languages=None, interactive=False):
    """Run the Firebase docs extractor with the given parameters."""
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get the Python executable path
    python_exe = "F:/repos/extract-data-from-firebase-documenations/.venv/Scripts/python.exe"
    
    # Build command
    cmd = [python_exe, "firebase_docs_extractor.py", url, "--output", output_dir]
    
    if interactive:
        cmd.append("--interactive")
    elif languages:
        cmd.extend(["--languages"] + languages)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    # Example URLs to test
    test_url = "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
    
    if len(sys.argv) > 1:
        # Use URL provided as command line argument
        url = sys.argv[1]
        
        print("🔥 Firebase Documentation Extractor - Examples")
        print("=" * 50)
        
        print(f"\n1. Extract complete documentation:")
        success = run_extractor(url)
        
        print(f"\n2. Extract only Swift and Web examples:")
        success = run_extractor(url, "./extracted_docs", languages=["swift", "web"])
        
        print(f"\n3. Extract only mobile platforms:")
        success = run_extractor(url, "./extracted_docs", languages=["swift", "kotlin", "dart"])
        
        if success:
            print("\n✅ All extractions completed successfully!")
        else:
            print("\n❌ Some extractions failed!")
    else:
        print("🔥 Firebase Documentation Extractor - Usage Examples")
        print("=" * 55)
        print(f"\nUsage: python example_usage.py <firebase_docs_url>")
        print(f"\nExample commands you can try:")
        print(f"\n1. Complete documentation:")
        print(f"   python firebase_docs_extractor.py \"{test_url}\"")
        print(f"\n2. Only Swift and Web examples:")
        print(f"   python firebase_docs_extractor.py \"{test_url}\" --languages swift web")
        print(f"\n3. Interactive language selection:")
        print(f"   python firebase_docs_extractor.py \"{test_url}\" --interactive")
        print(f"\n4. Mobile platforms only:")
        print(f"   python firebase_docs_extractor.py \"{test_url}\" --languages swift kotlin dart")
        print(f"\n5. Save to specific directory:")
        print(f"   python firebase_docs_extractor.py \"{test_url}\" --languages web --output ./docs")
        print(f"\nSupported languages: swift, kotlin, java, web, dart, unity, python, go, php, ruby, node")
