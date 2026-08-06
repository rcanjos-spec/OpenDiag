from opendiag.protocols.isotp import ISOTPFrame


def test_parse_single_frame() -> None:
    frame = ISOTPFrame.from_can_data(b"\x03\x22\xf1\x90")

    assert frame.length == 3
    assert frame.payload == b"\x22\xf1\x90"
