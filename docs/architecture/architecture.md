# OpenDiag Architecture Principles

## Purpose

This document defines the architectural principles that guide the OpenDiag project.

These principles should be followed by all contributors when designing, implementing, and reviewing code.

---

# 1. Layered Architecture

The project is organized into independent layers.

Each layer depends only on the layer immediately below it.

Application
↓
UDS
↓
Transport
↓
ISO-TP
↓
CAN
↓
Hardware

---

# 2. Single Responsibility Principle

Each class should have one well-defined responsibility.

Classes should be small, cohesive, and easy to test.

---

# 3. Dependency Inversion

High-level modules must depend on abstractions rather than concrete implementations.

Example:

UDSClient
↓

Transport

instead of

UDSClient
↓

CANBus

---

# 4. Test-Driven Development

New features should begin with a failing test.

Implementation should be the minimum required to make the test pass.

Refactoring comes only after all tests are green.

---

# 5. Public API Stability

Public APIs should be designed before implementation.

Breaking changes should be avoided whenever possible.

---

# 6. Low Coupling

Components should communicate through abstractions.

Direct dependencies between unrelated modules should be avoided.

---

# 7. Conventional Commits

All commits must follow the Conventional Commits specification.

Examples:

feat:
fix:
refactor:
docs:
test:
chore:

---

# 8. Incremental Development

Large features should be implemented through small, verifiable steps.

Every step should keep the project in a working state.

---

# 9. Architecture Before Code

Architectural decisions should be discussed and documented before implementation.

Important decisions must be recorded as ADRs.

---

# 10. Code Review

Every change should answer four questions:

- Is the architecture improved?
- Is the code simpler?
- Is it fully tested?
- Is the public API preserved?

# 11. Small Changes

Changes should be as small as possible.

Whenever practical:

- modify one behavior at a time;
- execute the full test suite;
- continue only after all tests pass.

Small changes reduce risk and simplify debugging.

# 12. Architecture First

Before implementing a new feature:

1. Define the problem.
2. Review the architecture.
3. Design the public API.
4. Write the tests.
5. Implement the feature.
6. Refactor.
7. Document the decision if necessary.
