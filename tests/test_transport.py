from opendiag.transport import Transport


class DummyTransport:
    def send(
        self,
        data: bytes,
    ) -> None:
        pass

    def receive(
        self,
    ) -> bytes:
        return b""


def test_transport_protocol() -> None:
    transport: Transport = DummyTransport()

    assert transport.receive() == b""
