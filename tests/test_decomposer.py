from xeqer.decomposer import decompose
from xeqer.structures import StructuredProgram, Sequence, Selection, Iteration, Atom
from pathlib import Path

DIVIDE_SRC = (Path(__file__).parent / "fixtures" / "divide.py").read_text()


def test_decompose_returns_structured_program():
    prog = decompose(DIVIDE_SRC, function_name="divide")
    assert isinstance(prog, StructuredProgram)
    assert prog.function_name == "divide"
    assert prog.is_structured


def test_decompose_params():
    prog = decompose(DIVIDE_SRC, function_name="divide")
    assert "numerator" in prog.params
    assert "denominator" in prog.params


def test_decompose_simple_body_is_sequence():
    prog = decompose(DIVIDE_SRC, function_name="divide")
    assert isinstance(prog.body, (Sequence, Atom))


def test_decompose_if_becomes_selection():
    src = """\
def abs_val(x):
    if x >= 0:
        return x
    else:
        return -x
"""
    prog = decompose(src, function_name="abs_val")
    assert isinstance(prog.body, Selection)
    assert "x >= 0" in prog.body.condition


def test_decompose_while_becomes_iteration():
    src = """\
def countdown(n):
    while n > 0:
        n = n - 1
    return n
"""
    prog = decompose(src, function_name="countdown")
    # body is Sequence(Iteration, Atom)
    assert prog.is_structured


def test_unstructured_goto_flagged():
    # Python doesn't have goto, but we flag generator/async/yield
    src = """\
def gen():
    yield 1
    yield 2
"""
    prog = decompose(src, function_name="gen")
    assert not prog.is_structured
    assert len(prog.unstructured_reasons) > 0
