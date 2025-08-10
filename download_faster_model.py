#!/usr/bin/env python3
"""
Download a faster, smaller Llama2 model variant for better performance
"""

import os
import sys
from pathlib import Path

def download_faster_model():
    """Download a smaller, faster Llama2 model variant"""
    print("🚀 Downloading Faster Llama2 Model Variant")
    print("=" * 50)
    
    try:
        from huggingface_hub import hf_hub_download
        
        print("📥 Downloading Llama2 7B Chat Q2_K GGUF model...")
        print("This model is ~2.5GB (vs 4GB) and should be 2-3x faster!")
        print("Downloading... (this may take 10-15 minutes)")
        
        # Download the smaller Q2_K model
        model_path = hf_hub_download(
            repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
            filename="llama-2-7b-chat.Q2_K.gguf",  # Smaller, faster variant
            local_dir="./models"
        )
        
        print(f"✅ Faster model downloaded successfully to: {model_path}")
        
        # Create a symlink for easier access
        local_path = "./llama-2-7b-chat-fast.gguf"
        if os.path.exists(local_path):
            os.remove(local_path)
        
        # Create symlink using absolute paths
        abs_model_path = os.path.abspath(model_path)
        abs_local_path = os.path.abspath(local_path)
        
        try:
            os.symlink(abs_model_path, abs_local_path)
            print(f"✅ Created symlink: {local_path} -> {abs_model_path}")
        except Exception as e:
            print(f"⚠️ Could not create symlink: {e}")
            print(f"Model is available at: {abs_model_path}")
        
        print("\n🎉 Faster model ready!")
        print("\nTo use this faster model, update your app.py:")
        print("Change the model path to: './llama-2-7b-chat-fast.gguf'")
        
        return True
        
    except ImportError:
        print("❌ huggingface_hub not found. Installing...")
        os.system("pip install huggingface_hub")
        return download_faster_model()
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("\nAlternative: Download manually from:")
        print("https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF")
        print("File: llama-2-7b-chat.Q2_K.gguf")
        return False

def update_app_for_faster_model():
    """Update app.py to use the faster model"""
    print("\n🔧 Updating app.py for faster model...")
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Update the model path to use the faster model
        updated_content = content.replace(
            '"./llama-2-7b-chat.gguf"',
            '"./llama-2-7b-chat-fast.gguf"'
        )
        
        with open('app.py', 'w') as f:
            f.write(updated_content)
        
        print("✅ app.py updated to use faster model!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating app.py: {e}")
        return False

def main():
    """Main function"""
    print("🎯 Llama2 Performance Boost - Download Faster Model")
    print("=" * 60)
    
    # Download the faster model
    if download_faster_model():
        # Update app.py
        update_app_for_faster_model()
        
        print("\n🎉 Setup completed!")
        print("\nExpected performance improvements:")
        print("- Model size: ~2.5GB (vs 4GB)")
        print("- Loading time: 30-60s (vs 1-2 minutes)")
        print("- Response time: 10-30s (vs 60-120s)")
        print("- Memory usage: ~2GB (vs 4GB)")
        
        print("\nNext steps:")
        print("1. Test the faster model: python test_model.py")
        print("2. Run the application: python app.py")
        print("3. Enjoy much faster responses!")
        
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
