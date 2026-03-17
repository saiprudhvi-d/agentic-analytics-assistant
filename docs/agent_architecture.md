# Agent Architecture

## Decision Flow
```
User Question
      |
      v
[Pattern Matcher] ~1ms
  |- calculation  -> Calculator Tool
  |- data_query   -> CSV Analyzer
  |- summarize    -> LLM Summarizer
  |- no match
          |
          v
    [Fallback: clarification prompt]
```

## Tool Selection
- **Calculator**: safe AST-based arithmetic, no eval()
- **CSV Analyzer**: pandas aggregations on sample_metrics.csv
- **Summarizer**: OpenAI gpt-4o-mini (requires OPENAI_API_KEY)
