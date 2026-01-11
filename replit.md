# XTermux AI API Proxy

## Overview
XTermux AI API Proxy is a serverless backend deployed on Vercel that serves as a bridge to the Groq AI Engine. It provides a simple, unauthenticated API endpoint for AI chat completions using the Llama-3.1-70b model.

## System Architecture

### Backend (Vercel)
- **Framework**: Flask (Python 3.11+)
- **Platform**: Vercel Serverless Functions
- **AI Engine**: Groq (Llama-3.1-70b-versatile)
- **Security**: GROQ_API_KEY managed via Vercel Environment Variables

### API Endpoints
- `GET /`: Status page (HTML)
- `GET /api/status`: System health check (JSON)
- `POST /api/chat`: AI Chat completion endpoint
  - Request: `{"message": "user input"}`
  - Response: `{"reply": "AI response"}`

## Environment Variables
- `GROQ_API_KEY`: Required on Vercel for AI functionality.
