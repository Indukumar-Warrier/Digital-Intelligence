from flask import Flask, render_template, request, jsonify
import os
import pickle
import json

app = Flask(__name__)

def load_config():
    with open("qa_config.json", "r") as f:
        return json.load(f)

def load_pdf_model(model_dir):
    with open(os.path.join(model_dir, "chunks.pkl"), "rb") as f:
        chunks = pickle.load(f)
    return chunks

def find_best_match(question, config):
    q = question.lower().strip()
    
    if q in config["custom_qa"]:
        return config["custom_qa"][q]
    
    if "art" in q and "where" in q:
        return config["custom_qa"].get("where art exhibition", "Art exhibition arranged nearby the workshop venue")
    
    if "art" in q and any(word in q for word in ["who", "conducted", "artist"]):
        return config["custom_qa"].get("who conducted art exhibition", "Abhijith R from Sivadrumam, Peruvaram")
    
    for qa_key, answer in config["custom_qa"].items():
        if qa_key in q:
            return answer
    
    for qa_key, answer in config["custom_qa"].items():
        qa_words = qa_key.split()
        if len(qa_words) > 1 and all(word in q for word in qa_words):
            return answer
    
    return "Please ask about workshop topics, instructor, location, or art exhibition details."

# Load data once at startup
config = load_config()
chunks = load_pdf_model("my_pdf_model")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.json.get('question', '')
    answer = find_best_match(question, config)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)