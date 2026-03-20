from xeqer.solver import discharge, SolverResult
from xeqer.obligations import ProofObligation


def test_trivially_true_obligation_passes():
    ob = ProofObligation(
        formula="BoolVal(True)",
        description="trivially true",
        structure_type="atom",
    )
    result = discharge(ob)
    assert result.proved


def test_trivially_false_obligation_fails():
    ob = ProofObligation(
        formula="BoolVal(False)",
        description="trivially false",
        structure_type="atom",
    )
    result = discharge(ob)
    assert not result.proved


def test_simple_arithmetic_obligation():
    ob = ProofObligation(
        formula="Implies(x > 0, x + 1 > 0)",
        description="x+1 > 0 when x > 0",
        structure_type="atom",
        variables=["x"],
    )
    result = discharge(ob)
    assert result.proved


def test_counterexample_found():
    ob = ProofObligation(
        formula="Implies(x > 0, x > 1)",
        description="x > 1 when x > 0 (false)",
        structure_type="atom",
        variables=["x"],
    )
    result = discharge(ob)
    assert not result.proved
    assert result.counterexample is not None
