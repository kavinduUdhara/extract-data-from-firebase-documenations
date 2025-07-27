#!/usr/bin/env python3
"""
Test script for Firebase Documentation Extractor
"""

import os
import sys
from firebase_docs_extractor import FirebaseDocsExtractor

def test_extraction():
    """Test the extraction functionality with a sample URL."""
    
    # Test URL
    test_url = "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
    
    print("🧪 Testing Firebase Documentation Extractor")
    print(f"📄 Test URL: {test_url}")
    print("-" * 50)
    
    # Create extractor instance
    extractor = FirebaseDocsExtractor()
    
    # Test extraction
    success = extractor.extract_and_save(test_url, "./test_output")
    
    if success:
        print("\n✅ Test passed! Documentation extracted successfully.")
        
        # Check if file was created
        expected_filename = "ai-logic-get-started-api-vertex.md"
        expected_path = os.path.join("./test_output", expected_filename)
        
        if os.path.exists(expected_path):
            file_size = os.path.getsize(expected_path)
            print(f"📁 File created: {expected_path}")
            print(f"📊 File size: {file_size} bytes")
            
            # Show first few lines
            with open(expected_path, 'r', encoding='utf-8') as f:
                first_lines = f.readlines()[:10]
            
            print("\n📖 First few lines of extracted content:")
            print("=" * 40)
            for line in first_lines:
                print(line.rstrip())
            print("=" * 40)
            
        else:
            print(f"⚠️  Expected file not found: {expected_path}")
            
    else:
        print("\n❌ Test failed! Could not extract documentation.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = test_extraction()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        sys.exit(1)
