from opendiag.uds.client import UDSClient


def test_create_client() -> None:
    client = UDSClient(
        transport=object(),
        registry=object(),
    )

    assert client is not None
