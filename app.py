from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# HTML template
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>GLM-5 AI Chat</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: 'Segoe UI', Arial; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .chat-box { 
            background: white; 
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        textarea { 
            width: 100%; 
            height: 120px; 
            margin: 10px 0; 
            padding: 15px; 
            border: 2px solid #e0e0e0; 
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        button { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 12px 30px; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover {
            transform: scale(1.05);
        }
        #response { 
            background: #f8f9fa; 
            padding: 20px; 
            margin-top: 20px; 
            border-radius: 10px;
            border-left: 4px solid #667eea;
            font-size: 16px;
            line-height: 1.5;
        }
        .loading {
            color: #667eea;
            font-style: italic;
        }
        .error {
            color: red;
            background: #ffe6e6;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="chat-box">
        <h1>🤖 GLM-5 AI Assistant</h1>
        <textarea id="question" placeholder="Ask me anything... For example: How many r's are in strawberry?"></textarea>
        <button onclick="askAI()">Send Message ✨</button>
        <div id="response">💬 Your answer will appear here...</div>
    </div>

    <script>
        async function askAI() {
            const question = document.getElementById('question').value;
            const responseDiv = document.getElementById('response');
            
            if (!question.trim()) {
                responseDiv.innerHTML = '<div class="error">⚠️ Please enter a question!</div>';
                return;
            }
            
            responseDiv.innerHTML = '<div class="loading">🤔 Thinking... ⏳</div>';
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: question})
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    responseDiv.innerHTML = "<strong>✅ Answer:</strong><br><br>" + data.answer;
                } else {
                    responseDiv.innerHTML = '<div class="error">❌ Error: ' + data.error + '</div>';
                }
            } catch(error) {
                responseDiv.innerHTML = '<div class="error">❌ Connection error: ' + error.message + '</div>';
            }
        }
        
        // Allow Enter key to send (Ctrl+Enter for new line)
        document.getElementById('question').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.ctrlKey) {
                e.preventDefault();
                askAI();
            }
        });
    </script>
</body>
</html>
'''

# Use environment variable for API key (safer for deployment)
API_URL = "https://api.us-west-2.modal.direct/v1/chat/completions"
API_KEY = os.environ.get('API_KEY', 'modalresearch_B8RDpTpmO09hRYxNyebSLPnI_SmcopeouU12emcZGhI')

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json['question']
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        data = {
            "model": "zai-org/GLM-5.1-FP8",
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 500
        }
        
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*50)
    print("🌐 GLM-5 AI Chatbot Starting...")
    print(f"📱 Open in browser: http://localhost:{port}")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=port, debug=False)