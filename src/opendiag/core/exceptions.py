"""
Exception hierarchy.

All project-specific exceptions inherit from KACTOENGError, allowing
callers to catch either a specific error or the common base exception.
"""


class OpenDiagError(Exception):
    """Base exception for all project-specific errors."""


class ConfigurationError(OpenDiagError):
    """Configuration-related error."""


class BusError(OpenDiagError):
    """CAN bus communication error."""


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
    """Plugin-related error."""
