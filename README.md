# Agentic Analytics Assistant

![Tests](https://github.com/saiprudhvi-d/agentic-analytics-assistant/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangChain](https://img.shields.io/badge/LangChain-Agents-green)

## Overview
A tool-routing AI agent that answers business analytics questions by deciding which tool to invoke — calculator, CSV data analyzer, or LLM summarizer — rather than routing everything through a single prompt.

## Business Problem
A business analyst needs answers to diverse questions: calculations, data trends, and report summaries — all in natural language. This assistant routes each query to the right tool based on intent, returning a structured response with reasoning trace.

## Agent Workflow
```
User Question → [Intent Classifier: regex patterns ~1ms]
  ├── calculation  → [Calculator Tool]   safe AST eval, no exec()
  ├── data_query   → [CSV Analyzer]      pandas aggregations
  ├── summarize    → [LLM Summarizer]    OpenAI gpt-4o-mini
  └── unknown      → [Fallback]          clarification prompt
```

## Example Outputs
- *"What is 15% of 84500?"* → Calculator → **"The result is 12,675.00"**
- *"Total revenue in Q3?"* → CSV Analyzer → **"Total revenue: 684,000.00"**

## Tech Stack
Python · LangChain · OpenAI · FastAPI · pandas · pytest · GitHub Actions

## Setup
```bash
git clone https://github.com/saiprudhvi-d/agentic-analytics-assistant
pip install -r requirements.txt
cp .env.example .env  # Add OPENAI_API_KEY
uvicorn app.app:app --reload
```

## Future Improvements
- SQL query generation tool
- Session memory for multi-turn conversations
- Streaming responses via WebSocket