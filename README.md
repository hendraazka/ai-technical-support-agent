# AI Technical Support Agent

An AI-powered technical support agent built with Python, Google Gemini, LangGraph, and Telegram. Designed to assist with Linux infrastructure troubleshooting, system monitoring, and Docker operations.

## Overview

This project explores how Agentic AI can be integrated with DevOps and infrastructure operations.

The agent interacts through Telegram, uses Google Gemini as its LLM, and leverages LangGraph to coordinate reasoning and tool execution.

The project is developed in a local Ubuntu 24.04 environment running on Windows 11 with WSL2.

## Architecture

```text
Telegram User
      |
      v
Telegram Bot
      |
      v
User Access Control
      |
      v
LangGraph ReAct Agent
      |
      v
Google Gemini API
      |
      +-------------------+
      |                   |
      v                   v
System Monitoring    Docker Monitoring
      |                   |
      v                   v
    psutil             Docker CLI

      |
      v
SQLite Conversation Memory
```

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Operating Environment | Ubuntu 24.04 / WSL2 |
| LLM | Google Gemini API |
| Agent Framework | LangGraph |
| Agent Pattern | ReAct |
| LLM Integration | LangChain Google GenAI |
| Chat Interface | Telegram Bot API |
| Telegram Library | python-telegram-bot |
| System Monitoring | psutil |
| Container Monitoring | Docker CLI |
| Persistent Memory | SQLite |
| Configuration | python-dotenv |
| Version Control | Git and GitHub |

## Current Features

- Telegram-based AI technical support interface
- Gemini-powered conversational agent
- LangGraph ReAct agent architecture
- Linux CPU, RAM, disk, and uptime monitoring
- Docker container monitoring
- Telegram user ID allowlist
- Persistent conversation history with SQLite
- Conversation history management through `/clear`

## Telegram Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/help` | Display available commands |
| `/id` | Display Telegram user ID |
| `/status` | Check Linux system status |
| `/docker` | Check Docker containers |
| `/clear` | Clear conversation history |

## Project Structure

```text
ai-technical-support-agent/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── bot.py
│   ├── agent.py
│   ├── tools.py
│   └── memory.py
├── data/
│   └── .gitkeep
├── docs/
├── scripts/
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

## Prerequisites

- Windows 11 with WSL2
- Ubuntu 24.04
- Python 3.12
- Docker Desktop with WSL2 integration
- Google Gemini API key
- Telegram Bot Token

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/hendraazka/ai-technical-support-agent.git
cd ai-technical-support-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
nano .env
```

Configure the following values:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_ALLOWED_USER_IDS=your_telegram_user_id
```

Never commit `.env` or expose API keys and bot tokens.

### 5. Run the application

```bash
python -m app.main
```

## Development Roadmap

- [x] Python and WSL2 environment
- [x] Gemini API integration
- [x] Telegram bot integration
- [x] LangGraph ReAct agent
- [x] Linux system monitoring tools
- [x] Docker monitoring tools
- [x] Telegram user access control
- [x] SQLite conversation memory
- [ ] RAG knowledge base
- [ ] Document ingestion and embeddings
- [ ] Vector database integration
- [ ] Human approval for sensitive operations
- [ ] Structured logging and observability
- [ ] Prometheus and Grafana integration
- [ ] Docker-based deployment
- [ ] Kubernetes deployment

## Security

- API keys and bot tokens are stored in environment variables.
- Telegram access is restricted through a user ID allowlist.
- Initial monitoring tools are read-only.
- Sensitive infrastructure operations will require an approval mechanism before implementation.

## Learning Objectives

This project is part of a hands-on learning journey toward AI Engineering, Agentic AI, and AI-powered infrastructure automation.

The focus is on understanding how LLMs, agents, tools, memory, RAG, and DevOps infrastructure work together in a production-oriented system.

## License

MIT License.

