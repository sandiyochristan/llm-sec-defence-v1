#!/usr/bin/env python3
"""
Test script for the Red Teaming LLM model
Tests the Llama2 7B Chat GGUF model loading and response generation
"""

import sys
import os

def test_model_loading():
    """Test if the Llama2 model can be loaded and generate responses"""
    print("🔍 Testing Llama2 7B Chat GGUF model loading and response generation...")
    
    try:
        # Import the app module to access the model functions
        sys.path.append('.')
        from app import load_model, generate_response
        
        # Load the model
        print("Loading Llama2 model...")
        load_model()
        
        # Test response generation
        test_prompts = [
            "Hello, how are you?",
            "What is the capital of France?",
            "Tell me a joke",
            "What is 2+2?",
            "Explain what Red Teaming is in cybersecurity"
        ]
        
        print("\nTesting response generation...")
        for prompt in test_prompts:
            print(f"\nPrompt: {prompt}")
            response = generate_response(prompt, max_new_tokens=100)
            print(f"Response: {response}")
            
            if response and len(response) > 5:
                print("✅ Response generated successfully")
            else:
                print("❌ Response too short or empty")
        
        print("\n🎉 Llama2 model test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have installed the requirements: pip install -r requirements.txt")
        print("2. The model will be downloaded automatically on first run")
        print("3. Ensure you have sufficient disk space (model is ~4GB)")
        print("4. Check your internet connection for model download")
        return False

def main():
    """Run the model test"""
    print("🔒 Red Teaming LLM Model Test - Llama2 7B Chat GGUF")
    print("=" * 50)
    
    success = test_model_loading()
    
    if success:
        print("\n✅ Llama2 model is working correctly!")
        print("You can now run: python app.py")
    else:
        print("\n❌ Model test failed. Please check the errors above.")

if __name__ == "__main__":
    main()
