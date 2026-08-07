## OpenDiag

OpenDiag is an open-source Python library for automotive diagnostics based on
ISO 14229 (UDS).

## Current Status

### Milestone v0.2.0-dev

Implemented:

- UDS Client
- Request/Response model
- Positive and Negative Responses
- Response Parser
- Response Registry
- Service Registry
- Default Response Registration

### Supported UDS Services

| Service | SID | Status |
|---------|----:|:------:|
| Diagnostic Session Control | 0x10 | ✅ |
| ECU Reset | 0x11 | ✅ |
| Read Data By Identifier | 0x22 | ✅ |
| Security Access | 0x27 | ✅ |
| Routine Control | 0x31 | ✅ |
| Tester Present | 0x3E | ✅ |

### Implemented Positive Responses

| Response | SID |
|----------|----:|
| DiagnosticSessionControlResponse | 0x50 |
| ECUResetResponse | 0x51 |
| ReadDataByIdentifierResponse | 0x62 |
| SecurityAccessResponse | 0x67 |
| RoutineControlResponse | 0x71 |
| TesterPresentResponse | 0x7E |

## Architecture

```
Application
      │
      ▼
 UDSClient
      │
      ▼
 UDSResponseParser
      │
      ▼
 ResponseRegistry
      ▲
      │
register_default_responses()
      │
      ▼
Response Classes
```

## Example

```python
from opendiag.uds.client import UDSClient
from opendiag.uds.defaults import register_default_responses
from opendiag.uds.response_parser import UDSResponseParser
from opendiag.uds.response_registry import ResponseRegistry

registry = ResponseRegistry()
register_default_responses(registry)

parser = UDSResponseParser(registry)

client = UDSClient(
    transport=transport,
    parser=parser,
)

response = client.send(
    ReadDataByIdentifier(
        did=0xF190,
    )
)
```

## Quality

Current quality status:

- ✅ 82 automated tests
- ✅ Ruff compliant
- ✅ Fully formatted
- ✅ Type annotated
- ✅ Test-driven development

## Next Milestone

### v0.3.0-dev

Planned features:

- ISO-TP Transport
- CAN Transport
- Mock Transport improvements
- Multi-frame support
- Real ECU communication

## Status

### Milestone M1 (Concluído)

- ✔ CAN Frame
- ✔ Python CAN Bus
- ✔ ISO-TP
- ✔ UDS Client
- ✔ Tester Present
- ✔ 106 testes automatizados
- ✔ Ruff Check
- ✔ Ruff Format

Próximo objetivo:

- Comunicação com ECU Magneti Marelli IAW 10GF
