import os
import json
import pickle

# Create dist directory
os.makedirs('dist', exist_ok=True)

# Load config
with open('qa_config.json', 'r') as f:
    config = json.load(f)

# Load PDF chunks
with open('my_pdf_model/chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

# Create static HTML with embedded JavaScript
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digital Intelligence Workshop Chatbot</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; color: white; margin-bottom: 30px; }}
        .chat-container {{ background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden; }}
        .chat-header {{ background: #4a5568; color: white; padding: 20px; text-align: center; }}
        .chat-messages {{ height: 400px; overflow-y: auto; padding: 20px; background: #f7fafc; }}
        .message {{ margin-bottom: 15px; }}
        .user-message {{ text-align: right; }}
        .bot-message {{ text-align: left; }}
        .message-bubble {{ display: inline-block; padding: 10px 15px; border-radius: 20px; max-width: 70%; }}
        .user-bubble {{ background: #4299e1; color: white; }}
        .bot-bubble {{ background: #e2e8f0; color: #2d3748; }}
        .input-container {{ padding: 20px; background: white; display: flex; gap: 10px; }}
        .input-field {{ flex: 1; padding: 12px; border: 2px solid #e2e8f0; border-radius: 25px; outline: none; }}
        .send-btn {{ padding: 12px 25px; background: #4299e1; color: white; border: none; border-radius: 25px; cursor: pointer; }}
        .send-btn:hover {{ background: #3182ce; }}
        .suggestions {{ padding: 15px; background: #edf2f7; }}
        .suggestion-btn {{ margin: 5px; padding: 8px 15px; background: #bee3f8; border: none; border-radius: 15px; cursor: pointer; font-size: 12px; }}
        .suggestion-btn:hover {{ background: #90cdf4; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Digital Intelligence Workshop</h1>
            <p>Ask me about the workshop, instructor, topics, or art exhibition!</p>
        </div>
        
        <div class="chat-container">
            <div class="chat-header">
                <h3>Workshop Assistant</h3>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">
                    <div class="message-bubble bot-bubble">
                        👋 Hello! I can answer questions about the Digital Intelligence Workshop. Try the suggestions below!
                    </div>
                </div>
            </div>
            
            <div class="suggestions">
                <button class="suggestion-btn" onclick="askQuestion('Who conducted the workshop?')">Who conducted workshop?</button>
                <button class="suggestion-btn" onclick="askQuestion('What topics were covered?')">Topics covered</button>
                <button class="suggestion-btn" onclick="askQuestion('Where was it held?')">Location</button>
                <button class="suggestion-btn" onclick="askQuestion('Tell me about Arduino')">About Arduino</button>
                <button class="suggestion-btn" onclick="askQuestion('What is IoT?')">IoT</button>
                <button class="suggestion-btn" onclick="askQuestion('Who conducted art exhibition?')">Art exhibition</button>
            </div>
            
            <div class="input-container">
                <input type="text" id="questionInput" class="input-field" placeholder="Ask your question..." onkeypress="handleKeyPress(event)">
                <button class="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        const qaData = {json.dumps(config["custom_qa"])};
        const pdfChunks = {json.dumps(chunks)};
        
        function findAnswer(question) {{
            const q = question.toLowerCase().trim();
            
            if (qaData[q]) return qaData[q];
            
            if (q.includes("art") && q.includes("where")) {{
                return qaData["where art exhibition"] || "Art exhibition arranged nearby the workshop venue";
            }}
            
            if (q.includes("art") && (q.includes("who") || q.includes("conducted") || q.includes("artist"))) {{
                return qaData["who conducted art exhibition"] || "Abhijith R from Sivadrumam, Peruvaram";
            }}
            
            for (const [key, answer] of Object.entries(qaData)) {{
                if (q.includes(key)) return answer;
            }}
            
            for (const [key, answer] of Object.entries(qaData)) {{
                const words = key.split(" ");
                if (words.length > 1 && words.every(word => q.includes(word))) {{
                    return answer;
                }}
            }}
            
            // Search in PDF chunks
            const words = q.split(' ');
            for (const chunk of pdfChunks) {{
                const chunkLower = chunk.toLowerCase();
                const matches = words.filter(word => word.length > 3 && chunkLower.includes(word));
                if (matches.length >= 2) {{
                    return chunk.substring(0, 200) + "...";
                }}
            }}
            
            return "Please ask about workshop topics, instructor, location, or art exhibition details.";
        }}

        function addMessage(message, isUser) {{
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{isUser ? 'user-message' : 'bot-message'}}`;
            messageDiv.innerHTML = `<div class="message-bubble ${{isUser ? 'user-bubble' : 'bot-bubble'}}">${{message}}</div>`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }}

        function sendMessage() {{
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            if (!question) return;

            addMessage(question, true);
            input.value = '';
            
            const answer = findAnswer(question);
            setTimeout(() => addMessage(answer, false), 500);
        }}

        function askQuestion(question) {{
            document.getElementById('questionInput').value = question;
            sendMessage();
        }}

        function handleKeyPress(event) {{
            if (event.key === 'Enter') sendMessage();
        }}
    </script>
</body>
</html>'''

# Write to dist/index.html
with open('dist/index.html', 'w') as f:
    f.write(html_content)

print("Static site built with model data successfully!")
