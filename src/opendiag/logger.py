"""
Public logger API.

Exposes the logger implementation through a simplified public name,
keeping the concrete logger class hidden from callers.
"""

from opendiag.core.logger import OpenDiagLogger as Logger

__all__ = ["Logger"]
