#!/usr/bin/env python3
"""
Ultra-fast configuration for Llama2 7B Chat GGUF
Implements the most aggressive optimizations for maximum speed
"""

import os

def create_ultra_fast_config():
    """Create an ultra-fast configuration for app.py"""
    
    config_content = '''# Ultra-fast Llama2 configuration
# This configuration prioritizes speed over response length

def load_model():
    """Load Llama2 7B Chat GGUF model with ultra-fast settings"""
    global model
    
    print("Loading Llama2 7B Chat GGUF model (Ultra-Fast Mode)...")
    
    # Try multiple possible model paths
    possible_paths = [
        "./llama-2-7b-chat-fast.gguf",  # Faster Q2_K model
        "./llama-2-7b-chat.gguf",       # Original model
        "./models/llama-2-7b-chat.Q2_K.gguf",
        "./models/llama-2-7b-chat.Q4_K_M.gguf",
    ]
    
    for model_path in possible_paths:
        if os.path.exists(model_path):
            try:
                print(f"Found model at: {model_path}")
                model = Llama(
                    model_path=model_path,
                    n_ctx=512,      # Ultra-small context for maximum speed
                    n_threads=4,    # Optimized thread count
                    n_gpu_layers=0, # CPU only
                    n_batch=128,    # Small batch for speed
                    verbose=False
                )
                print("Ultra-fast Llama2 model loaded successfully!")
                return
            except Exception as e:
                print(f"Error loading model from {model_path}: {e}")
                continue
    
    raise Exception("Could not load Llama2 model. Please ensure the model is available.")

def generate_response(prompt, max_new_tokens=64, temperature=0.3):
    """Generate response with ultra-fast settings"""
    if model is None:
        return "Error: Model not loaded"
    
    try:
        # Simple prompt format for speed
        formatted_prompt = f"[INST] {prompt} [/INST]"
        
        # Ultra-fast generation parameters
        response = model(
            formatted_prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=0.7,           # Very low for speed
            top_k=5,             # Very low for speed
            repeat_penalty=1.01, # Minimal penalty
            stop=["[INST]", "</s>", "<s>"],
            stream=False
        )
        
        generated_text = response['choices'][0]['text'].strip()
        
        # Clean up response
        if generated_text.startswith(formatted_prompt):
            generated_text = generated_text[len(formatted_prompt):].strip()
        
        return generated_text if generated_text else "Response generated."
    
    except Exception as e:
        return f"Error: {str(e)}"'''
    
    # Write the ultra-fast configuration
    with open('ultra_fast_config.py', 'w') as f:
        f.write(config_content)
    
    print("✅ Ultra-fast configuration created: ultra_fast_config.py")
    print("\nTo use this configuration:")
    print("1. Replace the load_model() and generate_response() functions in app.py")
    print("2. Or import from ultra_fast_config.py")
    
    return True

def create_backup_and_apply():
    """Create backup and apply ultra-fast configuration"""
    print("🔧 Applying ultra-fast configuration...")
    
    try:
        # Create backup
        if os.path.exists('app.py'):
            os.system('cp app.py app_backup.py')
            print("✅ Created backup: app_backup.py")
        
        # Read current app.py
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Replace the functions with ultra-fast versions
        ultra_fast_functions = '''def load_model():
    """Load Llama2 7B Chat GGUF model with ultra-fast settings"""
    global model
    
    print("Loading Llama2 7B Chat GGUF model (Ultra-Fast Mode)...")
    
    # Try multiple possible model paths
    possible_paths = [
        "./llama-2-7b-chat-fast.gguf",  # Faster Q2_K model
        "./llama-2-7b-chat.gguf",       # Original model
        "./models/llama-2-7b-chat.Q2_K.gguf",
        "./models/llama-2-7b-chat.Q4_K_M.gguf",
    ]
    
    for model_path in possible_paths:
        if os.path.exists(model_path):
            try:
                print(f"Found model at: {model_path}")
                model = Llama(
                    model_path=model_path,
                    n_ctx=512,      # Ultra-small context for maximum speed
                    n_threads=4,    # Optimized thread count
                    n_gpu_layers=0, # CPU only
                    n_batch=128,    # Small batch for speed
                    verbose=False
                )
                print("Ultra-fast Llama2 model loaded successfully!")
                return
            except Exception as e:
                print(f"Error loading model from {model_path}: {e}")
                continue
    
    raise Exception("Could not load Llama2 model. Please ensure the model is available.")

def generate_response(prompt, max_new_tokens=64, temperature=0.3):
    """Generate response with ultra-fast settings"""
    if model is None:
        return "Error: Model not loaded"
    
    try:
        # Simple prompt format for speed
        formatted_prompt = f"[INST] {prompt} [/INST]"
        
        # Ultra-fast generation parameters
        response = model(
            formatted_prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=0.7,           # Very low for speed
            top_k=5,             # Very low for speed
            repeat_penalty=1.01, # Minimal penalty
            stop=["[INST]", "</s>", "<s>"],
            stream=False
        )
        
        generated_text = response['choices'][0]['text'].strip()
        
        # Clean up response
        if generated_text.startswith(formatted_prompt):
            generated_text = generated_text[len(formatted_prompt):].strip()
        
        return generated_text if generated_text else "Response generated."
    
    except Exception as e:
        return f"Error: {str(e)}"'''
        
        # Replace the functions in app.py
        import re
        
        # Find and replace load_model function
        load_model_pattern = r'def load_model\(\):.*?def generate_response'
        content = re.sub(load_model_pattern, ultra_fast_functions + '\n\ndef generate_response', content, flags=re.DOTALL)
        
        # Find and replace generate_response function
        generate_response_pattern = r'def generate_response\(.*?\):.*?(?=# HTML template)'
        content = re.sub(generate_response_pattern, '', content, flags=re.DOTALL)
        
        # Write updated app.py
        with open('app.py', 'w') as f:
            f.write(content)
        
        print("✅ Applied ultra-fast configuration to app.py")
        return True
        
    except Exception as e:
        print(f"❌ Error applying configuration: {e}")
        return False

def main():
    """Main function"""
    print("⚡ Ultra-Fast Llama2 Configuration")
    print("=" * 40)
    
    print("This will apply the most aggressive optimizations:")
    print("- Context window: 512 tokens (vs 1024)")
    print("- Max tokens: 64 (vs 128)")
    print("- Temperature: 0.3 (vs 0.5)")
    print("- Top-k: 5 (vs 10)")
    print("- Batch size: 128 (vs 256)")
    print("- Minimal repetition penalty")
    
    response = input("\nApply ultra-fast configuration? (y/n): ").lower()
    
    if response == 'y':
        if create_backup_and_apply():
            print("\n🎉 Ultra-fast configuration applied!")
            print("\nExpected performance:")
            print("- Response time: 5-15 seconds")
            print("- Shorter but faster responses")
            print("- Lower memory usage")
            
            print("\nTo restore original settings:")
            print("cp app_backup.py app.py")
        else:
            print("\n❌ Failed to apply configuration")
    else:
        print("Configuration not applied.")

if __name__ == "__main__":
    main()
