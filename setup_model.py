#!/usr/bin/env python3
"""
Setup script for Llama2 7B Chat GGUF model
Downloads and configures the model for Red Teaming use
"""

import os
import sys
from pathlib import Path

def download_model():
    """Download the Llama2 7B Chat GGUF model"""
    print("🔧 Setting up Llama2 7B Chat GGUF model for Red Teaming...")
    
    try:
        # Import required libraries
        from huggingface_hub import hf_hub_download
        
        print("📥 Downloading Llama2 7B Chat GGUF model...")
        print("This may take several minutes depending on your internet connection...")
        
        # Download the model file
        model_path = hf_hub_download(
            repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
            filename="llama-2-7b-chat.Q4_K_M.gguf",
            local_dir="./models"
        )
        
        print(f"✅ Model downloaded successfully to: {model_path}")
        
        # Create a symlink for easier access
        local_path = "./llama-2-7b-chat.gguf"
        if os.path.exists(local_path):
            os.remove(local_path)
        
        # Create symlink using absolute paths to avoid issues
        abs_model_path = os.path.abspath(model_path)
        abs_local_path = os.path.abspath(local_path)
        
        try:
            os.symlink(abs_model_path, abs_local_path)
            print(f"✅ Created symlink: {local_path} -> {abs_model_path}")
        except Exception as e:
            print(f"⚠️ Could not create symlink: {e}")
            print(f"Model is available at: {abs_model_path}")
        
        return True
        
    except ImportError:
        print("❌ huggingface_hub not found. Installing...")
        os.system("pip install huggingface_hub")
        return download_model()
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("\nAlternative setup:")
        print("1. Visit: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF")
        print("2. Download the llama-2-7b-chat.Q4_K_M.gguf file")
        print("3. Place it in the current directory as 'llama-2-7b-chat.gguf'")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "flask",
        "llama-cpp-python", 
        "torch",
        "huggingface_hub"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        os.system(f"pip install {' '.join(missing_packages)}")
        return True
    else:
        print("✅ All dependencies are installed!")
        return True

def main():
    """Main setup function"""
    print("🚀 Llama2 7B Chat GGUF Setup for Red Teaming")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Download model
    if download_model():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Test the model: python test_model.py")
        print("2. Run the application: python app.py")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
