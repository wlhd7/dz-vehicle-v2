# Research: Unattended Vehicle Asset Pickup

## Technical Context
The project follows the "Nine Articles of Development" from the Project Constitution. Key constraints:
- **Article I (Library-First)**: Implementation must be a standalone library.
- **Article II (CLI-Interface)**: Must provide a CLI with JSON support.
- **Article III (Test-First)**: Strict TDD.
- **Article VII (Simplicity)**: Minimal project structure.
- **Article VIII (Framework Trust)**: Use framework features directly.
- **Article IX (Integration-First)**: Use realistic environments (e.g., SQLite for DB).

## Decision: Technology Stack
Based on the environment (Linux) and the requirement for a CLI and library-first approach, the following stack is chosen:
- **Language**: Python 3.9+ (Core Library & CLI).
- **Backend Framework**: FastAPI (Bridge between Library and Frontend).
- **Frontend Framework**: Vue 3 (Composition API) + TypeScript.
- **UI Library**: Element Plus (for rapid development and consistent UI).
- **CLI**: Typer (Article II mandate).
- **Database**: SQLite (Article IX requirement for realistic environments).
- **Testing**: pytest (Backend), Vitest (Frontend).

## Rationale
- **Python** is pre-installed in most Linux environments and has superior support for CLI and library development.
- **Vue 3 (Composition API)** provides a clean, reactive, and type-safe way to build the user interface, following Article VII (Simplicity) by being more intuitive for form-heavy applications.
- **FastAPI** provides a robust way to handle data and future web interfaces while staying "Library-First".
- **Typer** allows for rapid CLI development that is easily testable.

## Alternatives Considered
- **Go**: Excellent for CLIs, but Python's speed of development for business logic and database integration is preferred here.
- **Node.js**: Good, but Python's standard library and type hinting are better suited for "Library-First" backend logic in this specific context.

## Resolved Unknowns
- **OTP Generation**: Will use a simple secure random selection from the admin-provided pool stored in the database.
- **Identity Verification**: Name and ID digits will be stored in a `whitelist` table.
- **Persistence**: Using SQLite ensures persistence without heavy infrastructure.
