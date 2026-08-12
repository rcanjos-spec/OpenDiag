from opendiag.uds.did_resolver import DIDDefinition


class DIDDecoder:
    """Decode raw values according to a DID definition."""

    def decode(
        self,
        definition: DIDDefinition,
        data: bytes,
    ):
        if definition.type == "ascii":
            if len(data) != definition.length:
                raise ValueError(f"Expected {definition.length} bytes, got {len(data)}")

            try:
                return data.decode("ascii")
            except UnicodeDecodeError as exc:
                raise ValueError("DID value must contain ASCII characters") from exc

        raise ValueError(f"Unsupported DID type: {definition.type}")
