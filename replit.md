# XTermux Script

## Overview

XTermux is a multi-purpose command-line interface (CLI) tool built in Python. It provides an interactive terminal experience with rich text formatting and integrates with AI services for enhanced functionality. The application is designed to run in terminal environments and features user authentication through an external Vercel-hosted service.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Application Structure

- **Single-file Python application** (`main.py`) - The entire application logic is contained in one file, following a simple monolithic pattern suitable for CLI tools
- **Class-based design** - Uses the `XTermux` class to encapsulate application state and methods
- **Interactive menu system** - Implements a loop-based menu for user navigation

### AI Integration

- **Replit AI Integration** - Primary AI access through Replit's AI API (`https://api.replit.com/ai/v1`)
- **OpenAI fallback** - Supports direct OpenAI API as an alternative when Replit AI is not available
- **Environment-based configuration** - API keys are loaded from environment variables (`REPLIT_AI_API_KEY` or `OPENAI_API_KEY`)

### User Interface

- **Rich library** - Uses the `rich` package for enhanced terminal output including panels, tables, and live updates
- **Interactive prompts** - Leverages `rich.prompt` for user input handling

### Authentication

- **External auth service** - User authentication is handled through a separate Vercel-hosted application
- **Session state management** - Tracks connection status via `is_connected` flag and stores user data in `user_data`

## External Dependencies

### Python Packages

- `openai` - AI model interaction client
- `rich` - Terminal formatting and interactive elements
- `requests` - HTTP client for external API calls
- `python-dotenv` - Environment variable management

### External Services

- **Replit AI API** (`https://api.replit.com/ai/v1`) - Primary AI service integration
- **Vercel Auth App** - External authentication service (URL configured via `VERCEL_AUTH_URL` environment variable)

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `REPLIT_AI_API_KEY` | Replit AI integration API key (preferred) |
| `OPENAI_API_KEY` | Fallback OpenAI API key |
| `VERCEL_AUTH_URL` | URL for external authentication service |