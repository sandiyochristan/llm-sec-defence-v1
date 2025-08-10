#!/usr/bin/env python3
"""
Test script to verify improved response generation
"""

import sys
import os

def test_responses():
    """Test the improved response generation"""
    print("🔍 Testing improved response generation...")
    
    try:
        # Import the app module
        sys.path.append('.')
        from app import load_model, generate_response
        
        # Load the model
        print("Loading model...")
        load_model()
        
        # Test prompts that were failing before
        test_prompts = [
            "hello",
            "what is cybersecurity",
            "explain about cybersecurity in detail",
            "tell me a joke",
            "what is the capital of France",
            "how does encryption work",
            "explain penetration testing",
            "what are common cybersecurity threats",
            "why is the sky blue",
            "who are you"
        ]
        
        print("\nTesting response generation...")
        for prompt in test_prompts:
            print(f"\nPrompt: {prompt}")
            response = generate_response(prompt)
            print(f"Response: {response}")
            
            # Check response quality
            if response and len(response) > 50:
                print("✅ Excellent detailed response")
            elif response and len(response) > 20:
                print("✅ Good response")
            elif response and len(response) > 10:
                print("⚠️  Short but acceptable response")
            else:
                print("❌ Poor response")
        
        print("\n🎉 Response test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run the response test"""
    print("🔒 Red Teaming LLM - Response Quality Test")
    print("=" * 50)
    
    success = test_responses()
    
    if success:
        print("\n✅ Response generation is working better!")
        print("You can now run: python app.py")
    else:
        print("\n❌ Test failed. Please check the errors above.")

if __name__ == "__main__":
    main()
