from xeqer.proof_rules import rule_sequence, rule_selection, rule_iteration
from xeqer.structures import Sequence, Selection, Iteration, Atom
from xeqer.obligations import ProofObligation


def test_rule_sequence_generates_intermediate():
    a1 = Atom("x = 1", lineno=1)
    a2 = Atom("y = x + 1", lineno=2)
    seq = Sequence([a1, a2])
    obligations = rule_sequence(seq, precondition="True", postcondition="y == 2")
    # Sequence rule: must have at least one intermediate obligation
    assert len(obligations) >= 1
    assert all(isinstance(o, ProofObligation) for o in obligations)


def test_rule_selection_generates_two_branches():
    sel = Selection(
        condition="x >= 0",
        then_branch=Atom("result = x", lineno=2),
        else_branch=Atom("result = -x", lineno=4),
    )
    obligations = rule_selection(sel, precondition="True", postcondition="result >= 0")
    # Selection rule: two branches → two obligations
    assert len(obligations) == 2


def test_rule_selection_no_else_generates_one_branch():
    sel = Selection(
        condition="x > 0",
        then_branch=Atom("x = x - 1", lineno=2),
        else_branch=None,
    )
    obligations = rule_selection(sel, precondition="x >= 0", postcondition="x >= 0")
    assert len(obligations) >= 1


def test_rule_iteration_requires_invariant():
    it = Iteration(condition="n > 0", body=Atom("n = n - 1", lineno=2))
    obligations = rule_iteration(it, precondition="n >= 0", postcondition="n == 0")
    # Without invariant annotation, generates a placeholder obligation
    assert any("invariant" in o.description.lower() for o in obligations)
