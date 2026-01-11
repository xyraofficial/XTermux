import os
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from supabase import create_client, Client
from groq import Groq

app = Flask(__name__)
CORS(app)

# Environment Variables (Set these in Vercel Dashboard)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

supabase_instance: any = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

@app.route('/')
def home():
    return jsonify({"status": "XTermux Backend Running", "version": "1.0.0", "engine": "Groq Proxy"})

@app.route('/api/config')
def get_config():
    return jsonify({
        "supabase_url": SUPABASE_URL,
        "supabase_key": SUPABASE_KEY,
    })

@app.route('/auth/<provider>')
def auth(provider):
    return jsonify({
        "message": f"Redirecting to {provider} auth...",
        "url": f"{SUPABASE_URL}/auth/v1/authorize?provider={provider}"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    # Menggunakan API Key dari Secret Vercel
    if not groq_client:
        return jsonify({"error": "Groq AI not configured in Vercel secrets"}), 500
    
    data = request.json
    user_message = data.get('message')
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
