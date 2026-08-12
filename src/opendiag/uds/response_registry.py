"""
UDS response registry.

Maps UDS response service identifiers to the classes responsible
for decoding those responses.
"""

from opendiag.uds.response import NegativeResponse
from opendiag.uds.responses.diagnostic_session_control import (
    DiagnosticSessionControlResponse,
)
from opendiag.uds.responses.ecu_reset import ECUResetResponse
from opendiag.uds.responses.read_data_by_identifier import (
    ReadDataByIdentifierResponse,
)
from opendiag.uds.responses.read_dtc_information import (
    ReadDTCInformationResponse,
)
from opendiag.uds.responses.security_access import (
    SecurityAccessResponse,
)
from opendiag.uds.responses.tester_present import (
    TesterPresentResponse,
)


class ResponseRegistry:
    """
    Registry of UDS response classes.

    The registry associates each positive response SID with the
    response class responsible for interpreting that service.
    """

    def __init__(self) -> None:
        """
        Initialize the response registry with the supported UDS
        response types.
        """
        self._responses = {}

        # ECU Reset positive response: 0x11 + 0x40 = 0x51.
        self.register(
            0x51,
            ECUResetResponse,
        )

        # Diagnostic Session Control positive response: 0x10 + 0x40 = 0x50.
        self.register(
            0x50,
            DiagnosticSessionControlResponse,
        )

        # Read DTC Information positive response: 0x19 + 0x40 = 0x59.
        self.register(
            0x59,
            ReadDTCInformationResponse,
        )

        # Read Data By Identifier positive response: 0x22 + 0x40 = 0x62.
        self.register(
            0x62,
            ReadDataByIdentifierResponse,
        )

        # Security Access positive response: 0x27 + 0x40 = 0x67.
        self.register(
            0x67,
            SecurityAccessResponse,
        )

        # Tester Present positive response: 0x3E + 0x40 = 0x7E.
        self.register(
            0x7E,
            TesterPresentResponse,
        )

        # Negative response: 0x7F.
        self.register(
            0x7F,
            NegativeResponse,
        )

    def register(
        self,
        sid: int,
        response,
    ) -> None:
        """
        Associate a response SID with its response class.
        """
        self._responses[sid] = response

    def get(
        self,
        sid: int,
    ):
        """
        Return the response class registered for the given SID.
        """
        return self._responses[sid]

    def create(
        self,
        sid: int,
        **kwargs,
    ):
        """
        Create a response instance using the class registered for
        the given SID.
        """
        response_class = self.get(sid)

        return response_class(
            sid=sid,
            **kwargs,
        )
