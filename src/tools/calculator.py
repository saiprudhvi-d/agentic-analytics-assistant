import re, ast, operator
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    output: str
    tool: str = "calculator"
    error: str = ""

SAFE_NODES = {ast.Expression,ast.BinOp,ast.UnaryOp,ast.Constant,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow,ast.Mod,ast.FloorDiv,ast.USub,ast.UAdd}
OPS = {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.FloorDiv:operator.floordiv,ast.Pow:operator.pow,ast.Mod:operator.mod,ast.USub:operator.neg,ast.UAdd:operator.pos}

def _eval(node):
    if isinstance(node, ast.Expression): return _eval(node.body)
    elif isinstance(node, ast.Constant) and isinstance(node.value,(int,float)): return float(node.value)
    elif isinstance(node, ast.BinOp): return OPS[type(node.op)](_eval(node.left),_eval(node.right))
    elif isinstance(node, ast.UnaryOp): return OPS[type(node.op)](_eval(node.operand))
    raise ValueError(f"Unsafe: {type(node)}")

def extract_expression(q):
    m = re.search(r"(\d+(?:\.\d+)?)\s*%\s*of\s*([\d,]+(?:\.\d+)?)", q, re.IGNORECASE)
    if m: return f"{m.group(1)} / 100 * {m.group(2).replace(',','')}"
    cleaned = re.sub(r"[^0-9+\-*/().\s]"," ",q)
    m2 = re.search(r"[\d][\d\s+\-*/().]*[\d]", cleaned)
    return m2.group(0).strip() if m2 else cleaned.strip()

def calculate(question):
    try:
        expr = extract_expression(question)
        if not expr: return ToolResult(False,"","calculator","No expression found")
        tree = ast.parse(expr, mode="eval")
        if not all(type(n) in SAFE_NODES for n in ast.walk(tree)):
            return ToolResult(False,"","calculator","Unsafe expression")
        result = _eval(tree)
        fmt = f"{int(result):,}" if result == int(result) else f"{result:,.2f}"
        return ToolResult(True, f"The result is {fmt}")
    except ZeroDivisionError:
        return ToolResult(False,"","calculator","Division by zero")
    except Exception as e:
        return ToolResult(False,"","calculator",str(e))
