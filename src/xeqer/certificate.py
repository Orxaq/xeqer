"""ProofCertificate — the output of a successful Xeqer verification."""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from xeqer.obligations import ProofObligation
from xeqer.solver import SolverResult


@dataclass
class ProofCertificate:
    spec_name: str
    spec_hash: str
    impl_hash: str
    status: str          # "PROVEN" | "FAILED" | "UNVERIFIABLE"
    obligations: list[dict]
    verified_at: str
    content_hash: str = field(default="")

    def to_json(self, indent: int = 2) -> str:
        body = {
            "spec_name": self.spec_name,
            "spec_hash": self.spec_hash,
            "impl_hash": self.impl_hash,
            "status": self.status,
            "obligations": self.obligations,
            "verified_at": self.verified_at,
        }
        canonical = json.dumps(body, sort_keys=True)
        content_hash = hashlib.sha256(canonical.encode()).hexdigest()
        body["content_hash"] = content_hash
        return json.dumps(body, indent=indent)


def build_certificate(
    spec_name: str,
    spec_hash: str,
    impl_hash: str,
    results: list[tuple[ProofObligation, SolverResult]],
) -> ProofCertificate:
    all_proved = all(r.proved for _, r in results)
    status = "PROVEN" if all_proved else "FAILED"
    obligations = [
        {
            "description": ob.description,
            "structure_type": ob.structure_type,
            "proved": r.proved,
            "counterexample": r.counterexample,
        }
        for ob, r in results
    ]
    return ProofCertificate(
        spec_name=spec_name,
        spec_hash=spec_hash,
        impl_hash=impl_hash,
        status=status,
        obligations=obligations,
        verified_at=datetime.now(timezone.utc).isoformat(),
    )
