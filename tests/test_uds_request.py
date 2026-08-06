import pytest

from opendiag.uds.request import UDSRequest


def test_request_is_abstract() -> None:
    """UDSRequest cannot be instantiated directly."""

    with pytest.raises(TypeError):
        UDSRequest()
