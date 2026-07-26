# 🎓 Interview Preparation Coach

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Groq Llama-3.1](https://img.shields.io/badge/LLM-Groq%20Llama--3.1--8B-orange.svg)](https://groq.com/)
[![OpenRouter GPT-4o](https://img.shields.io/badge/LLM-OpenRouter%20GPT--4o--Mini-purple.svg)](https://openrouter.ai/)
[![Chroma Vector DB](https://img.shields.io/badge/RAG-ChromaDB-green.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Academic Module](https://img.shields.io/badge/Module-IT41043-lightgrey.svg)]()

> **An Agentic AI Multi-Agent Preparation, Strategy Coaching & Industry Outreach Platform.**  
> Built as Phase 5 (Final Phase) for academic module IT41043 (Due: 27th July 2026).

---

## 📌 Project Overview

**Interview Preparation Coach** is an intelligent, full-stack multi-agent platform designed to help job candidates master technical interviews, behavioral questions, and professional industry networking. Driven by an autonomous orchestration architecture, the platform integrates **Retrieval-Augmented Generation (RAG)** over role-specific vector databases, a **ReAct Content Evaluation Agent**, and a **Two-Stage Self-Critique Evaluation Engine**.

The system dynamically adapts across four target professional domains:
- 💻 **Software Engineering** (OOP, System Architecture, DBMS, Networks, OS)
- 📊 **Data Analysis & Engineering** (SQL Window Functions, A/B Testing, ETL Pipelines, Pandas)
- 📦 **Product Management** (RICE Framework, Product Discovery, DAU/MAU Metrics, Strategy)
- 🎨 **UX/UI Design** (Nielsen Heuristics, Card Sorting, Wireframing, Accessibility Frameworks)

---

## 🖥️ Application Showcase

![Interview Preparation Coach Home UI](assets/home_ui.png)

---

## ✨ Key Features & Capabilities

### 🎯 1. Interactive Practice Studio (Tab 1)
- **Role-Aware Technical Question Bank**: Vector-retrieved questions customized for Software Engineers, Data Analysts, Product Managers, and UX Designers.
- **Dynamic Complexity Selector**: Switch between `Easy` (Fundamentals), `Medium` (Standard Interview), and `Hard` (Senior/Lead) complexity levels on the fly.
- **Clean Card Presentation**: Custom glassmorphism UI containers featuring role, topic, and difficulty badges with **zero raw markdown leaks**.
- **💡 Interactive Hint Expander**: On-demand hint drawers providing core concept guidance before answering.
- **✍️ Real-Time Response Gauge**: Live word counter tracking response length.

### 📝 2. Autonomous Dual-LLM AI Evaluation & Reflection Engine
- **Two-Stage Evaluation**: 
  1. *Draft Evaluation*: Compares candidate response against vector reference answer key for conceptual accuracy.
  2. *Self-Critique Reflection*: Senior Reviewer prompt revises draft score for fairness and constructiveness.
- **Resilient Multi-Model Failover**: Primary evaluation driven by OpenRouter (`openai/gpt-4o-mini`) with automatic fallback to Groq (`llama-3.1-8b-instant`).
- **💡 Automatic Correct Answer Display**: Automatically reveals the **Expected Model Answer Box** right on screen whenever an answer receives a score lower than 8.

### 📊 3. Interactive Performance Report Dashboard
- **Performance Tier Badging**: Automatically classifies candidate session performance into *Master Class* (90%+), *Solid Competency* (70%+), or *Practice Recommended* (<65%).
- **📈 Interactive Score Bar Chart**: Renders `st.bar_chart` visual plotting candidate score per question.
- **🔍 Color-Coded Review Accordions**: Expandable history cards color-coded by score (🟢 Green for 8-10, 🟡 Amber for 6-7, 🔴 Red for 0-5).
- **📥 One-Click Export**: Download a full Markdown report (`interview_report.md`) for offline review.

### 💡 4. Interview Technique & Strategy Studio (Tab 2)
- **🌟 Interactive STAR Methodology Builder**: 4-step interactive workspace (Situation, Task, Action, Result) allowing candidates to draft, preview, and refine behavioral answers in real-time.
- **🤖 Unified RAG Strategy Tips**: Retrieves structured interview techniques from vector storage, displaying clean **Candidate Pitfall (❌)** vs **Coach Action Plan (💡)** side-by-side cards.

### 🤝 5. Expert Networking & Outreach Studio (Tab 3)
- **🚀 3-Step Networking Playbook**: Visual guidance cards breaking down Target Prospecting, 300-Char Hook Notes, and 15-Minute Coffee Chats.
- **✉️ Interactive Outreach Template Builder**: Customizable message generator for 5 scenarios (*Alumni Connection*, *Informational Interview*, *Post-Event Follow-up*, *Referral Request*, *Role-Specific Cold Outreach*).
- **🤖 RAG Strategic Networking Advice**: Vector retrieval pulling real networking strategy insights without returning raw template placeholders.

---

## 🏗️ Multi-Agent System Architecture

The platform is powered by four decoupled, specialized agents communicating via typed dataclasses (`protocol/messages.py`):

```
                       ┌────────────────────────┐
                       │   Streamlit Web UI     │
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │ InterviewOrchestrator  │
                       └───────────┬────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   RouterAgent    │      │  QuestionAgent   │      │    CoachAgent    │
│ (Classifies topic│      │(ReAct Retrieve/  │      │(Draft + Critique │
│   & collection)  │      │   Generate)      │      │ LLM Evaluation)  │
└────────┬─────────┘      └────────┬─────────┘      └────────┬─────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │ ChromaDB Vector Engine │
                       │(3 Embedding Collections│
                       └────────────────────────┘
```

### Agent Roles:
1. **`InterviewOrchestrator`** (`agents/orchestrator.py`): Central session state manager coordinating requests between agents and maintaining running history and score statistics.
2. **`RouterAgent`** (`agents/router_agent.py`): Classifies panel intent and maps queries to target vector collections (`technical_qa`, `interview_tips`, `networking_advice`).
3. **`QuestionAgent`** (`agents/question_agent.py`): Executes ReAct retrieve-vs-generate workflow over ChromaDB vector embeddings (`all-MiniLM-L6-v2`) and parses clean question prompts.
4. **`CoachAgent`** (`agents/coach_agent.py`): Runs two-stage draft evaluation and self-critique reflection with multi-model failover (OpenRouter → Groq).

---

## 📁 Repository Directory Structure

```
interview-prep-coach/
├── agents/
│   ├── coach_agent.py          # Dual-stage evaluation agent with model failover
│   ├── orchestrator.py         # Multi-agent session orchestrator
│   ├── question_agent.py       # ReAct retrieval & question agent
│   └── router_agent.py         # Intent classification & collection router
├── assets/
│   └── home_ui.png             # UI Screenshot for README
├── kb/
│   ├── documents/              # Markdown knowledge base source files
│   │   ├── technical_qa/       # Q&A datasets (SE, Data Analyst, PM, UX)
│   │   ├── interview_tips/     # STAR method, body language, mistakes
│   │   └── networking_advice/  # Prospecting, informational chats, referrals
│   ├── ingest.py               # Vector database ingestion pipeline script
│   └── retriever.py            # ChromaDB similarity retriever & metadata filter
├── models/
│   ├── groq_client.py          # Groq Llama-3.1 API wrapper
│   └── openrouter_client.py    # OpenRouter GPT-4o-mini API wrapper
├── protocol/
│   └── messages.py             # Typed dataclasses for inter-agent messaging
├── tests/
│   ├── test_agents.py          # End-to-end agent orchestration test suite
│   └── test_retrieval.py       # ChromaDB vector retrieval test suite
├── .env                        # Environment variables (API keys)
├── .gitignore                  # Git ignore file (.env, venv, chromadb)
├── app.py                      # Main Streamlit UI web application
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

---

## ⚡ Getting Started & Setup Guide

### 1. Prerequisites
- Python `3.10` or higher installed on your system.
- Git installed.

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone repository
git clone https://github.com/Janadari1213/Interview-Preparation-Coach.git
cd Interview-Preparation-Coach/interview-prep-coach

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Secrets / API Keys
Create a `.env` file in the project root (`interview-prep-coach/.env`) or configure `.streamlit/secrets.toml`:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
OPENROUTER_API_KEY=sk-or-v1-your_openrouter_api_key_here
```

### 5. Ingest Knowledge Base into Vector Database
Run the ingestion pipeline to embed markdown knowledge documents into ChromaDB:

```bash
python kb/ingest.py
```

*Output summary:*
```
--- Ingestion Summary ---
Collection 'technical_qa': 43 chunks loaded.
Collection 'interview_tips': 8 chunks loaded.
Collection 'networking_advice': 6 chunks loaded.
-------------------------
```

### 6. Run the Application
Launch the Streamlit web application:

```bash
python -m streamlit run app.py
```

Open your browser at **`http://localhost:8501`**.

---

## 🧪 Running Unit & Integration Tests

Run the automated test suite to verify agent orchestration and vector retrieval:

```bash
# Test Agent Orchestration Pipeline
python tests/test_agents.py

# Test ChromaDB Vector Retrieval
python tests/test_retrieval.py
```

---

## 📜 Academic Metadata & License

- **Course Module**: IT41043 — Agentic AI Applications
- **Project Phase**: Phase 5 (Final Phase - Complete Delivery)
- **Submission Date**: 27th July 2026
- **License**: [MIT License](LICENSE)
