# AutoDiag Architecture

## Objetivo

O AutoDiag é uma plataforma de diagnóstico automotivo desenvolvida em Python, focada em:

- Diagnóstico UDS
- ISO-TP
- CAN
- Engenharia reversa
- Testes em bancada
- Integração com ESP32
- Integração com CANable

---

# Arquitetura

GUI

↓

Application

↓

Services

↓

Protocol

↓

Transport

↓

Hardware

---

# Camadas

## Hardware

Responsável pela comunicação física.

Exemplos:

- CANable
- ESP32
- SocketCAN
- J2534

---

## Transport

Responsável pelo transporte.

Exemplo:

- ISO-TP

---

## Protocol

Responsável pelos protocolos.

Exemplo:

- UDS
- KWP2000

---

## Services

Implementa os serviços UDS.

Exemplo:

- Session
- DID
- DTC
- Security
- Routine

---

## Application

Lógica da aplicação.

Exemplo:

- Detectar ECU
- Ler VIN
- Ler DTC

---

## GUI

Interface gráfica.

---

# Regras

1. Nunca usar print() dentro da biblioteca.

2. Toda função pública retorna um objeto Response.

3. Nunca retornar None.

4. Toda classe possui uma única responsabilidade.

5. Todo módulo possui testes.

6. Toda alteração passa por revisão.

---

# Objetivo Final

Construir uma plataforma profissional para diagnóstico automotivo e engenharia reversa.