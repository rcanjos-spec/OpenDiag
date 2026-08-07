Daily Log – OpenDiag

Data: 06/08/2026
Sprint: M1 – Conclusão da Infraestrutura CAN / ISO-TP / UDS

Objetivo da sessão

Concluir a refatoração da pilha de comunicação, estabilizar a arquitetura e preparar o projeto para iniciar os testes em hardware com a ECU Magneti Marelli IAW 10GF.

Principais atividades realizadas

Camada ISO-TP

• Refatoração completa do ISOTPTransport.

• Integração definitiva entre ISOTPFrame e CANFrame.

• Implementação do método to_can_frame().

• Padronização da transmissão utilizando CANFrame.

• Padronização da recepção através de ISOTPFrame.from_can_frame().


Camada CAN

• Implementação completa do PythonCANBus (send/receive).

• Integração com python-can.

• Conversão CANFrame ⇄ can.Message.


Camada UDS

• Validação completa do fluxo:

TesterPresent → UDSClient → ISOTPTransport → PythonCANBus.

• Implementação do TesterPresent.

• Integração Request → Transport.

• Integração Response → Parser.

Refatorações realizadas

• Atualização dos contratos do ISOTPTransport.

• Atualização dos testes de integração.

• Atualização dos mocks.

• Remoção de dependências da API antiga.

• Remoção de código duplicado.

Problemas encontrados

• Incompatibilidade entre ISOTPFrame e CANFrame.

• Retorno inconsistente entre ISOTPMessage e bytes.

• Testes antigos utilizando object() em vez de CANFrame.

• Duplicação de testes (F811).

• Imports obsoletos.


Todos os problemas foram corrigidos.

Validação

• 106 testes passando.

• Ruff Check: All checks passed.

• Ruff Format executado com sucesso.

Arquitetura consolidada

UDS

 └── UDSClient

      └── ISOTPTransport

           └── ISOTPFrame

                └── CANFrame

                     └── PythonCANBus

                          └── python-can

                               └── USB-CAN

                                    └── ECU

Situação atual do projeto

Concluído:

• CANFrame

• PythonCANBus

• ISOTPFrame

• ISOTPSegmenter

• ISOTPReassembler

• ISOTPTransport

• UDSClient

• ResponseParser

• TesterPresent

• Testes unitários

• Testes de integração

• Refatoração completa

• Padronização do código

Próxima Sprint

Sprint 41


Primeiro objetivo:

examples/tester_present.py


Fluxo esperado:

PythonCANBus → ISOTPTransport → UDSClient → TesterPresent → Magneti Marelli IAW 10GF

Próximos serviços UDS

1. Tester Present (hardware)

2. Diagnostic Session Control

3. ReadDataByIdentifier

4. Read VIN

5. Read DTC

6. Clear DTC

7. Live Data

Lições aprendidas

• A arquitetura em camadas facilitou a refatoração.

• A suíte automatizada detectou regressões rapidamente.

• O uso de CANFrame simplificou a comunicação entre as camadas.

• O desenvolvimento orientado por testes (TDD) reduziu riscos.

Status do projeto

OpenDiag v0.4.0-alpha


A infraestrutura de comunicação CAN, ISO-TP e UDS foi concluída, estabilizada e validada por 106 testes automatizados. O projeto está pronto para iniciar a validação em bancada com a Magneti Marelli IAW 10GF.
