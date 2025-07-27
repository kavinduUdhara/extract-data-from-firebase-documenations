#!/usr/bin/env python3
"""
Quick test for the fixed interactive interface
"""

import os
from firebase_docs_extractor import FirebaseDocsExtractor

def test_fixed_interface():
    print("=" * 60)
    print("🔥 FIREBASE DOCUMENTATION EXTRACTOR TEST")
    print("=" * 60)
    print("Testing the FIXED interactive language selection...")
    print("The menu should NOT erase the lines above!")
    print("=" * 60)
    
    # Mock some languages for testing
    available_languages = ['dart', 'go', 'java', 'kotlin', 'swift', 'unity', 'web']
    
    extractor = FirebaseDocsExtractor()
    
    print("\n🎨 About to show the FIXED interactive menu...")
    print("✅ Content above should stay visible!")
    print("🎯 Use arrow keys to navigate, space to select, enter to confirm")
    
    try:
        selected_languages = extractor.interactive_language_selection(available_languages)
        print(f"\n🎉 Test completed! You selected: {selected_languages}")
        print("✅ Success: Content above the menu should still be visible!")
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_fixed_interface()
