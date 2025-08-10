#!/usr/bin/env python3
"""
Check LLM Guard installation and configuration
"""

def check_llm_guard_installation():
    """Check if LLM Guard is properly installed"""
    print("🔍 Checking LLM Guard Installation")
    print("=" * 40)
    
    try:
        # Try to import LLM Guard
        print("1. Testing imports...")
        from llm_guard import scan_prompt, scan_output
        print("   ✅ llm_guard imported successfully")
        
        from llm_guard.input_scanners import (
            Anonymize, 
            PromptInjection, 
            TokenLimit, 
            Toxicity,
            Code,
            BanSubstrings,
            BanTopics
        )
        print("   ✅ Input scanners imported successfully")
        
        from llm_guard.output_scanners import (
            Deanonymize, 
            NoRefusal, 
            Relevance, 
            Sensitive,
            Code as OutputCode,
            BanSubstrings as OutputBanSubstrings
        )
        print("   ✅ Output scanners imported successfully")
        
        from llm_guard.vault import Vault
        print("   ✅ Vault imported successfully")
        
        # Test basic functionality
        print("\n2. Testing basic functionality...")
        
        # Initialize vault
        vault = Vault()
        print("   ✅ Vault initialized")
        
        # Test input scanner
        input_scanners = [
            Anonymize(vault),
            PromptInjection(),
            TokenLimit(limit=2048),
            Toxicity(),
        ]
        print("   ✅ Input scanners created")
        
        # Test output scanner
        output_scanners = [
            Deanonymize(vault),
            NoRefusal(),
            Relevance(threshold=0.5),
            Sensitive(),
        ]
        print("   ✅ Output scanners created")
        
        # Test scanning
        test_input = "Hello, how are you?"
        sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, test_input)
        print("   ✅ Input scanning works")
        
        test_output = "I'm doing well, thank you!"
        sanitized_response, results_valid, results_score = scan_output(output_scanners, test_input, test_output)
        print("   ✅ Output scanning works")
        
        print("\n✅ LLM Guard is working correctly!")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("\n💡 Solution: Install LLM Guard with:")
        print("   pip install llm-guard")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        print(f"   Full traceback: {traceback.format_exc()}")
        return False

def check_llm_guard_version():
    """Check LLM Guard version"""
    try:
        import llm_guard
        print(f"📦 LLM Guard version: {llm_guard.__version__}")
        return True
    except:
        print("❌ Could not determine LLM Guard version")
        return False

def main():
    """Main function"""
    print("🛡️ LLM Guard Diagnostic Tool")
    print("=" * 50)
    
    # Check version
    check_llm_guard_version()
    
    # Check installation
    success = check_llm_guard_installation()
    
    if success:
        print("\n🎉 LLM Guard is ready to use!")
        print("You can now run: python app.py")
    else:
        print("\n❌ LLM Guard has issues.")
        print("Please fix the issues above before running the application.")

if __name__ == "__main__":
    main()
