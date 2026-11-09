import ast

from tools.financial_tools import foir, monthly_emi


_ALLOWED = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Mod,
    ast.FloorDiv,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.keyword,
    ast.Tuple,
    ast.List,
)


def run_python(expression: str) -> str:
    """Evaluate a constrained arithmetic / EMI expression."""
    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in {"emi", "foir", "round"}:
                raise ValueError("Only emi(), foir(), and round() calls are allowed")
        elif not isinstance(node, _ALLOWED):
            raise ValueError("Expression is not allowed in the sandbox")
    env = {
        "emi": monthly_emi,
        "foir": foir,
        "round": round,
    }
    result = eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, env)
    return str(result)
