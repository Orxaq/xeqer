"""Decompose a Python function into Böhm-Jacopini structures."""
from __future__ import annotations
import ast
from xeqer.structures import (
    Structure, Atom, Sequence, Selection, Iteration, StructuredProgram,
)


def decompose(source: str, function_name: str) -> StructuredProgram:
    """Parse Python source and decompose the named function."""
    tree = ast.parse(source)
    func = _find_function(tree, function_name)
    if func is None:
        raise ValueError(f"Function '{function_name}' not found in source")

    unstructured: list[str] = []
    _check_unstructured(func, unstructured)

    body = _decompose_stmts(func.body)
    params = [a.arg for a in func.args.args]

    return StructuredProgram(
        function_name=function_name,
        params=params,
        body=body,
        is_structured=len(unstructured) == 0,
        unstructured_reasons=unstructured,
    )


def _find_function(tree: ast.Module, name: str) -> ast.FunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def _check_unstructured(func: ast.FunctionDef, reasons: list[str]) -> None:
    for node in ast.walk(func):
        if isinstance(node, (ast.Yield, ast.YieldFrom)):
            reasons.append("yield/generator not supported in v0.1.0")
        elif isinstance(node, ast.AsyncFunctionDef):
            reasons.append("async function not supported in v0.1.0")


def _decompose_stmts(stmts: list[ast.stmt]) -> Structure:
    items = [_decompose_stmt(s) for s in stmts]
    if len(items) == 1:
        return items[0]
    return Sequence(items=items)


def _decompose_stmt(stmt: ast.stmt) -> Structure:
    if isinstance(stmt, ast.If):
        return Selection(
            condition=ast.unparse(stmt.test),
            then_branch=_decompose_stmts(stmt.body),
            else_branch=_decompose_stmts(stmt.orelse) if stmt.orelse else None,
        )
    elif isinstance(stmt, (ast.While, ast.For)):
        cond = (
            ast.unparse(stmt.test)
            if isinstance(stmt, ast.While)
            else f"for {ast.unparse(stmt.target)} in {ast.unparse(stmt.iter)}"
        )
        return Iteration(condition=cond, body=_decompose_stmts(stmt.body))
    else:
        return Atom(source=ast.unparse(stmt), lineno=stmt.lineno)
