from opendiag.uds.did_decoder import DIDDecoder
from opendiag.uds.did_resolver import DIDDefinition


def test_decode_ascii_did() -> None:
    definition = DIDDefinition(
        name="VIN",
        type="ascii",
        length=17,
    )

    decoder = DIDDecoder()

    value = decoder.decode(
        definition,
        b"1HGCM82633A004352",
    )

    assert value == "1HGCM82633A004352"


def test_decode_ascii_rejects_invalid_length() -> None:
    definition = DIDDefinition(
        name="VIN",
        type="ascii",
        length=17,
    )

    decoder = DIDDecoder()

    try:
        decoder.decode(
            definition,
            b"ABC",
        )
    except ValueError as exc:
        assert "Expected 17 bytes" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_decode_ascii_rejects_invalid_ascii() -> None:
    definition = DIDDefinition(
        name="VIN",
        type="ascii",
        length=3,
    )

    decoder = DIDDecoder()

    try:
        decoder.decode(
            definition,
            b"\xff\xfe\xfd",
        )
    except ValueError as exc:
        assert "ASCII" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_decode_rejects_unsupported_type() -> None:
    definition = DIDDefinition(
        name="TEST",
        type="unknown",
        length=1,
    )

    decoder = DIDDecoder()

    try:
        decoder.decode(
            definition,
            b"\x01",
        )
    except ValueError as exc:
        assert "Unsupported DID type" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_decode_uint8() -> None:
    definition = DIDDefinition(
        name="Example",
        type="uint8",
        length=1,
    )

    decoder = DIDDecoder()

    assert decoder.decode(definition, b"\x2a") == 42


def test_decode_uint16() -> None:
    definition = DIDDefinition(
        name="Example",
        type="uint16",
        length=2,
    )

    decoder = DIDDecoder()

    assert (
        decoder.decode(
            definition,
            b"\x12\x34",
        )
        == 0x1234
    )


def test_decode_uint32() -> None:
    definition = DIDDefinition(
        name="Example",
        type="uint32",
        length=4,
    )

    decoder = DIDDecoder()

    assert (
        decoder.decode(
            definition,
            b"\x12\x34\x56\x78",
        )
        == 0x12345678
    )
