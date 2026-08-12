from pathlib import Path

from opendiag.uds.did_resolver import DIDResolver


def test_resolve_known_did() -> None:
    resolver = DIDResolver(
        Path("data/dids/generic.json"),
    )

    did = resolver.resolve(0xF190)

    assert did.name == "VIN"
    assert did.type == "ascii"
    assert did.length == 17


def test_resolve_unknown_did() -> None:
    resolver = DIDResolver(
        Path("data/dids/generic.json"),
    )

    did = resolver.resolve(0x1234)

    assert did is None
