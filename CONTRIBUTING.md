# Contributing to CreatorRadar

Thank you for your interest in contributing to CreatorRadar!

## Development Guidelines

1. **Architecture Principles**:
   - Maintain platform-agnostic core domain models.
   - Do not hardcode vendor-specific API calls in business logic.
   - Enforce the **Inspiration ≠ Replication** philosophy.

2. **Branching & Commits**:
   - Create feature branches named `feature/description` or `fix/description`.
   - Write clear, concise commit messages.

3. **Testing Requirements**:
   - Every new abstraction or endpoint must include pytest unit tests in `tests/`.
   - Run `pytest tests/` before submitting a Pull Request.

4. **Code Style**:
   - Follow PEP 8 for Python code.
   - Use typed Pydantic models for request/response validation.
