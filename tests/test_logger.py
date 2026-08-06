from opendiag.core.can_frame import CANFrame
from opendiag.logger import Logger

print("========== TEST LOGGER ==========")
print("Logger =", Logger)
print("CANFrame =", CANFrame)
print("===============================")


def test_logger_creation() -> None:
    logger = Logger()

    assert logger is not None


def test_logger_methods() -> None:
    logger = Logger()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")


def test_can_rx_log(caplog) -> None:
    logger = Logger()

    frame = CANFrame(
        arbitration_id=0x7E0,
        data=b"\x02\x10\x03",
        timestamp=0.0,
    )

    logger.can_rx(frame)

    assert "CAN RX" in caplog.text
    assert "7E0 [3] 02 10 03" in caplog.text


def test_can_tx_log(caplog) -> None:
    logger = Logger()

    frame = CANFrame(
        arbitration_id=0x7DF,
        data=b"\x02\x01\x0c\x00\x00\x00\x00\x00",
        timestamp=0.0,
    )

    logger.can_tx(frame)

    assert "CAN TX" in caplog.text
    assert "7DF [8] 02 01 0C 00 00 00 00 00" in caplog.text
