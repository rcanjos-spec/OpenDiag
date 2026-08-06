# ADR-003 - Independent UDS Service Classes

**Status:** Accepted

**Date:** 2026-08-05

## Context

The UDS protocol contains many services.

Implementing all service logic inside the UDS client would create a large and difficult-to-maintain class.

## Decision

Each UDS service will be implemented as an independent class.

The UDS client will only coordinate request execution.

## Rationale

This follows the Single Responsibility Principle and keeps each service isolated.

## Consequences

### Positive

- Easier maintenance
- Better unit testing
- Independent evolution of services

### Negative

- Larger number of source files

## Alternatives Considered

### Option A

Implement all services inside UDSClient.

Rejected because it creates excessive coupling.

### Option B

Create one class per service.

Accepted.
