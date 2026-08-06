# OpenDiag Decisions

## Arquitetura

✔ Layered Architecture

Application
↓
UDS
↓
Transport
↓
ISO-TP
↓
CAN

---

## Convenções

SID

Usaremos "sid" em vez de "service_id".

---

## UDSRequest

Permanece abstrata.

Será reavaliada após três serviços implementados.

---

## Sniffer

É independente da camada UDS.

Não conhece ISO-TP.

Não conhece Services.

Recebe apenas CAN Frames.

## Modelo para Serviços UDS Simples

O DiagnosticSessionControl torna-se o modelo oficial para serviços
compostos por:

- SID
- Subfunção
- Serialização simples

Novos serviços deverão seguir a mesma estrutura,
salvo justificativa arquitetural.

## Serviço de referência

DiagnosticSessionControl é o modelo oficial para serviços UDS simples.

Novos serviços deverão seguir a mesma estrutura:

- dataclass imutável
- SID como ClassVar
- serialização através da propriedade data
- testes de:
  - construção
  - serialização
  - constantes

  ## Architecture Checkpoint 01

Após a implementação dos serviços:

- DiagnosticSessionControl
- ECUReset

A arquitetura foi revisada.

Nenhuma refatoração foi considerada necessária.

A estrutura atual permanece válida.

A criação de uma pasta `types/` será reavaliada quando houver pelo menos seis tipos de domínio.

### DEC-003 — ReadDataByIdentifier

O serviço `ReadDataByIdentifier` receberá um `did: int`.

Sua responsabilidade limita-se à construção da requisição UDS.

A interpretação dos dados retornados será responsabilidade de uma camada de decodificação (`decoder`), independente do serviço UDS.

Essa separação permite suporte a DIDs padronizados e proprietários sem aumentar a complexidade da camada de transporte.

## DEC-004 — Unidade arquitetural

A unidade fundamental do OpenDiag é a mensagem UDS.

Um mesmo SID pode possuir múltiplas mensagens distintas.

Cada mensagem será representada por uma classe própria.

Exemplo:

SecurityAccess

- RequestSeed
- SendKey
