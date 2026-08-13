from time import monotonic

from opendiag.uds.request import UDSRequest
from opendiag.uds.reset import ResetType
from opendiag.uds.security import SecurityLevel
from opendiag.uds.services.diagnostic_session_control import (
    DiagnosticSessionControl,
)
from opendiag.uds.services.ecu_reset import ECUReset
from opendiag.uds.services.read_data_by_identifier import (
    ReadDataByIdentifier,
)
from opendiag.uds.services.read_dtc_information import (
    ReadDTCInformation,
)
from opendiag.uds.services.security_access import SecurityAccess
from opendiag.uds.services.tester_present import TesterPresent
from opendiag.uds.session import SessionType


class UDSClient:
    """
    Coordinates the UDS request/response workflow.

    Responsibilities:
    - send serialized requests through the transport;
    - receive raw responses;
    - delegate response parsing to the parser;
    - return the parsed response;
    - preserve responses that arrive out of order.
    """

    def __init__(
        self,
        *,
        transport=None,
        scanner=None,
        parser,
        did_resolver=None,
        did_decoder=None,
    ) -> None:

        self._transport = transport
        self._scanner = scanner
        self._parser = parser
        self._did_resolver = did_resolver
        self._did_decoder = did_decoder

        # ----------------------------------------------------
        # Respostas UDS recebidas fora da ordem esperada.
        #
        # Exemplo:
        #
        # solicitamos 0x1204
        # recebemos 0x1205
        #
        # A resposta 0x1205 fica armazenada aqui.
        # ----------------------------------------------------

        self._pending_did_responses = {}

    # ========================================================
    # READ DATA BY IDENTIFIER
    # ========================================================

    def read_data_by_identifier(
        self,
        did: int,
        timeout: float = 2.0,
    ):
        """
        Read a DID using UDS service 0x22.

        Responses containing another DID are preserved instead
        of being incorrectly associated with the current request.
        """

        # ----------------------------------------------------
        # 1. Verifica se já temos uma resposta desse DID
        #    aguardando.
        # ----------------------------------------------------

        pending = self._pending_did_responses.pop(
            did,
            None,
        )

        if pending is not None:
            return pending

        # ----------------------------------------------------
        # 2. Cria a requisição.
        # ----------------------------------------------------

        request = ReadDataByIdentifier(
            did=did,
        )

        # ----------------------------------------------------
        # 3. Envia somente uma vez.
        # ----------------------------------------------------

        if self._scanner is not None:
            response = self._scanner.request(
                request.data,
            )

            parsed = self._parser.parse(response.data)

            # Scanner normalmente já controla a associação.
            if hasattr(parsed, "did") and parsed.did != did:
                self._pending_did_responses[parsed.did] = parsed

                raise TimeoutError(
                    "Unexpected DID response: "
                    f"requested 0x{did:04X}, "
                    f"received 0x{parsed.did:04X}"
                )

            return parsed

        self._transport.send(request.data)

        # ----------------------------------------------------
        # 4. Timeout total da operação.
        # ----------------------------------------------------

        deadline = monotonic() + timeout

        while True:
            remaining = deadline - monotonic()

            if remaining <= 0:
                raise TimeoutError(f"Timeout waiting for DID 0x{did:04X}")

            # ------------------------------------------------
            # 5. Recebe uma mensagem ISO-TP completa.
            # ------------------------------------------------

            raw_response = self._transport.receive(timeout=remaining)

            # ------------------------------------------------
            # 6. Faz o parsing UDS.
            # ------------------------------------------------

            parsed = self._parser.parse(raw_response)

            # ------------------------------------------------
            # 7. Resposta de DID.
            # ------------------------------------------------

            if hasattr(parsed, "did"):
                received_did = parsed.did

                # --------------------------------------------
                # Resposta correta.
                # --------------------------------------------

                if received_did == did:
                    return parsed

                # --------------------------------------------
                # Resposta pertence a outro DID.
                #
                # NÃO descartamos.
                # --------------------------------------------

                self._pending_did_responses[received_did] = parsed

                print(
                    "[UDS] Resposta fora de ordem: "
                    f"solicitado=0x{did:04X} "
                    f"recebido=0x{received_did:04X}"
                )

                continue

            # ------------------------------------------------
            # Se não for uma resposta DID, devolve normalmente.
            # ------------------------------------------------

            return parsed

    # ========================================================
    # READ DID + DECODER
    # ========================================================

    def read_did(
        self,
        did: int,
    ):
        """Read and decode a diagnostic data identifier."""

        response = self.read_data_by_identifier(
            did,
        )

        if self._did_resolver is None:
            raise ValueError("DID resolver is not configured")

        if self._did_decoder is None:
            raise ValueError("DID decoder is not configured")

        definition = self._did_resolver.resolve(response.did)

        if definition is None:
            raise ValueError(f"Unknown DID: 0x{did:04X}")

        return self._did_decoder.decode(
            definition,
            response.value,
        )

    # ========================================================
    # VIN
    # ========================================================

    def read_vin(self) -> str:
        """Read the vehicle VIN using UDS DID F190."""

        response = self.read_data_by_identifier(0xF190)

        definition = self._did_resolver.resolve(response.did)

        if definition is None:
            raise ValueError(f"Unknown DID: 0x{response.did:04X}")

        value = self._did_decoder.decode(
            definition,
            response.value,
        )

        return value

    # ========================================================
    # GENERIC SEND
    # ========================================================

    def send(
        self,
        request: UDSRequest,
        timeout: float = 2.0,
    ):
        """
        Send a generic UDS request and wait for the response.
        """

        if self._scanner is not None:
            response = self._scanner.request(
                request.data,
            )

            return self._parser.parse(response.data)

        self._transport.send(request.data)

        response = self._transport.receive(timeout=timeout)

        return self._parser.parse(response)

    # ========================================================
    # DTC
    # ========================================================

    def read_dtc_information(
        self,
        subfunction: int = 0x02,
        status_mask: int = 0xFF,
    ):
        """Read diagnostic trouble code information."""

        return self.send(
            ReadDTCInformation(
                subfunction=subfunction,
                status_mask=status_mask,
            )
        )

    # ========================================================
    # TESTER PRESENT
    # ========================================================

    def tester_present(
        self,
    ):
        """Send Tester Present request."""

        return self.send(
            TesterPresent(),
        )

    # ========================================================
    # DIAGNOSTIC SESSION
    # ========================================================

    def diagnostic_session_control(
        self,
        session_type: SessionType = SessionType.DEFAULT,
    ):
        """Change the ECU diagnostic session."""

        return self.send(
            DiagnosticSessionControl(
                session_type=session_type,
            )
        )

    # ========================================================
    # ECU RESET
    # ========================================================

    def ecu_reset(
        self,
        reset_type: ResetType = ResetType.HARD,
    ):
        """Send ECU Reset request."""

        return self.send(
            ECUReset(
                reset_type=reset_type,
            )
        )

    # ========================================================
    # SECURITY ACCESS
    # ========================================================

    def security_access(
        self,
        level: SecurityLevel,
        key: bytes = b"",
    ):
        """Send Security Access request."""

        return self.send(
            SecurityAccess(
                level=level,
                key=key,
            )
        )
