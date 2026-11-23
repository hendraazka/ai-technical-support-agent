# AI Technical Support Agent

An AI-powered technical support agent built with Python, Google Gemini, LangGraph, RAG, and Telegram. Designed to assist with Linux infrastructure troubleshooting, system monitoring, Docker monitoring, and incident analysis using internal runbooks.

## Overview

This project explores how Agentic AI can support DevOps and technical support operations.

The agent interacts through Telegram, uses Google Gemini as its LLM, and leverages LangGraph to coordinate reasoning and tool execution.

It combines infrastructure monitoring, Retrieval-Augmented Generation (RAG), conversation memory, and sensitive data masking to help technical support teams investigate incidents more efficiently.

The project is developed in Ubuntu 24.04 running on Windows 11 with WSL2.

## Architecture

### High-Level Architecture

```text
                    TELEGRAM
                        |
                        v
                +----------------+
                |  Telegram Bot  |
                +----------------+
                        |
                        v
                +----------------+
                | User Access    |
                | Control        |
                +----------------+
                        |
                        v
                +----------------+
                | Security Layer |
                | Data Masking   |
                +----------------+
                        |
                        v
                +----------------+
                | Conversation   |
                | Memory (SQLite)|
                +----------------+
                        |
                        v
                +----------------+
                | LangGraph      |
                | ReAct Agent    |
                +----------------+
                        |
                        v
                +----------------+
                | Google Gemini  |
                | LLM            |
                +----------------+
                        |
             Agent Tool Selection
                        |
        +---------------+----------------+
        |               |                |
        v               v                v
+---------------+ +-------------+ +----------------+
| System        | | Docker      | | RAG Runbook    |
| Monitoring    | | Monitoring  | | Search Tool    |
+---------------+ +-------------+ +----------------+
        |               |                |
        v               v                v
     psutil          Docker CLI      Retriever
                                         |
                                         v
                                   +-------------+
                                   | ChromaDB    |
                                   | Vector Store|
                                   +-------------+
                                         ^
                                         |
                                  Similarity Search
                                         |
                                  Query Embedding
                                         |
                                  SentenceTransformers
                                  (Local CPU Model)

                        |
                        v
                +----------------+
                | Agent Response |
                +----------------+
                        |
                        v
                +----------------+
                | Output Masking |
                +----------------+
                        |
              +---------+---------+
              |                   |
              v                   v
        SQLite Memory       Telegram Response
```

### RAG Knowledge Base Ingestion Pipeline

The knowledge base is indexed separately from the Telegram conversation flow.

```text
       Knowledge Base Documents
          (MD / TXT / PDF)
                  |
                  v
          Document Loader
                  |
                  v
             Text Splitter
                  |
                  v
          Sentence Transformers
          Local Embedding Model
                  |
                  v
              ChromaDB
          Persistent Vector Store
                  |
                  v
          Ready for Retrieval
```

When an incident is received, the agent searches ChromaDB for relevant runbook content and uses the retrieved information to support its analysis.

### Incident Analysis Flow

1. Receive an incident alert or error log through Telegram.
2. Validate the Telegram user against the allowlist.
3. Mask sensitive information such as passwords, API keys, tokens, email addresses, and phone numbers.
4. Retrieve conversation history from SQLite.
5. Send the sanitized message and context to the LangGraph Agent.
6. The agent uses Gemini to reason and select relevant tools.
7. For incidents, the agent can search relevant runbooks through the RAG pipeline.
8. The agent produces an incident summary, possible root cause, recommended investigation steps, and a draft escalation.
9. Mask the generated response before saving and sending it.
10. Return the result to Telegram.

Root causes are treated as hypotheses unless supported by sufficient evidence. The agent does not automatically execute destructive or production-changing actions.

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
| RAG Framework | LangChain |
| Embedding Model | Sentence Transformers |
| Embedding Execution | Local CPU |
| Vector Database | ChromaDB |
| Knowledge Base | Markdown / TXT / PDF |
| Document Processing | PyPDF |
| System Monitoring | psutil |
| Container Monitoring | Docker CLI |
| Conversation Memory | SQLite |
| Security | Regex-based Sensitive Data Masking |
| Configuration | python-dotenv |
| Version Control | Git and GitHub |

## Current Features

- Telegram-based AI technical support interface.
- Gemini-powered conversational agent.
- LangGraph ReAct agent architecture.
- Linux CPU, RAM, disk, hostname, and uptime monitoring.
- Docker container monitoring.
- Telegram user ID allowlist.
- Persistent conversation history using SQLite.
- Conversation history management through `/clear`.
- RAG-based runbook retrieval.
- Document ingestion and text chunking.
- Local sentence-transformer embeddings.
- Persistent ChromaDB vector store.
- Sensitive data masking before LLM processing.
- Output masking before Telegram delivery and database storage.
- Incident analysis with RCA hypotheses and draft escalation.

## Telegram Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/help` | Display available commands |
| `/id` | Display Telegram user ID |
| `/status` | Check Linux system status |
| `/docker` | Check Docker containers |
| `/clear` | Clear conversation history |

Users can also submit incident alerts, timeout errors, and raw application logs as regular Telegram messages.

## Project Structure

```text
ai-technical-support-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── bot.py
│   ├── tools.py
│   ├── memory.py
│   ├── security/
│   │   ├── __init__.py
│   │   └── masking.py
│   └── rag/
│       ├── __init__.py
│       ├── loader.py
│       ├── chunker.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── tools.py
│       └── ingest.py
├── knowledge_base/
│   ├── runbooks/
│   │   └── connection-timeout.md
│   ├── incidents/
│   └── procedures/
├── data/
│   ├── chroma/
│   └── conversations.db
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Note: `data/chroma/` and `data/conversations.db` are generated at runtime and should not be committed to Git.

## Prerequisites

- Windows 11 with WSL2.
- Ubuntu 24.04.
- Python 3.12.
- Docker Desktop with WSL2 integration (for Docker monitoring).
- Google Gemini API key.
- Telegram Bot Token.

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

Configure:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_ALLOWED_USER_IDS=your_telegram_user_id
```

Never commit `.env` or expose API keys and bot tokens.

### 5. Index the knowledge base

```bash
python -m app.rag.ingest
```

This command loads documents from `knowledge_base/`, splits them into chunks, generates local embeddings, and stores them in ChromaDB.

Run this command again when you add or update knowledge base documents.

### 6. Start the Telegram bot

```bash
python -m app.bot
```

## Security Considerations

- API keys and Telegram bot tokens are stored in environment variables.
- Telegram access is restricted through a user ID allowlist.
- Incoming logs are sanitized before being passed to the LLM.
- Conversation history is sanitized before being reused as LLM context.
- Generated responses are sanitized before persistence and delivery.
- Initial infrastructure monitoring tools are read-only.
- Incident analysis provides recommendations and draft escalations; it does not automatically execute production-changing actions.
- Regex-based masking is a basic protection layer, not a complete Data Loss Prevention (DLP) solution.

## Development Roadmap

- [x] Python and WSL2 environment
- [x] Gemini API integration
- [x] Telegram bot integration
- [x] LangGraph ReAct agent
- [x] Linux system monitoring tools
- [x] Docker monitoring tools
- [x] Telegram user access control
- [x] SQLite conversation memory
- [x] RAG knowledge base
- [x] Document ingestion and chunking
- [x] Local embedding generation
- [x] ChromaDB vector store
- [x] Runbook retrieval tool
- [x] Sensitive data masking
- [x] Incident analysis and draft escalation
- [ ] Automated incident test suite
- [ ] Human approval workflow for sensitive operations
- [ ] Structured logging and observability
- [ ] Prometheus and Grafana integration
- [ ] Docker-based deployment
- [ ] Kubernetes deployment
- [ ] Production-grade security and evaluation

## Learning Objectives

This project is part of a hands-on learning journey toward AI Engineering, Agentic AI, and AI-powered infrastructure automation.

The focus is on understanding how LLMs, agents, tools, conversation memory, RAG, embeddings, vector databases, and DevOps infrastructure work together in a production-oriented system.

## License

MIT License.