import pytest

from opendiag.uds.services.base import BaseService


def test_base_service_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseService()
