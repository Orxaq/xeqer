from pathlib import Path
from xeqer.ast_reader import load_spec, SpecModel

FIXTURE = Path(__file__).parent / "fixtures" / "divide.speqr.json"


def test_load_returns_spec_model():
    spec = load_spec(FIXTURE.read_text())
    assert isinstance(spec, SpecModel)
    assert spec.name == "Divide"


def test_load_inputs():
    spec = load_spec(FIXTURE.read_text())
    assert len(spec.inputs) == 2
    names = [i.name for i in spec.inputs]
    assert "numerator" in names
    assert "denominator" in names


def test_load_preconditions():
    spec = load_spec(FIXTURE.read_text())
    assert len(spec.preconditions) == 1
    assert "denominator" in spec.preconditions[0]


def test_load_postconditions():
    spec = load_spec(FIXTURE.read_text())
    assert len(spec.postconditions) == 1
