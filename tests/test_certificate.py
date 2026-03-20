import json, hashlib
from xeqer.certificate import build_certificate, ProofCertificate
from xeqer.solver import SolverResult
from xeqer.obligations import ProofObligation


def _make_results(proved: bool) -> list[tuple[ProofObligation, SolverResult]]:
    ob = ProofObligation("True", "test", "atom")
    return [(ob, SolverResult(proved=proved))]


def test_certificate_is_json_serializable():
    cert = build_certificate(
        spec_name="Divide",
        spec_hash="abc123",
        impl_hash="def456",
        results=_make_results(True),
    )
    json_str = cert.to_json()
    data = json.loads(json_str)
    assert data["spec_name"] == "Divide"


def test_certificate_status_proven():
    cert = build_certificate("X", "a", "b", _make_results(True))
    assert cert.status == "PROVEN"


def test_certificate_status_failed():
    cert = build_certificate("X", "a", "b", _make_results(False))
    assert cert.status == "FAILED"


def test_certificate_has_content_hash():
    cert = build_certificate("X", "a", "b", _make_results(True))
    data = json.loads(cert.to_json())
    assert "content_hash" in data
    # Verify the hash
    content = json.dumps({k: v for k, v in data.items() if k != "content_hash"},
                         sort_keys=True)
    expected = hashlib.sha256(content.encode()).hexdigest()
    assert data["content_hash"] == expected
