from opendiag.core.logger import OpenDiagLogger


def test_logger_creation() -> None:
    logger = OpenDiagLogger()

    assert logger is not None


def test_logger_methods() -> None:
    logger = OpenDiagLogger()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
