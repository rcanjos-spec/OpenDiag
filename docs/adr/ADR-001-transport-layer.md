# ADR-001 - Transport Layer Abstraction

**Status:** Accepted

**Date:** 2026-08-05

## Context

The UDS layer requires a reliable transport mechanism to exchange diagnostic messages.

Although ISO-TP commonly runs over CAN, future transports such as DoIP or J2534 should also be supported.

Directly coupling the UDS client to the CAN bus would make future extensions difficult.

## Decision

The UDS layer will depend on a Transport abstraction instead of directly communicating with the CAN bus.

The ISO-TP transport will be one implementation of this abstraction.

## Rationale

This approach reduces coupling between layers and allows new transport implementations without modifying the UDS layer.

## Consequences

### Positive

- Low coupling
- High extensibility
- Easier testing
- Future support for DoIP and J2534

### Negative

- Additional abstraction layer
- Slightly more initial implementation effort

## Alternatives Considered

### Option A

The UDS client communicates directly with the CAN bus.

Rejected because it tightly couples the diagnostic layer to a specific transport.

### Option B

Introduce a Transport abstraction.

Accepted.
