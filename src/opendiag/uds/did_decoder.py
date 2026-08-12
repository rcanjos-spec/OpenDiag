from opendiag.uds.did_resolver import DIDDefinition


class DIDDecoder:
    """Decode raw values according to a DID definition."""

    def decode(
        self,
        definition: DIDDefinition,
        data: bytes,
    ):
        if len(data) != definition.length:
            raise ValueError(f"Expected {definition.length} bytes, got {len(data)}")

        if definition.type == "ascii":
            try:
                return data.decode("ascii")
            except UnicodeDecodeError as exc:
                raise ValueError("DID value must contain ASCII characters") from exc

        if definition.type == "uint8":
            return int.from_bytes(data, "big")

        if definition.type == "uint16":
            return int.from_bytes(data, "big")

        if definition.type == "uint32":
            return int.from_bytes(data, "big")

        raise ValueError(f"Unsupported DID type: {definition.type}")
