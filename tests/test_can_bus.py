import pytest

from opendiag.bus.base import CANBus


def test_can_bus_is_abstract() -> None:
    with pytest.raises(TypeError):
        CANBus()
