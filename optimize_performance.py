#!/usr/bin/env python3
"""
Performance optimization script for Llama2 7B Chat GGUF
Helps find optimal settings for your hardware to reduce response time
"""

import os
import time
import psutil
from llama_cpp import Llama

def get_system_info():
    """Get system information for optimization"""
    print("🖥️ System Information:")
    print(f"CPU Cores: {psutil.cpu_count()}")
    print(f"CPU Logical Cores: {psutil.cpu_count(logical=True)}")
    print(f"Available RAM: {psutil.virtual_memory().available / (1024**3):.1f} GB")
    print(f"Total RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    print()

def find_model_path():
    """Find the Llama2 model file"""
    possible_paths = [
        "./llama-2-7b-chat.gguf",
        "./models/llama-2-7b-chat.Q4_K_M.gguf",
        "/home/user/models/llama-2-7b-chat.Q4_K_M.gguf",
        os.path.expanduser("~/models/llama-2-7b-chat.Q4_K_M.gguf"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def test_model_performance(model_path, config):
    """Test model performance with given configuration"""
    try:
        print(f"Testing with config: {config}")
        
        # Load model with test configuration
        model = Llama(
            model_path=model_path,
            n_ctx=config['n_ctx'],
            n_threads=config['n_threads'],
            n_batch=config['n_batch'],
            n_gpu_layers=0,
            verbose=False
        )
        
        # Test prompt
        test_prompt = "[INST] What is the capital of France? [/INST]"
        
        # Measure generation time
        start_time = time.time()
        response = model(
            test_prompt,
            max_tokens=100,
            temperature=0.7,
            top_p=0.9,
            top_k=20,
            repeat_penalty=1.05,
            stop=["[INST]", "</s>", "<s>"],
            stream=False
        )
        end_time = time.time()
        
        generation_time = end_time - start_time
        tokens_generated = len(response['choices'][0]['text'].split())
        tokens_per_second = tokens_generated / generation_time if generation_time > 0 else 0
        
        print(f"  ✅ Generation time: {generation_time:.2f}s")
        print(f"  ✅ Tokens generated: {tokens_generated}")
        print(f"  ✅ Tokens/second: {tokens_per_second:.1f}")
        print()
        
        return {
            'config': config,
            'generation_time': generation_time,
            'tokens_generated': tokens_generated,
            'tokens_per_second': tokens_per_second
        }
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        print()
        return None

def optimize_performance():
    """Find optimal performance configuration"""
    print("🚀 Llama2 Performance Optimizer")
    print("=" * 40)
    
    # Get system info
    get_system_info()
    
    # Find model
    model_path = find_model_path()
    if not model_path:
        print("❌ Model not found! Please ensure the model is downloaded.")
        return
    
    print(f"✅ Found model: {model_path}")
    print()
    
    # Test configurations
    cpu_cores = psutil.cpu_count()
    test_configs = [
        # Conservative settings
        {'n_ctx': 1024, 'n_threads': 2, 'n_batch': 256},
        {'n_ctx': 1024, 'n_threads': 4, 'n_batch': 256},
        {'n_ctx': 1024, 'n_threads': cpu_cores, 'n_batch': 256},
        
        # Balanced settings
        {'n_ctx': 2048, 'n_threads': 4, 'n_batch': 512},
        {'n_ctx': 2048, 'n_threads': cpu_cores, 'n_batch': 512},
        {'n_ctx': 2048, 'n_threads': cpu_cores, 'n_batch': 1024},
        
        # Aggressive settings (if enough RAM)
        {'n_ctx': 4096, 'n_threads': cpu_cores, 'n_batch': 1024},
        {'n_ctx': 4096, 'n_threads': cpu_cores, 'n_batch': 2048},
    ]
    
    print("🧪 Testing different configurations...")
    print()
    
    results = []
    for config in test_configs:
        result = test_model_performance(model_path, config)
        if result:
            results.append(result)
    
    if not results:
        print("❌ No successful tests. Check your model and system.")
        return
    
    # Find best configuration
    best_result = min(results, key=lambda x: x['generation_time'])
    
    print("🏆 Best Configuration Found:")
    print(f"Context Window: {best_result['config']['n_ctx']}")
    print(f"Threads: {best_result['config']['n_threads']}")
    print(f"Batch Size: {best_result['config']['n_batch']}")
    print(f"Generation Time: {best_result['generation_time']:.2f}s")
    print(f"Tokens/Second: {best_result['tokens_per_second']:.1f}")
    print()
    
    # Generate optimized app.py configuration
    print("📝 Recommended app.py configuration:")
    print("```python")
    print(f"model = Llama(")
    print(f"    model_path=model_path,")
    print(f"    n_ctx={best_result['config']['n_ctx']},")
    print(f"    n_threads={best_result['config']['n_threads']},")
    print(f"    n_batch={best_result['config']['n_batch']},")
    print(f"    n_gpu_layers=0,")
    print(f"    verbose=False")
    print(f")")
    print("```")
    print()
    
    # Additional optimization tips
    print("💡 Additional Optimization Tips:")
    print("1. Use a smaller model variant (Q2_K instead of Q4_K_M)")
    print("2. Reduce max_tokens in generate_response()")
    print("3. Lower temperature for faster, more focused responses")
    print("4. Consider using GPU if available")
    print("5. Close other applications to free up RAM")

def main():
    """Main function"""
    try:
        optimize_performance()
    except KeyboardInterrupt:
        print("\n⏹️ Optimization interrupted by user")
    except Exception as e:
        print(f"❌ Error during optimization: {e}")

if __name__ == "__main__":
    main()
