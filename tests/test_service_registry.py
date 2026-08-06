from opendiag.uds.registry import ServiceRegistry
from opendiag.uds.services.base import BaseService


class DummyService(BaseService):
    def execute(
        self,
        request,
        transport,
    ):
        return None


def test_register_service() -> None:
    registry = ServiceRegistry()

    registry.register(
        0x22,
        DummyService,
    )

    assert registry.get(0x22) is DummyService
