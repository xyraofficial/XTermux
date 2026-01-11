import os
import sys

# Tambahkan folder root ke path untuk menghindari import error di Vercel
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from groq import Groq

app = Flask(__name__)
CORS(app)

# Fallback untuk Environment Variables
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Inisialisasi clients secara lazy untuk mencegah crash saat startup
def get_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        return None

def get_groq():
    if not GROQ_API_KEY:
        return None
    try:
        return Groq(api_key=GROQ_API_KEY)
    except Exception:
        return None

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "service": "XTermux Backend",
        "config": {
            "supabase": bool(SUPABASE_URL),
            "groq": bool(GROQ_API_KEY)
        }
    })

@app.route('/api/config')
def config():
    if not SUPABASE_URL:
        return jsonify({"error": "Missing config"}), 500
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

# Handler untuk Vercel
def handler(request):
    return app(request)

if __name__ == "__main__":
    app.run(port=5000)
