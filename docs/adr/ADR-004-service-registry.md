# ADR-004 - Service Registry

**Status:** Accepted

**Date:** 2026-08-05

## Context

The UDS client must determine which service implementation is responsible for processing each request.

Using conditional statements would require modifications whenever a new service is added.

## Decision

A Service Registry will map Service IDs (SIDs) to their corresponding service implementations.

The UDS client will delegate service resolution to the registry.

## Rationale

This design follows the Open/Closed Principle by allowing new services to be added without modifying the UDS client.

## Consequences

### Positive

- Extensible architecture
- Reduced coupling
- Simpler UDS client
- Easier plugin support in the future

### Negative

- Requires registry initialization

## Alternatives Considered

### Option A

Use if/elif statements.

Rejected because every new service would require changes to the UDS client.

### Option B

Use a Service Registry.

Accepted.
