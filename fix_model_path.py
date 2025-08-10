#!/usr/bin/env python3
"""
Helper script to fix model path issues
Finds the downloaded Llama2 model and creates proper symlinks
"""

import os
import glob

def find_model_file():
    """Find the downloaded Llama2 model file"""
    print("🔍 Searching for Llama2 model file...")
    
    # Common locations to search
    search_paths = [
        "./models/",
        "/home/user/models/",
        os.path.expanduser("~/models/"),
        os.path.expanduser("~/.cache/huggingface/hub/"),
        "./",
    ]
    
    # File patterns to look for
    file_patterns = [
        "llama-2-7b-chat.Q4_K_M.gguf",
        "llama-2-7b-chat.gguf",
        "*.gguf"
    ]
    
    found_files = []
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            print(f"Searching in: {search_path}")
            for pattern in file_patterns:
                pattern_path = os.path.join(search_path, pattern)
                matches = glob.glob(pattern_path)
                for match in matches:
                    if os.path.isfile(match) and match.endswith('.gguf'):
                        found_files.append(match)
                        print(f"✅ Found: {match}")
    
    return found_files

def create_symlink(model_path):
    """Create a symlink to the model file"""
    print(f"\n🔗 Creating symlink to: {model_path}")
    
    # Create symlink in current directory
    symlink_path = "./llama-2-7b-chat.gguf"
    
    # Remove existing symlink if it exists
    if os.path.exists(symlink_path):
        if os.path.islink(symlink_path):
            os.unlink(symlink_path)
            print(f"Removed existing symlink: {symlink_path}")
        else:
            os.remove(symlink_path)
            print(f"Removed existing file: {symlink_path}")
    
    try:
        # Create symlink using absolute paths
        abs_model_path = os.path.abspath(model_path)
        abs_symlink_path = os.path.abspath(symlink_path)
        
        os.symlink(abs_model_path, abs_symlink_path)
        print(f"✅ Created symlink: {symlink_path} -> {abs_model_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating symlink: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Llama2 Model Path Fixer")
    print("=" * 40)
    
    # Find model files
    model_files = find_model_file()
    
    if not model_files:
        print("❌ No Llama2 model files found!")
        print("\nPlease ensure the model is downloaded. You can:")
        print("1. Run: python setup_model.py")
        print("2. Or manually download from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF")
        return
    
    # Use the first found model file
    model_path = model_files[0]
    print(f"\n🎯 Using model: {model_path}")
    
    # Create symlink
    if create_symlink(model_path):
        print("\n✅ Model path fixed successfully!")
        print("You can now run: python app.py")
    else:
        print("\n❌ Failed to create symlink")
        print(f"Model is available at: {model_path}")
        print("You can manually create a symlink or copy the file to ./llama-2-7b-chat.gguf")

if __name__ == "__main__":
    main()
