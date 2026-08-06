# ADR-001 — Session Discovery

**Status:** Accepted

**Milestone:** v0.4.0-dev

## Contexto

O ISOTPTransport necessita conhecer os IDs CAN (TX/RX) para transmitir e
receber mensagens.

Existiam três alternativas:

1. IDs fixos no ISOTPTransport.
2. Descoberta automática dentro do ISOTPTransport.
3. Descoberta realizada pelo Sniffer.

## Decisão

A descoberta dos parâmetros da rede será responsabilidade exclusiva do
Sniffer.

O ISOTPTransport receberá uma Session já configurada.

## Arquitetura

Sniffer
    │
    ▼
Session
    │
    ▼
ISOTPTransport
    │
    ▼
CANFrame
    │
    ▼
CANBus

## Benefícios

- Baixo acoplamento.
- Single Responsibility Principle.
- Facilita testes unitários.
- Compatível com múltiplas ECUs.
- Compatível com CAN FD.
- Compatível com 11 e 29 bits.
- Facilita futura implementação do OpenDiag.auto().

## Consequências

O ISOTPTransport deixa de possuir qualquer lógica de descoberta.

Toda a inteligência da rede fica concentrada no Sniffer.
