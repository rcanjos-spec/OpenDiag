# ADR-002 - Object-Oriented UDS API

**Status:** Accepted

**Date:** 2026-08-05

## Context

Users need a simple and maintainable way to build UDS requests and process responses.

Using raw byte arrays exposes protocol details and makes applications harder to read and maintain.

## Decision

The public API will be object-oriented.

Requests and responses will be represented by dedicated classes.

A low-level API using raw bytes will also be available for advanced users.

## Rationale

Object-oriented APIs improve readability, type safety, and maintainability.

## Consequences

### Positive

- Cleaner API
- Better readability
- Easier validation
- Strong typing

### Negative

- More classes
- Slightly larger codebase

## Alternatives Considered

### Option A

Use raw byte arrays.

Rejected because it exposes protocol implementation details.

### Option B

Use Request and Response objects.

Accepted.
