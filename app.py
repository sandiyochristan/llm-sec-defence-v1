from flask import Flask, render_template_string, request, jsonify
from llama_cpp import Llama
import torch
import os

# LLM Guard imports for security scanning
from llm_guard import scan_prompt, scan_output
from llm_guard.input_scanners import (
    Anonymize, 
    PromptInjection, 
    TokenLimit, 
    Toxicity,
    Code,
    BanSubstrings,
    BanTopics
)
from llm_guard.output_scanners import (
    Deanonymize, 
    NoRefusal, 
    Relevance, 
    Sensitive,
    Code as OutputCode,
    BanSubstrings as OutputBanSubstrings
)
from llm_guard.vault import Vault

app = Flask(__name__)

# Global variables for model and LLM Guard
model = None
vault = None
input_scanners = None
output_scanners = None

def initialize_llm_guard():
    """Initialize LLM Guard security scanners"""
    global vault, input_scanners, output_scanners
    
    print("🔒 Initializing LLM Guard security scanners...")
    
    try:
        # Initialize the vault for anonymization
        vault = Vault()
        print("  ✅ Vault initialized")
        
        # Define input scanners for Red Teaming security
        print("  📥 Setting up input scanners...")
        input_scanners = [
            Anonymize(vault),  # Anonymize sensitive data
            PromptInjection(),  # Detect prompt injection attacks
            TokenLimit(limit=2048),  # Limit input length
            Toxicity(),  # Detect toxic content
            BanSubstrings(substrings=["password", "admin", "root", "sudo"], case_sensitive=False),  # Monitor sensitive terms
            BanTopics(topics=["violence", "illegal_activities"], threshold=0.8)  # Monitor dangerous topics
        ]
        print("  ✅ Input scanners configured")
        
        # Define output scanners for Red Teaming security
        print("  📤 Setting up output scanners...")
        output_scanners = [
            Deanonymize(vault),  # Deanonymize data in responses
            NoRefusal(),  # Detect refusal patterns
            Relevance(threshold=0.5),  # Ensure response relevance
            Sensitive(),  # Detect sensitive information leakage
            OutputCode(languages=["Python", "JavaScript", "PHP"], is_blocked=False),  # Monitor code output
            OutputBanSubstrings(substrings=["password", "admin", "root", "sudo"], case_sensitive=False)  # Monitor sensitive terms
        ]
        print("  ✅ Output scanners configured")
        
        print("✅ LLM Guard security scanners initialized!")
        
    except Exception as e:
        print(f"⚠️ Warning: LLM Guard initialization failed: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        print("Continuing without LLM Guard protection...")
        vault = None
        input_scanners = None
        output_scanners = None

def load_model():
    """Load Llama2 7B Chat GGUF model for Red Teaming with good token limits and CPU compatibility"""
    global model
    
    print("Loading Llama2 7B Chat GGUF model...")
    
    # Try multiple possible model paths (prioritizing faster Q2_K model)
    possible_paths = [
        "./llama-2-7b-chat-fast.gguf",  # Faster Q2_K model symlink
        "./models/llama-2-7b-chat.Q2_K.gguf",  # Direct path to Q2_K model
        "/home/user/models/llama-2-7b-chat.Q2_K.gguf",  # User's Q2_K model path
        "./llama-2-7b-chat.gguf",  # Original Q4_K_M model symlink
        "./models/llama-2-7b-chat.Q4_K_M.gguf",  # Direct path to Q4_K_M model
        "/home/user/models/llama-2-7b-chat.Q4_K_M.gguf",  # User's Q4_K_M model path
        os.path.expanduser("~/models/llama-2-7b-chat.Q2_K.gguf"),  # Expanded Q2_K path
        os.path.expanduser("~/models/llama-2-7b-chat.Q4_K_M.gguf"),  # Expanded Q4_K_M path
    ]
    
    for model_path in possible_paths:
        if os.path.exists(model_path):
            try:
                print(f"Found model at: {model_path}")
                model = Llama(
                    model_path=model_path,
                    n_ctx=2048,  # Optimal context window from performance test
                    n_threads=8,  # Optimal thread count from performance test
                    n_gpu_layers=0,  # Use CPU only for compatibility
                    n_batch=1024,  # Optimal batch size from performance test
                    verbose=False
                )
                print("Llama2 model loaded successfully!")
                return
            except Exception as e:
                print(f"Error loading model from {model_path}: {e}")
                continue
    
    # If no local model found, try to download from Hugging Face
    try:
        print("No local model found. Attempting to download from Hugging Face...")
        from huggingface_hub import hf_hub_download
        
        # Check if model is already downloaded in cache
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        cached_model_path = os.path.join(cache_dir, "models--TheBloke--Llama-2-7B-Chat-GGUF", "snapshots", "*", "llama-2-7b-chat.Q2_K.gguf")
        
        import glob
        cached_models = glob.glob(cached_model_path)
        
        if cached_models:
            model_path = cached_models[0]
            print(f"Found cached model: {model_path}")
        else:
            print("Downloading model from Hugging Face...")
            model_path = hf_hub_download(
                repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
                filename="llama-2-7b-chat.Q2_K.gguf",  # Faster Q2_K model
                local_dir="./models"
            )
        
        model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=8,
            n_gpu_layers=0,
            n_batch=1024,
            verbose=False
        )
        print("Llama2 model loaded successfully!")
        
    except Exception as e:
        raise Exception(f"Could not load Llama2 model. Please ensure the model is available at one of these paths: {possible_paths}")

def generate_response(prompt, max_new_tokens=256, temperature=0.7):
    """Generate response using the loaded Llama2 model with optimal performance settings"""
    if model is None:
        return "Error: Model not loaded"
    
    try:
        # Create a chat format prompt for Llama2
        formatted_prompt = f"[INST] {prompt} [/INST]"
        
        # Generate response with optimal performance settings
        response = model(
            formatted_prompt,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=0.9,  # Balanced for quality and speed
            top_k=20,  # Balanced for quality and speed
            repeat_penalty=1.05,  # Balanced penalty
            stop=["[INST]", "</s>", "<s>"],  # Stop at instruction markers
            stream=False  # Disable streaming for faster response
        )
        
        # Extract the generated text
        generated_text = response['choices'][0]['text'].strip()
        
        # Clean up the response
        if generated_text.startswith(formatted_prompt):
            generated_text = generated_text[len(formatted_prompt):].strip()
        
        # Only try alternative prompt if response is very short
        if not generated_text or len(generated_text) < 10:
            alt_prompt = f"<s>[INST] {prompt} [/INST]"
            response = model(
                alt_prompt,
                max_tokens=max_new_tokens,
                temperature=temperature,
                top_p=0.9,
                top_k=20,
                repeat_penalty=1.05,
                stop=["[INST]", "</s>", "<s>"],
                stream=False
            )
            generated_text = response['choices'][0]['text'].strip()
            
            if generated_text.startswith(alt_prompt):
                generated_text = generated_text[len(alt_prompt):].strip()
        
        return generated_text if generated_text else "I understand your question. Let me provide a response based on my training data."
    
    except Exception as e:
        return f"Error generating response: {str(e)}"

def generate_secure_response(user_input, max_new_tokens=256, temperature=0.7):
    """Generate response with LLM Guard security scanning"""
    global input_scanners, output_scanners
    
    # If LLM Guard is not available, fall back to regular response generation
    if input_scanners is None or output_scanners is None:
        print("⚠️ LLM Guard not available, using regular response generation")
        return generate_response(user_input, max_new_tokens, temperature)
    
    try:
        print(f"🔍 Scanning input: {user_input[:50]}...")
        
        # Scan and sanitize the user input
        sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, user_input)
        
        # Check if input is valid
        if any(not result for result in results_valid.values()):
            blocked_reasons = [scanner for scanner, valid in results_valid.items() if not valid]
            print(f"🚫 Input blocked by scanners: {blocked_reasons}")
            print(f"📊 Scanner scores: {results_score}")
            return f"⚠️ Input blocked for security reasons. Detected issues: {', '.join(blocked_reasons)}"
        
        print(f"✅ Input passed security scan. Scores: {results_score}")
        
        # Generate response using the sanitized prompt
        response_text = generate_response(sanitized_prompt, max_new_tokens, temperature)
        
        print(f"🔍 Scanning output: {response_text[:50]}...")
        
        # Scan and sanitize the model's response
        sanitized_response_text, results_valid, results_score = scan_output(
            output_scanners, sanitized_prompt, response_text
        )
        
        # Check if output is valid
        if any(not result for result in results_valid.values()):
            blocked_reasons = [scanner for scanner, valid in results_valid.items() if not valid]
            print(f"🚫 Output blocked by scanners: {blocked_reasons}")
            print(f"📊 Scanner scores: {results_score}")
            return f"⚠️ Response blocked for security reasons. Detected issues: {', '.join(blocked_reasons)}"
        
        print(f"✅ Output passed security scan. Scores: {results_score}")
        
        return sanitized_response_text
        
    except Exception as e:
        print(f"❌ Error in secure response generation: {e}")
        print("Falling back to regular response generation...")
        return generate_response(user_input, max_new_tokens, temperature)

# HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Red Teaming LLM Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .chat-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #fafafa;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #dc3545;
            color: white;
            margin-left: 20%;
        }
        .bot-message {
            background-color: #e9ecef;
            color: black;
            margin-right: 20%;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        #user-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            padding: 10px 20px;
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background-color: #c82333;
        }
        button:disabled {
            background-color: #6c757d;
            cursor: not-allowed;
        }
        .loading {
            color: #6c757d;
            font-style: italic;
        }
        .model-info {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 20px;
            color: #721c24;
        }
        .security-notice {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 20px;
            color: #856404;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>🔒 Red Teaming LLM Security Lab</h1>
        
        <div class="model-info">
            <strong>Model:</strong> Llama2 7B Chat GGUF<br>
            <strong>Response Length:</strong> 256 tokens (configurable)<br>
            <strong>Purpose:</strong> LLM Security Research & Red Teaming<br>
            <strong>CPU Optimized:</strong> Yes<br>
            <strong>Security:</strong> LLM Guard Protected
        </div>
        
        <div class="security-notice">
            <strong>⚠️ Security Notice:</strong> This is a Red Teaming lab environment with LLM Guard protection. 
            All interactions are for security research purposes only. 
            Input and output are scanned for security threats.
            Do not use for malicious purposes.
        </div>
        
        <div class="chat-messages" id="chat-messages">
            <div class="message bot-message">
                Hello! I'm a Llama2 7B Chat GGUF model with LLM Guard protection for Red Teaming and LLM security research. 
                I can generate responses up to 256 tokens and support various security testing scenarios. 
                All inputs and outputs are scanned for security threats. 
                How can I help you with your security research today?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your security test prompt here..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()" id="send-btn">Send</button>
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function addMessage(message, isUser) {
            const messagesDiv = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = message;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            
            // Disable input and button
            input.disabled = true;
            sendBtn.disabled = true;
            sendBtn.textContent = 'Generating...';
            
            // Add loading message
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message loading';
            loadingDiv.textContent = 'Generating response...';
            document.getElementById('chat-messages').appendChild(loadingDiv);
            
            // Send request to backend
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                // Remove loading message
                document.getElementById('chat-messages').removeChild(loadingDiv);
                
                // Add bot response
                addMessage(data.response, false);
                
                // Re-enable input and button
                input.disabled = false;
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
                input.focus();
            })
            .catch(error => {
                // Remove loading message
                document.getElementById('chat-messages').removeChild(loadingDiv);
                
                // Add error message
                addMessage('Error: ' + error.message, false);
                
                // Re-enable input and button
                input.disabled = false;
                sendBtn.disabled = false;
                sendBtn.textContent = 'Send';
                input.focus();
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'Please provide a message.'})
        
        # Generate secure response with LLM Guard scanning
        response = generate_secure_response(user_message)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'tokenizer_loaded': False, # No tokenizer for Llama2 GGUF
        'generator_loaded': model is not None # Llama2 is a generator
    })

if __name__ == '__main__':
    print("Starting Red Teaming LLM Chat Application with LLM Guard...")
    
    # Initialize LLM Guard security scanners
    initialize_llm_guard()
    
    print("Loading model (this may take a few minutes)...")
    
    # Load the model
    load_model()
    
    print("Starting Flask server...")
    print("🔒 Security Status:", "Enabled" if input_scanners is not None else "Disabled")
    app.run(debug=True, host='0.0.0.0', port=5000)
