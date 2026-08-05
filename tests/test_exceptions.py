from opendiag.core.exceptions import (
    BusError,
    ConfigurationError,
    DecodeError,
    OpenDiagError,
    PluginError,
    ProtocolError,
    SecurityError,
    TimeoutError,
    TransportError,
)


def test_all_exceptions_inherit_from_opendiag_error():
    exceptions = [
        ConfigurationError,
        BusError,
        TransportError,
        ProtocolError,
        TimeoutError,
        DecodeError,
        SecurityError,
        PluginError,
    ]

    for exc in exceptions:
        assert issubclass(exc, OpenDiagError)
