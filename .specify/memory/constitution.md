<!--
SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0
Rationale: Major update to align with "The Nine Articles of Development" architectural discipline.
Modified principles:
- Replaced initial principles with Articles I-IX framework.
- Article I: Library-First Principle (Added)
- Article II: CLI Interface Mandate (Added)
- Article III: Test-First Imperative (Added)
- Article VII: Minimal Project Structure (Added)
- Article VIII: Framework Trust (Added)
- Article IX: Integration-First Testing (Added)
Added sections:
- Expanded Principles to 9 articles.
Removed sections:
- Initial generic principles.
Templates requiring updates:
- .specify/templates/constitution-template.md (✅ updated to support 9 principles)
Follow-up TODOs:
- TODO(Article IV): Define Article IV.
- TODO(Article V): Define Article V.
- TODO(Article VI): Define Article VI.
-->

# Project Constitution: dz-vehicle-v2

## Mission & Values
Architectural discipline through the Spec-Driven Development (SDD) framework, ensuring consistency, simplicity, and quality in every implementation.

## Principles

### 1. Article I: Library-First Principle
**Rule**: Every feature MUST begin its existence as a standalone library. No feature shall be implemented directly within application code without first being abstracted into a reusable library component.
**Rationale**: This forces modular design from the start and ensures that specifications generate reusable code rather than monolithic applications.

### 2. Article II: CLI Interface Mandate
**Rule**: Every library MUST expose its functionality through a CLI that accepts text as input (stdin, arguments, or files), produces text as output (stdout), and supports JSON format for structured data exchange.
**Rationale**: Enforces observability and testability by ensuring functionality is accessible and verifiable through text-based interfaces.

### 3. Article III: Test-First Imperative
**Rule**: NON-NEGOTIABLE: All implementation MUST follow strict Test-Driven Development. No implementation code shall be written before unit tests are written, validated/approved by the user, and confirmed to FAIL (Red phase).
**Rationale**: Defines behavior through comprehensive tests before generation, ensuring the implementation meets the specification.

### 4. Article IV: [TBD]
**Rule**: TODO(Article IV): Define non-negotiable rules.
**Rationale**: TODO(Article IV): Explain rationale.

### 5. Article V: [TBD]
**Rule**: TODO(Article V): Define non-negotiable rules.
**Rationale**: TODO(Article V): Explain rationale.

### 6. Article VI: [TBD]
**Rule**: TODO(Article VI): Define non-negotiable rules.
**Rationale**: TODO(Article VI): Explain rationale.

### 7. Article VII: Minimal Project Structure (Simplicity)
**Rule**: Maximum 3 projects for initial implementation. Additional projects require documented justification.
**Rationale**: Combats over-engineering and forces justification for every layer of complexity.

### 8. Article VIII: Framework Trust (Anti-Abstraction)
**Rule**: Use framework features directly rather than wrapping them in custom abstractions unless strictly necessary.
**Rationale**: Prevents unnecessary complexity and leverages the stability and features of established frameworks.

### 9. Article IX: Integration-First Testing
**Rule**: Tests MUST use realistic environments: prefer real databases over mocks, use actual service instances over stubs, and mandatory contract tests before implementation.
**Rationale**: Prioritizes real-world validation over isolated unit tests to ensure system-wide integrity.

## Governance

### Amendment Procedure
Proposed changes to this constitution must be submitted as a pull request, reviewed by the team, and result in a version bump following semantic versioning rules.

### Versioning Policy
This constitution follows semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Incompatible changes to core principles or governance.
- MINOR: Additions or significant expansions of guidance.
- PATCH: Clarifications and minor wording updates.

### Compliance Review
Technical decisions, specifications, and implementations will be audited against these principles during the planning and code review phases using "Phase -1 Gates".

## Metadata
- **Version**: 2.0.0
- **Ratification Date**: 2026-02-23
- **Last Amended Date**: 2026-02-23
