from pathlib import Path

from opendiag.uds.dtc_resolver import DTCResolver


def test_resolve_known_dtc() -> None:
    resolver = DTCResolver(
        Path("data/dtcs/generic.json"),
    )

    result = resolver.resolve(0x010700)

    assert result is not None
    assert result["description"] == "DTC de teste"
    assert result["system"] == "Motor"
    assert result["severity"] == "warning"


def test_resolve_unknown_dtc() -> None:
    resolver = DTCResolver(
        Path("data/dtcs/generic.json"),
    )

    result = resolver.resolve(0xFFFFFF)

    assert result is None
