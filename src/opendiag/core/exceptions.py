"""
OpenDiag exception hierarchy.

Every exception raised by OpenDiag should inherit from OpenDiagError.
"""


class OpenDiagError(Exception):
    """Base exception for all OpenDiag errors."""


class ConfigurationError(OpenDiagError):
    """Configuration related error."""


class BusError(OpenDiagError):
    """Bus communication error."""


class TransportError(OpenDiagError):
    """Transport layer error."""


class ProtocolError(OpenDiagError):
    """Protocol processing error."""


class TimeoutError(OpenDiagError):
    """Communication timeout."""


class DecodeError(OpenDiagError):
    """Frame decoding error."""


class SecurityError(OpenDiagError):
    """Security access error."""


class PluginError(OpenDiagError):
    """Plugin related error."""
