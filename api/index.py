import os
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from supabase import create_client, Client
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Environment Variables (Set these in Vercel Dashboard)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
ai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

@app.route('/')
def home():
    return jsonify({"status": "XTermux Backend Running", "version": "1.0.0"})

@app.route('/auth/<provider>')
def auth(provider):
    # Logic to handle Supabase Auth Redirect
    # In a real app, you'd use supabase.auth.sign_in_with_oauth
    # For now, we redirect to a mock success or your Supabase Auth UI
    return jsonify({
        "message": f"Redirecting to {provider} auth...",
        "url": f"{SUPABASE_URL}/auth/v1/authorize?provider={provider}"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    if not ai_client:
        return jsonify({"error": "AI not configured"}), 500
    
    data = request.json
    user_message = data.get('message')
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
