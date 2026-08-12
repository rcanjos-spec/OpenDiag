# KACTOENG — Estado e Histórico do Projeto

> Documento de referência do estado atual do projeto. Preserva de onde o projeto partiu, o que já foi construído e exatamente onde estamos agora.

## 1. Origem

O projeto começou como **OpenDiag**, com a ideia de construir uma ferramenta própria de diagnóstico automotivo. A estratégia foi construir primeiro o núcleo técnico, em camadas, antes de uma interface completa.

Evolução:

```text
CAN
 ↓
ISO-TP
 ↓
UDS
 ↓
Serviços UDS
 ↓
Parser de respostas
 ↓
DIDs
 ↓
Diagnóstico de alto nível
```

O nome de trabalho atual é **KACTOENG**.

## 2. Objetivo

Construir uma ferramenta própria de diagnóstico automotivo capaz de:

- comunicar-se com ECUs;
- trabalhar com CAN;
- transportar mensagens através de ISO-TP;
- executar serviços UDS;
- interpretar respostas;
- identificar e decodificar DIDs;
- trabalhar com DTCs;
- evoluir posteriormente para sessões, Security Access, rotinas e outras funções de diagnóstico.

O desenvolvimento é incremental, mantendo testes automatizados passando antes de avançar.

## 3. Arquitetura atual

```text
                 KACTOENG
                    │
                    ▼
                UDSClient
                    │
          ┌─────────┴─────────┐
          │                   │
     UDS Requests        UDS Responses
          │                   │
          ▼                   ▼
      ISO-TP Transport ── Response Parser
          │                   │
          ▼                   ▼
          CAN              DID Layer
                              │
                    ┌─────────┴─────────┐
                    │                   │
               DIDResolver         DIDDecoder
                    │                   │
                    └─────────┬─────────┘
                              ▼
                         Valor interpretado
```

## 4. CAN

A comunicação CAN é uma das bases do projeto.

Existe uma abstração de `CANFrame` e transporte baseado em `python-can`.

Já foram utilizados scripts físicos com:

- interface SLCAN;
- COM6;
- 500000 bit/s;
- CAN IDs estendidos.

## 5. ISO-TP

A camada ISO-TP já foi construída e testada.

Componentes:

```text
src/opendiag/protocols/isotp.py
src/opendiag/protocols/isotp_transport.py
```

Contempla:

- Single Frame;
- First Frame;
- Consecutive Frame;
- Flow Control;
- segmentação;
- reassembly;
- sequence number;
- timeout;
- CAN extended IDs;
- envio de Flow Control após First Frame.

Arquitetura:

```text
Aplicação
   ↓
ISOTPTransport
   ↓
ISOTPSegmenter
   ↓
ISOTPFrame
   ↓
CANFrame
   ↓
CAN Bus
```

Recepção:

```text
CAN Bus
   ↓
CANFrame
   ↓
ISOTPFrame
   ↓
ISOTPReassembler
   ↓
ISOTPTransport
   ↓
bytes UDS
```

**Não devemos recriar essa camada sem necessidade.**

## 6. UDS

O projeto evoluiu para UDS após a fundação CAN/ISO-TP.

O `UDSClient` coordena construção de requisições, envio, recepção e parsing.

Serviços já trabalhados:

- Tester Present — `0x3E`;
- Diagnostic Session Control — `0x10`;
- ECU Reset — `0x11`;
- Security Access — `0x27`;
- Read Data By Identifier — `0x22`;
- Read DTC Information — `0x19`.

Fluxo:

```text
UDSClient
   ↓
UDSRequest
   ↓
ISOTPTransport
   ↓
CAN
```

e:

```text
CAN
 ↓
ISOTPTransport
 ↓
UDSResponseParser
 ↓
UDSResponse
 ↓
UDSClient
```

## 7. Parser e Registry

Existem:

```text
UDSResponseParser
ResponseRegistry
```

A separação é:

```text
transporte
   ≠
protocolo
   ≠
interpretação
```

## 8. DIDs — etapa construída recentemente

**IMPORTANTE: a camada de DIDs foi construída recentemente e essa etapa já está concluída no estágio atual.**

Não devemos voltar a tratá-la como tarefa futura.

Foram criados:

```text
DIDDefinition
DIDResolver
DIDDecoder
```

e o banco:

```text
data/dids/generic.json
```

Exemplo:

```json
{
  "F190": {
    "name": "VIN",
    "type": "ascii",
    "length": 17
  }
}
```

## 9. DIDDefinition

Representa a definição de um identificador:

```text
DID
 ├── name
 ├── type
 └── length
```

Exemplo:

```text
F190
 ├── name: VIN
 ├── type: ascii
 └── length: 17
```

## 10. DIDResolver

O `DIDResolver` carrega o banco JSON e resolve um DID numérico para sua definição:

```text
0xF190
   ↓
"F190"
   ↓
DIDDefinition
   ↓
VIN / ascii / 17
```

## 11. DIDDecoder

O `DIDDecoder` recebe:

```text
DIDDefinition
+
bytes
```

e devolve o valor interpretado.

Tipos implementados:

```text
ascii
uint8
uint16
uint32
```

Para ASCII existem validações de comprimento e conteúdo ASCII.

## 12. VIN / DID F190

O primeiro DID concreto foi:

```text
F190 = VIN
```

com:

```text
type = ascii
length = 17
```

O cliente possui:

```text
read_vin()
```

Fluxo:

```text
UDS 0x22
   ↓
DID F190
   ↓
UDS Response
   ↓
DIDResolver
   ↓
DIDDecoder
   ↓
VIN
```

VIN usado nos testes:

```text
1HGCM82633A004352
```

## 13. Testes dos DIDs

Foram adicionados testes para:

```text
ASCII
uint8
uint16
uint32
```

Também existe teste de integração do resolver com o decoder para o VIN.

## 14. Problemas encontrados e resolvidos

Durante a integração dos DIDs com `UDSClient`, surgiram erros como:

```text
AttributeError: 'UDSClient' object has no attribute 'read_did'
```

e:

```text
AttributeError: 'NoneType' object has no attribute 'resolve'
```

Isso ocorreu porque o `UDSClient` passou a depender de `DIDResolver` e `DIDDecoder`, enquanto alguns testes antigos ainda criavam o cliente sem essas dependências.

Os testes foram ajustados e a arquitetura foi consolidada.

## 15. Estado dos testes

No ponto registrado:

```text
231 passed
```

Também:

```text
ruff check
All checks passed!
```

e:

```text
ruff format --check
161 files already formatted
```

## 16. Scripts físicos existentes

Pasta:

```text
scripts/hardware/
```

Arquivos relevantes:

```text
02_tester_present.py
04_can_scan.py
05_can_analyzer.py
06_can_counter_probe.py
07_uds_vin.py
09_uds_22_physical.py
09_uds_22_physical.txt
12_uds_timeout.py
16_uds_dtc_architecture.py
17_uds_vin_architecture.py
hardware_test.py
test_can_send.py
```

## 17. Script 07 — UDS VIN

Existe:

```text
scripts/hardware/07_uds_vin.py
```

Fluxo:

```text
PythonCANBus
    ↓
ISOTPTransport
    ↓
OBDClient
    ↓
read_vin()
```

Configuração utilizada:

```text
interface = slcan
channel = COM6
bitrate = 500000
TX = 18DB33F1
RX = 18DAF110
```

## 18. Script 09 — UDS 0x22 físico

Existe:

```text
scripts/hardware/09_uds_22_physical.py
```

Demonstra diretamente:

```text
22 F1 90
```

com:

```text
TX ID = 18DA10F1
RX ID = 18DAF110
FLOW CONTROL ID = 18DA10F1
```

Envia:

```text
03 22 F1 90 00 00 00 00
```

Quando recebe First Frame ISO-TP, envia:

```text
30 00 00 00 00 00 00 00
```

Esse script demonstra a comunicação física UDS 0x22 e o tratamento do First Frame/Flow Control.

## 19. Script 17 — arquitetura UDS

Existe:

```text
scripts/hardware/17_uds_vin_architecture.py
```

Representa a evolução:

```text
PythonCANBus
      ↓
ISOTPTransport
      ↓
UDSClient
      ↓
UDSResponseParser
      ↓
read_vin()
```

Esse é um dos pontos importantes do estado atual.

O objetivo é fazer a arquitetura nova utilizar corretamente também:

```text
DIDResolver
DIDDecoder
```

para que a leitura física do VIN percorra a cadeia completa.

## 20. Onde o projeto está agora

O projeto está neste estágio:

```text
                 KACTOENG
                    │
                    ▼
                UDSClient
                    │
                    ▼
             ReadDataByIdentifier
                    │
                    ▼
             ISOTPTransport
                    │
                    ▼
                   CAN
                    │
                    ▼
                  ECU
                    │
                    ▼
             resposta UDS
                    │
                    ▼
             ResponseParser
                    │
                    ▼
               DIDResolver
                    │
                    ▼
               DIDDecoder
                    │
                    ▼
               VIN
```

A fundação CAN/ISO-TP já existe.

O núcleo UDS já existe.

A camada DID já foi construída recentemente.

O banco inicial de DIDs já existe.

Os testes automatizados já cobrem essas camadas.

## 21. Próxima fronteira

A próxima etapa é **validar a arquitetura completa na comunicação física já existente**, sem recriar componentes.

Objetivo:

```text
CAN físico
   ↓
ISOTPTransport
   ↓
UDSClient
   ↓
ReadDataByIdentifier
   ↓
UDSResponseParser
   ↓
DIDResolver
   ↓
DIDDecoder
   ↓
VIN
```

Isso deve aproveitar os scripts existentes.

**Não criar uma ECU simulada em Python para substituir uma infraestrutura que já existe.**

**Não recriar ISO-TP.**

**Não recriar CAN.**

**Não recriar os DIDs.**

## 22. O que já está concluído

- [x] CAN
- [x] CANFrame
- [x] ISO-TP Frame
- [x] ISO-TP Segmenter
- [x] ISO-TP Reassembler
- [x] ISO-TP Transport
- [x] Flow Control
- [x] UDS Request
- [x] UDS Response Parser
- [x] Response Registry
- [x] UDSClient
- [x] Tester Present
- [x] Diagnostic Session Control
- [x] ECU Reset
- [x] Security Access
- [x] Read Data By Identifier
- [x] Read DTC Information
- [x] DIDDefinition
- [x] DIDResolver
- [x] DIDDecoder
- [x] banco JSON de DIDs
- [x] F190 / VIN
- [x] ASCII
- [x] uint8
- [x] uint16
- [x] uint32
- [x] testes unitários e de integração das etapas desenvolvidas

## 23. Próximo objetivo imediato

Validar a cadeia completa:

```text
PythonCANBus
      ↓
ISOTPTransport
      ↓
UDSClient
      ↓
UDS 0x22 F190
      ↓
ECU
      ↓
ISO-TP response
      ↓
UDSResponseParser
      ↓
DIDResolver
      ↓
DIDDecoder
      ↓
VIN
```

Depois dessa validação, avançar para a expansão organizada dos serviços e dos DIDs.

## 24. Regra de continuidade

Antes de implementar algo novo, responder:

1. Isso já existe?
2. Qual camada é responsável?
3. Existe teste?
4. Existe script físico relacionado?
5. Estamos corrigindo algo existente ou criando uma nova capacidade?
6. Qual é o próximo passo definido no estado do projeto?

A prioridade é **evoluir o que já existe**, não duplicar componentes.

## 25. Resumo executivo

O KACTOENG começou como OpenDiag e evoluiu de uma ideia de ferramenta de diagnóstico para um núcleo técnico estruturado.

Hoje já possui:

```text
CAN
 ↓
ISO-TP
 ↓
UDS
 ↓
UDSClient
 ↓
Response Parser
 ↓
DID Resolver
 ↓
DID Decoder
```

Com:

```text
231 testes passando
Ruff OK
Formatação OK
```

A camada de **DIDs foi construída recentemente e está concluída no estágio atual**, incluindo F190/VIN e os tipos implementados.

O projeto agora está na transição entre:

> **construir as camadas internas**

e:

> **validar a arquitetura completa usando a comunicação física já existente.**

Este documento deve ser atualizado ao final de cada etapa relevante para manter um ponto de referência único do projeto.
