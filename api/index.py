from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# HTML template string for single-file deployment to avoid path issues
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XTermux AI Proxy - Status</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --text-color: #f1f5f9;
            --primary-color: #38bdf8;
            --success-color: #4ade80;
            --card-bg: #1e293b;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: var(--card-bg);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 400px;
            width: 90%;
            border: 1px solid #334155;
        }
        h1 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        .status {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            font-weight: bold;
            margin: 1rem 0;
            background-color: rgba(74, 222, 128, 0.1);
            color: var(--success-color);
        }
        p {
            color: #94a3b8;
            line-height: 1.6;
        }
        .badge {
            display: inline-block;
            background: #334155;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            margin: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>XTermux AI</h1>
        <div class="status">● System Online</div>
        <p>Vercel Serverless Backend is running correctly and ready to handle your AI requests.</p>
        <div style="margin-top: 1.5rem;">
            <span class="badge">Groq Engine</span>
            <span class="badge">Llama-3.1</span>
            <span class="badge">Flask API</span>
        </div>
    </div>
</body>
</html>
"""

def get_groq_client():
    from groq import Groq
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        return Groq(api_key=api_key)
    return None

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/api/status')
def status():
    return jsonify({
        "status": "XTermux AI Proxy Running",
        "ready": bool(os.environ.get("GROQ_API_KEY"))
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        client = get_groq_client()
        if not client:
            return jsonify({"error": "GROQ_API_KEY not configured"}), 500
        
        data = request.get_json(silent=True) or {}
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
            
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": user_message}]
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Entry point for Vercel
app_handler = app
