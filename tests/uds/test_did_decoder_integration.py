from pathlib import Path

from opendiag.uds.did_decoder import DIDDecoder
from opendiag.uds.did_resolver import DIDResolver


def test_resolve_and_decode_vin() -> None:
    resolver = DIDResolver(
        Path("data/dids/generic.json"),
    )

    definition = resolver.resolve(0xF190)

    assert definition is not None
    assert definition.name == "VIN"
    assert definition.type == "ascii"
    assert definition.length == 17

    decoder = DIDDecoder()

    value = decoder.decode(
        definition,
        b"1HGCM82633A004352",
    )

    assert value == "1HGCM82633A004352"


def test_resolve_and_decode_uint16_did() -> None:
    resolver = DIDResolver(
        Path("data/dids/generic.json"),
    )

    decoder = DIDDecoder()

    definition = resolver.resolve(0xF191)

    assert definition is not None
    assert definition.name == "Example Numeric Value"
    assert definition.type == "uint16"
    assert definition.length == 2

    value = decoder.decode(
        definition,
        b"\x12\x34",
    )

    assert value == 0x1234
