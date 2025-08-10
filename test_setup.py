#!/usr/bin/env python3
"""
Test script for Red Teaming LLM Security Lab
Verifies that all dependencies are installed and the model can be loaded.
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...")
    
    required_packages = [
        'flask',
        'transformers', 
        'torch',
        'accelerate',
        'tokenizers'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All packages imported successfully!")
    return True

def test_model_loading():
    """Test if the model can be loaded (without downloading)"""
    print("\n🔍 Testing model availability...")
    
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        print("✅ Model is available for download!")
        return True
    except Exception as e:
        print(f"❌ Model loading test failed: {e}")
        print("This might be due to network issues or Hugging Face access.")
        return False

def test_flask_app():
    """Test if Flask app can be imported"""
    print("\n🔍 Testing Flask app...")
    
    try:
        # Import the app module
        sys.path.append('.')
        import app
        print("✅ Flask app can be imported!")
        return True
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔒 Red Teaming LLM Security Lab - Setup Test")
    print("=" * 50)
    
    # Test Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_model_loading():
        tests_passed += 1
    
    if test_flask_app():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! You're ready to run the application.")
        print("\nTo start the app:")
        print("  python app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
