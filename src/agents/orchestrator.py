import re
from dataclasses import dataclass
from src.tools.calculator import calculate, ToolResult as CalcResult
from src.tools.csv_analyzer import analyze, ToolResult as DataResult

@dataclass
class AgentResponse:
    answer: str
    tool_used: str
    reasoning: str
    confidence: str
    success: bool

CALC_PATTERNS = [r"\d+\s*[+\-*/]\s*\d+",r"\d+\s*%\s*of\s*[\d,]+",r"(what is|calculate|compute)\s.*\d",r"(multiply|divide|add|subtract|times|plus|minus)"]
DATA_PATTERNS = [r"(total|sum|average|avg|highest|lowest|count|how many)\s.*(revenue|sales|profit|cost|orders)",r"(q[1-4]|quarter|month|monthly)",r"(top|best|worst|maximum|minimum)\s.*(product|region)"]
SUM_PATTERNS = [r"(summarize|summary|overview|brief|key (points|takeaways))",r"(explain|describe|what does|what are the main)"]

def classify_intent(q):
    ql = q.lower()
    for p in CALC_PATTERNS:
        if re.search(p, ql): return "calculation","high"
    for p in DATA_PATTERNS:
        if re.search(p, ql): return "data_query","high"
    for p in SUM_PATTERNS:
        if re.search(p, ql): return "summarize","high"
    return "unknown","low"

def _llm_summarize(q):
    try:
        from openai import OpenAI
        r = OpenAI().chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":q}], max_tokens=300)
        return AgentResponse(r.choices[0].message.content.strip(),"summarizer","LLM summarization","high",True)
    except:
        return AgentResponse("LLM unavailable. Set OPENAI_API_KEY.","summarizer","LLM routing attempted","low",False)

def run_agent(question, data_path="data/sample_metrics.csv"):
    if not question or not question.strip():
        return AgentResponse("Please provide a question.","none","Empty input","high",False)
    intent, conf = classify_intent(question)
    if intent == "calculation":
        r = calculate(question)
        return AgentResponse(r.output if r.success else f"Error: {r.error}","calculator","Arithmetic intent detected",conf,r.success)
    elif intent == "data_query":
        r = analyze(question, data_path)
        return AgentResponse(r.output if r.success else f"Error: {r.error}","csv_analyzer","Data query intent detected",conf,r.success)
    elif intent == "summarize":
        return _llm_summarize(question)
    return AgentResponse("I can help with: calculations, data questions, or summaries.","fallback","Unknown intent","low",False)
