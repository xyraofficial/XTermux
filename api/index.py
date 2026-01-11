import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def get_groq():
    if GROQ_API_KEY:
        try:
            return Groq(api_key=GROQ_API_KEY)
        except:
            return None
    return None

@app.route('/')
def home():
    return jsonify({
        "status": "XTermux AI Proxy Running",
        "engine": "Groq",
        "ready": bool(GROQ_API_KEY)
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    client = get_groq()
    if not client:
        return jsonify({"error": "GROQ_API_KEY not configured in Vercel"}), 500
    
    data = request.get_json(silent=True) or {}
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
        
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel handler
app_handler = app
