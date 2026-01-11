import os
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from supabase import create_client, Client
from groq import Groq

app = Flask(__name__)
CORS(app)

# Environment Variables (Set ini di Dashboard Vercel)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Tambahkan pengecekan agar tidak crash jika env tidak ada saat startup
supabase_instance = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_instance = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        pass

groq_client = None
if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception:
        pass

@app.route('/')
def home():
    return jsonify({
        "status": "XTermux Backend Running",
        "version": "1.4.1",
        "engine": "Groq Proxy",
        "config_ready": all([SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY])
    })

@app.route('/api/config')
def get_config():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return jsonify({"error": "Supabase not configured in Vercel environment"}), 500
    return jsonify({
        "supabase_url": SUPABASE_URL,
        "supabase_key": SUPABASE_KEY,
    })

@app.route('/auth/<provider>')
def auth(provider):
    if not SUPABASE_URL:
        return jsonify({"error": "Backend not configured"}), 500
    return jsonify({
        "message": f"Redirecting to {provider} auth...",
        "url": f"{SUPABASE_URL}/auth/v1/authorize?provider={provider}"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    if not groq_client:
        return jsonify({"error": "Groq AI not configured in Vercel secrets"}), 500
    
    data = request.get_json(silent=True) or {}
    user_message = data.get('message')
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
        
    model = data.get('model', 'llama-3.1-70b-versatile')
    
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
