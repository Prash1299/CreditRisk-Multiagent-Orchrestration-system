import ast


def run_python(expression: str) -> str:
    """Evaluate a simple arithmetic expression. Not a general interpreter."""
    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(
            node,
            (
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
            ),
        ):
            raise ValueError("Only arithmetic expressions are allowed")
    result = eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, {})
    return str(result)
