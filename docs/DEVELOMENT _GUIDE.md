# OpenDiag Development Guide

## Filosofia

- Evoluir antes de reescrever.
- Implementar o menor incremento possível.
- Uma Task = um objetivo.
- Um Commit = uma mudança coesa.

---

## Fluxo de desenvolvimento

1. Revisar a implementação existente.
2. Revisar os testes existentes.
3. Identificar o comportamento faltante.
4. Escrever o teste.
5. Executar o teste.
6. Implementar apenas o necessário.
7. Executar:

   - pytest
   - ruff check
   - ruff format

8. Revisão de código.
9. Commit.

---

## Testes

Todo teste deve seguir o padrão:

Arrange

Act

Assert

Exemplo:

```python
def test_example() -> None:
    # Arrange
    ...

    # Act
    ...

    # Assert
    ...
