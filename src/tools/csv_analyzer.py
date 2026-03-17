import re, pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class ToolResult:
    success: bool
    output: str
    tool: str = "csv_analyzer"
    error: str = ""

DEFAULT_PATH = "data/sample_metrics.csv"

def detect_intent(q):
    q = q.lower()
    if any(w in q for w in ["total","sum","how much"]): return "sum"
    if any(w in q for w in ["average","avg","mean"]): return "mean"
    if any(w in q for w in ["highest","maximum","top","best"]): return "max"
    if any(w in q for w in ["lowest","minimum","worst"]): return "min"
    if any(w in q for w in ["count","how many"]): return "count"
    return "summary"

def detect_filter(q):
    m = re.search(r"\bq([1-4])\b", q.lower())
    if m: return ("quarter", int(m.group(1)))
    return None

def analyze(question, data_path=DEFAULT_PATH):
    if not Path(data_path).exists(): return ToolResult(False,"","csv_analyzer",f"File not found: {data_path}")
    df = pd.read_csv(data_path)
    df.columns = [c.lower().replace(" ","_") for c in df.columns]
    filt = detect_filter(question)
    fdf = df.copy()
    if filt:
        ft, fv = filt
        if ft == "quarter" and "quarter" in df.columns: fdf = df[df["quarter"]==fv]
    intent = detect_intent(question)
    num_cols = fdf.select_dtypes(include="number").columns.tolist()
    target = next((c for c in num_cols if c.lower() in question.lower()), num_cols[0] if num_cols else None)
    if not target: return ToolResult(True, fdf.describe().to_string())
    try:
        if intent == "sum": v = fdf[target].sum(); return ToolResult(True, f"Total {target}: {v:,.2f}")
        if intent == "mean": v = fdf[target].mean(); return ToolResult(True, f"Average {target}: {v:,.2f}")
        if intent == "max": v = fdf[target].max(); return ToolResult(True, f"Maximum {target}: {v:,.2f}")
        if intent == "min": v = fdf[target].min(); return ToolResult(True, f"Minimum {target}: {v:,.2f}")
        if intent == "count": return ToolResult(True, f"Row count: {len(fdf):,}")
        return ToolResult(True, fdf[target].describe().to_string())
    except Exception as e:
        return ToolResult(False,"","csv_analyzer",str(e))
