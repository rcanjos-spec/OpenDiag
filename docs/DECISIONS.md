# Decisions

## 2026-08-07

### SecurityAccess

Mantida a arquitetura de uma classe por serviço.

SecurityAccess substitui a abordagem anterior com RequestSeed e SendKey.

---

### Hardware

ISOTPTransport continuará sendo apenas um orquestrador.

Toda a lógica ISO-TP permanecerá em:

- ISOTPFrame
- ISOTPReassembler

receive() será implementado respeitando essa arquitetura.
