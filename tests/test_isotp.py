from opendiag.protocols.isotp import ISOTPFrame


def test_single_frame_creation() -> None:
    frame = ISOTPFrame(payload=b"\x22\xf1\x90")

    assert frame.payload == b"\x22\xf1\x90"
