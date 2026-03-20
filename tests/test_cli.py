import json
from pathlib import Path
from typer.testing import CliRunner
from xeqer.cli import app

runner = CliRunner()
FIXTURES = Path(__file__).parent / "fixtures"


def test_verify_outputs_status():
    result = runner.invoke(app, [
        str(FIXTURES / "divide.speqr.json"),
        str(FIXTURES / "divide.py"),
    ])
    # Should complete without crashing; status depends on Z3 proof result
    assert result.exit_code in (0, 1)
    assert "Divide" in result.output


def test_verify_outputs_certificate(tmp_path):
    cert_path = tmp_path / "cert.json"
    result = runner.invoke(app, [
        str(FIXTURES / "divide.speqr.json"),
        str(FIXTURES / "divide.py"),
        "--output", str(cert_path),
    ])
    assert cert_path.exists()
    data = json.loads(cert_path.read_text())
    assert "content_hash" in data


def test_verify_missing_spec():
    result = runner.invoke(app, ["missing.json", "divide.py"])
    assert result.exit_code != 0
