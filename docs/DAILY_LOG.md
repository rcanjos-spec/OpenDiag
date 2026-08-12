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

# Daily Log — OpenDiag

**Data:** 10/08/2026
**Projeto:** OpenDiag
**Branch:** `main`

## 1. Objetivo do dia

Evoluir o `CANTrafficAnalyzer` para identificar automaticamente estruturas de integridade presentes em frames CAN reais, especialmente:

* Contadores sequenciais;
* Contadores de 4 bits;
* Rollover;
* CRC-8/SAE-J1850;
* Separação entre campo de contador e campo de CRC;
* Análise dentro de `Payload States`.

## 2. Implementações realizadas

### Contador CAN

Foi aprimorada a detecção de contadores:

* Contador de 8 bits;
* Contador de 4 bits;
* `step = +1`;
* `modulus = 16` ou `256`;
* Detecção de rollover;
* Detecção de contador dentro de um `Payload State`.

### Integridade CAN

Foi implementada a detecção de:

**CRC-8/SAE-J1850**

Parâmetros identificados:

* Polynomial: `0x1D`
* Init: `0xFF`
* Xorout: `0xFF`
* Campo CRC identificado no byte 7;
* Dados protegidos: bytes `0–6`.

### Correção importante

O fluxo do analisador foi reorganizado para detectar a integridade antes do contador.

Assim:

```text
Frames
  ↓
Agrupamento por ID
  ↓
Detecção CRC
  ↓
Exclusão dos bytes de integridade
  ↓
Detecção de contador
  ↓
Análise de propriedades
  ↓
Análise por Payload State
```

Isso eliminou o falso positivo em que o byte 7, que contém o CRC, também era identificado como contador.

## 3. Testes automatizados

A suíte específica do analisador chegou a:

```text
22 passed
```

Foi acrescentado um teste de regressão para garantir a coexistência de:

```text
contador + CRC
```

no mesmo frame.

A suíte completa terminou com:

```text
178 passed in 1.92s
```

Qualidade:

```text
ruff check
All checks passed!

ruff format --check
145 files already formatted
```

## 4. Teste em hardware real

Foi executado o `05_can_analyzer.py` utilizando:

```text
Interface : COM6
Bitrate   : 500000
Duration  : 10 s
```

Resultado:

```text
Frames capturados: 6859
IDs encontrados:   17
```

Os principais IDs foram identificados com periodicidades coerentes:

* `0xF4` → ~100 Hz
* `0xFB` → ~100 Hz
* `0xFC` → ~100 Hz
* `0xFF` → ~100 Hz
* `0x100` → ~100 Hz
* `0x1F4` → ~50 Hz

No tráfego real, o analisador identificou corretamente:

```text
byte 6
bits 0-3
step +1
modulus 16
rollover YES
```

e:

```text
byte 7
CRC-8/SAE-J1850
protected bytes 0-6
matches 16/16
```

O resultado foi confirmado nos IDs `0xF4`, `0xFB`, `0xFC`, `0xFF`, `0x100` e `0x1F4`.

## 5. Git

Commit realizado:

```text
ee4d80e
feat: enhance CAN traffic integrity analysis
```

Pre-commit hooks:

```text
ruff                  Passed
ruff format           Passed
trim trailing whitespace  Passed
fix end of files      Passed
```

Push realizado com sucesso para:

```text
origin/main
```

Estado final:

```text
working tree clean
main sincronizado com origin/main
```

## 6. Estado ao final do dia

```text
TESTES       ✅ 178 passed
RUFF         ✅ All checks passed
FORMAT       ✅ 145 files already formatted
HARDWARE     ✅ CAN real validado
COMMIT       ✅ ee4d80e
PUSH         ✅ origin/main
WORKTREE     ✅ clean
```

## 7. Próximo passo

Não alterar o código validado hoje.

Retomar a partir do commit:

```text
ee4d80e
```

Próxima evolução planejada do `CANTrafficAnalyzer`:

**identificação automática dos bytes que provavelmente representam sinais/dados físicos**, separando-os de:

* contador;
* CRC;
* campos constantes;
* campos de estado.

A ideia é evoluir de uma análise estrutural do frame para uma primeira camada de **engenharia reversa automática dos sinais CAN**.

## Frase para retomada

> **“Hoje o OpenDiag deixou de apenas observar o tráfego CAN e passou a reconhecer parte da estrutura interna dos frames reais.”**

# OpenDiag — Daily Log

**Data:** 11/08/2026
**Projeto:** OpenDiag
**Branch:** `main`
**Status:** Checkpoint concluído — working tree clean

## 1. Objetivo do dia

Continuar a implementação e validação da camada **UDS sobre ISO-TP**, com foco na leitura de DTCs (`0x19`) utilizando hardware real através da interface CAN na COM6.

---

## 2. Atividades realizadas

### ISO-TP

Foi investigado e corrigido o comportamento de mensagens ISO-TP longas.

Validações realizadas:

* First Frame recebido corretamente.
* Flow Control `30 00 00` enviado corretamente.
* Consecutive Frames recebidos em sequência.
* Validação do rollover do Sequence Number:

  * `0x0E`
  * `0x0F`
  * `0x00`
  * `0x01`
* Reassembly de mensagens longas validado.
* Timeout de reassembly tornou-se configurável através de `reassembly_timeout`.

Foi criado teste específico para garantir o funcionamento do rollover `0x0F → 0x00`.

---

## 3. UDS — ReadDTCInformation

Foi implementado e validado o serviço:

```text
0x19 — ReadDTCInformation
```

com a subfunção:

```text
0x02 — reportDTCByStatusMask
```

e utilização da máscara:

```text
FF
```

A requisição utilizada no hardware foi:

```text
19 02 FF
```

A ECU respondeu com uma mensagem ISO-TP longa iniciada por:

```text
11 B3 59 02 CF ...
```

Foi identificado corretamente que:

```text
59 02 CF
```

contém:

* `59` — resposta positiva do serviço `0x19`
* `02` — subfunção
* `CF` — DTC Status Availability Mask

Os DTCs seguintes possuem o formato:

```text
DD DD DD SS
```

onde:

* `DD DD DD` = código DTC de 24 bits
* `SS` = status do DTC

O parser foi corrigido para considerar o byte `CF` antes dos registros de DTC.

---

## 4. Validação em hardware real

Foi executado o script:

```text
scripts/hardware/13_uds_dtc.py
```

Interface utilizada:

```text
COM6
Bitrate: 500000
```

IDs:

```text
TX ID: 18DA10F1
RX ID: 18DAF110
FC ID: 18DA10F1
```

Resultado:

```text
DTCs encontrados: 108
```

O OpenDiag conseguiu completar o ciclo:

```text
UDS Request
    ↓
CAN
    ↓
ISO-TP First Frame
    ↓
Flow Control
    ↓
Consecutive Frames
    ↓
ISO-TP Reassembly
    ↓
UDS Parser
    ↓
UDSDTC[]
```

### Resultado principal

**108 DTCs reais foram lidos da ECU e convertidos para objetos estruturados pelo OpenDiag.**

Primeiros registros obtidos:

```text
DTC=0x010700 STATUS=0x0F
DTC=0x013000 STATUS=0x40
DTC=0x011800 STATUS=0x0E
DTC=0x056200 STATUS=0x40
DTC=0x056300 STATUS=0x40
```

---

## 5. Testes automatizados

Resultado final da suíte:

```text
216 passed in 2.42s
```

Qualidade de código:

```text
ruff check
All checks passed!
```

Formatação:

```text
ruff format --check
157 files already formatted
```

---

## 6. Git

Alterações consolidadas e commitadas.

Estado final:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Checkpoint do projeto concluído com sucesso.

---

## 7. Conquistas do dia

Hoje o OpenDiag passou por uma validação importante:

> **Não estamos mais apenas simulando UDS/ISO-TP em testes unitários. O OpenDiag conseguiu conversar com uma ECU real, transportar uma resposta ISO-TP de grande porte e interpretar 108 DTCs reais.**

Isso representa a validação integrada das camadas:

```text
CAN
 ↓
ISO-TP
 ↓
UDS
 ↓
ECU REAL
```

---

## 8. Próximos passos

Para a próxima etapa:

1. Melhorar a estrutura `UDSDTC`.
2. Preservar o `DTC Status Availability Mask` na resposta.
3. Criar interpretação dos bits de status do DTC.
4. Separar claramente:

   * código bruto;
   * status bruto;
   * interpretação do status.
5. Melhorar a apresentação dos DTCs para o usuário.
6. Depois avançar para novos serviços UDS.

**Importante:** não alterar novamente a camada ISO-TP sem necessidade. A comunicação física e o reassembly já foram validados com sucesso.

---

## Frase do dia

> **Hoje o OpenDiag deixou de apenas testar protocolos e começou a diagnosticar uma ECU de verdade.**
