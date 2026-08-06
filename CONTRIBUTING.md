# Phase 2 — Protocol Engineering

Until now, our focus has been **Software Engineering**.

From this point forward, we will also focus on **Protocol Engineering**.

These are complementary disciplines, and both are essential to the success of the OpenDiag project.

---

# Development Workflow

Every UDS service will follow the development process below.

                Protocol Review
                       │
                       ▼
              ISO 14229 Analysis
                       │
                       ▼
               Public API Design
                       │
                       ▼
              Architecture Review
                       │
                       ▼
                       TDD
                       │
                       ▼
                Implementation
                       │
                       ▼
                  Refactoring
                       │
                       ▼
                  Documentation

No protocol feature should be implemented before completing this workflow.

---

# ADR-011 — Protocol-First Development

**Status:** Accepted

## Context

OpenDiag implements standardized automotive diagnostic protocols.

Protocol correctness is just as important as software architecture.

## Decision

Every protocol feature must begin with a protocol review before implementation.

## Consequences

### Positive

- Better compliance with ISO standards.
- Improved maintainability.
- Clear separation between protocol design and software implementation.
- Higher quality documentation.
- Easier onboarding for new contributors.

### Negative

- Slightly more planning before implementation.

---

# Documentation Structure

The documentation is organized into independent sections.

docs/
│
├── adr/
├── architecture/
├── protocol/
│   └── uds/
│       ├── README.md
│       ├── diagnostic_session.md
│       ├── ecu_reset.md
│       ├── read_data_by_identifier.md
│       ├── security_access.md
│       ├── routine_control.md
│       └── ...
│
└── roadmap/

This organization clearly separates:

- Architecture
- Protocol specifications
- Project roadmap

---

# Sprint 33.1

The first implementation step is intentionally small.

src/
└── opendiag/
    └── uds/
        constants.py

Initially, only the following enumerations will be implemented:

```python
class ServiceID(IntEnum):
    ...
```

Followed by:

```python
class DiagnosticSessionType(IntEnum):
    ...
```

No request or response classes will be created before these protocol constants are available.

---

# Expected Progress

| Sprint | Deliverable | Estimated Tests |
|---------|-------------|----------------:|
| 33.1 | Protocol Constants | 30 |
| 33.2 | DiagnosticSessionRequest | 31 |
| 33.3 | DiagnosticSessionResponse | 32 |
| 33.4 | DiagnosticSessionService | 34–35 |
| 33.5 | Service Registry Integration | 36 |

The project will continue following the same philosophy adopted since the beginning:

- Small iterations
- Test-Driven Development
- Fully passing test suite after every change

---

# Contributing Guide

As OpenDiag starts implementing real automotive protocols, a new document should be introduced:

```
CONTRIBUTING.md
```

It will describe:

- Development environment setup
- Running the test suite
- Coding standards
- Test-Driven Development workflow
- Conventional Commits
- Pull request guidelines
- Architecture Decision Records (ADRs)
- Protocol-First Development process

This document will make it significantly easier for new contributors to understand the project's development philosophy.

---

# Project Vision

OpenDiag has reached an important milestone.

The infrastructure phase is complete.

Future development will focus on implementing standardized automotive diagnostic services on top of a well-defined architecture.

Every new protocol implementation will follow the same engineering process, ensuring consistency, maintainability, and high code quality throughout the lifetime of the project.
