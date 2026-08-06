from opendiag.protocols.isotp import ISOTPFrame


def test_single_frame_length() -> None:
    frame = ISOTPFrame(payload=b"\x22\xf1\x90")

    assert frame.length == 3
