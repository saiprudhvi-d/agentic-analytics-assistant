# Agentic Analytics Assistant

![Tests](https://github.com/saiprudhvi-d/agentic-analytics-assistant/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)

Tool-routing AI agent that answers business analytics questions by routing to the right tool.

## Tools
- **Calculator** — safe AST-based arithmetic evaluator
- **CSV Analyzer** — pandas aggregations on business metrics
- **Summarizer** — LLM-powered text summarization

## Stack
Python · LangChain · OpenAI · FastAPI

## Setup
```bash
git clone https://github.com/saiprudhvi-d/agentic-analytics-assistant
pip install -r requirements.txt
cp .env.example .env  # Add OPENAI_API_KEY
uvicorn app.app:app --reload
```

## CI/CD
Tests run automatically on every push via GitHub Actions.