from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from supabase import create_client
from groq import Groq

app = Flask(__name__)
CORS(app)

# Env
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_supabase():
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except:
            return None
    return None

def get_groq():
    if GROQ_API_KEY:
        try:
            return Groq(api_key=GROQ_API_KEY)
        except:
            return None
    return None

@app.route('/')
def index():
    return jsonify({
        "status": "online", 
        "service": "XTermux Backend",
        "env_check": {
            "supabase": bool(SUPABASE_URL),
            "groq": bool(GROQ_API_KEY)
        }
    })

@app.route('/api/config')
def config():
    return jsonify({
        "supabase_url": SUPABASE_URL,
        "supabase_key": SUPABASE_KEY
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    client = get_groq()
    if not client:
        return jsonify({"error": "AI not configured"}), 500
    data = request.get_json(silent=True) or {}
    msg = data.get('message')
    if not msg:
        return jsonify({"error": "No message"}), 400
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": msg}]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
