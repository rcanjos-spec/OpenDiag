# Daily Log — 2026-08-07

## Sprint 49 — Concluída

### Implementações

- SecurityLevel
- SecurityAccess (Request)
- SecurityAccessResponse
- from_bytes()
- ResponseRegistry
- UDSResponseParser
- UDSClient.security_access()

### Validação

- 139 testes passando
- Ruff Check: OK
- Ruff Format: OK

---

## Hardware

Validação realizada com sucesso:

- USB-CAN (CANable)
- python-can
- Interface slcan
- COM6
- PythonCANBus
- ISOTPTransport.send()

### Descoberta

Durante o primeiro teste em hardware real foi identificado que o
ISOTPTransport ainda não implementa o método receive().

Os testes automatizados não detectaram essa ausência devido ao uso de
MockTransport.

Foi decidido manter a arquitetura e implementar o receive() apenas como
orquestrador entre CANBus, ISOTPFrame e ISOTPReassembler.

---

## Decisão

Sprint 50 será dedicada à integração com hardware.

Objetivos:

- Revisar ISOTPFrame
- Revisar ISOTPReassembler
- Implementar ISOTPTransport.receive()
- Testes unitários
- Testes com MockBus
- Primeiro TesterPresent em ECU real

---

## Status

Projeto em estado GREEN.

139 testes.
Arquitetura preservada.
Pronto para a Sprint 50.

## 08/08/2026 — First Real CAN ID Discovery

### Marco

Primeira varredura CAN real executada pelo OpenDiag através da interface SLCAN em `COM6`, com bitrate de `500000`.

### Resultado

O `DiagnosticScanner` realizou uma varredura passiva de 10 segundos e identificou **17 IDs CAN distintos**, sem transmitir qualquer frame.

|           ID | Frames | Frequência aprox. |
| -----------: | -----: | ----------------: |
|      `0x0F4` |   1001 |            100 Hz |
|      `0x0FB` |   1001 |            100 Hz |
|      `0x0FC` |   1001 |            100 Hz |
|      `0x0FF` |   1001 |            100 Hz |
|      `0x100` |   1001 |            100 Hz |
|      `0x1F0` |    501 |             50 Hz |
|      `0x1F4` |    501 |             50 Hz |
|      `0x2ED` |    201 |             20 Hz |
|      `0x2EF` |    201 |             20 Hz |
|      `0x412` |    101 |             10 Hz |
|      `0x417` |    101 |             10 Hz |
|      `0x41B` |    101 |             10 Hz |
|      `0x736` |    101 |             10 Hz |
|      `0x226` |     11 |             ~1 Hz |
|      `0x5A5` |     11 |             ~1 Hz |
|      `0x5AE` |     11 |             ~1 Hz |
| `0x1E360001` |     11 |             ~1 Hz |

### Observações técnicas

* O scanner demonstrou funcionamento correto em barramento CAN real.
* Foram observadas mensagens com periodicidades regulares de aproximadamente 100, 50, 20, 10 e 1 Hz.
* Foi identificado o ID `0x1E360001`, indicando a presença de **CAN Extended Frame (29 bits)**.
* Os IDs convencionais `0x7E0` e `0x7E8` não apareceram durante essa captura.
* Portanto, não devemos assumir IDs UDS padrão antes de analisar o barramento real.
* O resultado confirma a decisão arquitetural de realizar descoberta passiva da rede antes da implementação de diagnóstico ativo.

### Próximo passo

Implementar um monitor CAN capaz de registrar, para cada ID:

* arbitration ID;
* Standard/Extended;
* DLC;
* payload;
* timestamp;
* frequência de transmissão.

Objetivo: analisar o conteúdo das mensagens e identificar possíveis mensagens relacionadas ao diagnóstico e aos estados da ECU.

### Marco do projeto

O OpenDiag passou da fase de testes exclusivamente simulados para a **primeira interação funcional de descoberta com um barramento CAN automotivo real**.
