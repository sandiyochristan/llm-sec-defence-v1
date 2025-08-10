#!/usr/bin/env python3
"""
Red Teaming LLM Security Lab Setup Script
=========================================

This script sets up a Flask-based chat application using Microsoft DialoGPT-medium
for LLM security research and Red Teaming purposes.

Features:
- CPU-optimized model loading
- 2048 token context window (2x GPT-2 limit)
- Simple web interface for security testing
- Suitable for Red Teaming lab environments

Usage:
    python setup.py install  # Install dependencies
    python app.py           # Run the application
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def check_model_availability():
    """Check if the model can be downloaded"""
    print("Checking model availability...")
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        print("✅ Model is available for download!")
        return True
    except Exception as e:
        print(f"❌ Error checking model: {e}")
        return False

def main():
    """Main setup function"""
    print("🔒 Red Teaming LLM Security Lab Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check model availability
    if not check_model_availability():
        print("⚠️  Model availability check failed, but you can still try running the app")
    
    print("\n🎉 Setup complete!")
    print("\nTo run the application:")
    print("  python app.py")
    print("\nThe application will be available at: http://localhost:5000")
    print("\n⚠️  Security Notice:")
    print("  This is a Red Teaming lab environment for security research only.")
    print("  Do not use for malicious purposes.")

if __name__ == "__main__":
    main()
