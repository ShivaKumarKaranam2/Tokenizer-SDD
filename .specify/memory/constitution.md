<!--
Sync Impact Report
Version change: [none, unfilled template] → 1.0.0
Modified principles: N/A (initial ratification)
Added sections:
  - Core Principles (I–XIV)
  - Technology Stack
  - Quality & Security Gates
  - Governance
Removed sections: none
Templates requiring updates:
  - .specify/templates/plan-template.md — ⚠ pending manual check (verify Constitution Check gate references these principles)
  - .specify/templates/spec-template.md — ⚠ pending manual check (no direct constitution reference expected)
  - .specify/templates/tasks-template.md — ⚠ pending manual check (verify task categorization aligns with testing principles)
Follow-up TODOs: none
-->

# Tokenizer Application Constitution

## Core Principles

### I. Simple, Modular Architecture
The system MUST be composed of two clearly separated services: a Streamlit
frontend and a FastAPI backend, communicating only over REST/HTTP. Each
service MUST remain independently runnable and independently testable.
New functionality MUST fit into this two-service shape before any new
component, service, or layer is introduced.
Rationale: A small tokenization tool has no need for distributed complexity;
simplicity keeps the system easy to reason about, run locally, and hand off.

### II. Streamlit Is Presentation-Only
The Streamlit frontend MUST be limited to rendering UI, collecting user input
(text, TXT, PDF uploads), calling the backend API, and displaying results and
errors. The frontend MUST NOT implement tokenization, PDF parsing, or any
business/document-processing logic.
Rationale: Keeping the UI layer "dumb" prevents logic drift between what the
user sees and what the backend actually computes.

### III. FastAPI Owns Tokenization and Document Processing
All tokenization and document-processing logic (text extraction from PDFs,
input normalization, token counting/encoding) MUST live in the FastAPI
backend, exposed through well-defined endpoints. The frontend MUST treat the
backend as the sole authority for these operations.
Rationale: Centralizing processing logic in one service creates a single
place to fix bugs, add encodings, or change extraction behavior.

### IV. No Duplicated Tokenization Logic
Tokenization logic MUST NOT be reimplemented, copied, or approximated in the
Streamlit layer, even for previews or client-side estimates. If the frontend
needs token counts, it MUST obtain them from the backend API.
Rationale: Duplicate implementations inevitably diverge from tiktoken's
actual behavior, producing misleading counts.

### V. tiktoken Is the Single Source of Truth
All token counting and encoding/decoding operations MUST use the `tiktoken`
library exclusively. No alternative or custom tokenizers MUST be introduced
without amending this constitution.
Rationale: A single, well-defined tokenizer guarantees consistent, correct
results across the entire application.

### VI. Backend-Enforced Input Validation
The FastAPI backend MUST validate all uploaded files and input payloads,
including file type, file size, and text length limits, before processing.
Validation MUST NOT rely on frontend checks alone; the frontend MAY provide
early feedback, but the backend is the enforcement point.
Rationale: Client-side checks can be bypassed by direct API calls; only
backend enforcement protects the system reliably.

### VII. Explicit API Contracts via Pydantic
Every backend request and response MUST be defined with explicit Pydantic
models. Endpoints MUST NOT accept or return untyped/free-form JSON where a
structured model can be defined.
Rationale: Explicit contracts make the API self-documenting, catch shape
errors early, and keep frontend/backend integration predictable.

### VIII. Unit Tests for Tokenization and Extraction
Tokenization logic and PDF text-extraction logic MUST each have dedicated
pytest unit tests covering normal input, edge cases (empty text, unusual
encodings), and known failure modes. New tokenization or extraction code
MUST NOT be merged without accompanying unit tests.
Rationale: These two functions are the core value of the application and
carry the highest risk of silent correctness bugs.

### IX. API Tests for Backend Endpoints
Every FastAPI endpoint MUST have pytest-based API tests covering success
responses, validation failures, and error responses. Tests MUST use FastAPI's
test client rather than requiring a running server.
Rationale: API-level tests verify the actual contract clients depend on, not
just internal function behavior.

### X. Graceful Handling of Bad Input
The system MUST handle malformed PDFs, unsupported file types, empty input,
and invalid or unsupported encodings without crashing. Every such case MUST
return a clear, structured error response (via the Pydantic error model) with
an appropriate HTTP status code; the frontend MUST surface these errors
legibly to the user.
Rationale: Document tokenization tools routinely receive messy real-world
input; failures must be informative, not opaque crashes.

### XI. No Unnecessary Persistence
The application MUST NOT introduce a database or persistent storage layer.
Uploaded content and results MUST be processed in-memory/transiently for the
duration of a request only. Any future requirement for persistence requires
an explicit constitution amendment.
Rationale: This application is a stateless utility; persistence adds
operational and security surface area with no corresponding requirement.

### XII. Local-Development and Simple Deployment
The application MUST remain runnable with minimal setup: a standard Python
environment, `pip install` of dependencies, and two local processes
(`streamlit run ...` and a FastAPI server, e.g. via `uvicorn`). Deployment
MUST NOT require container orchestration, message queues, or multi-service
infrastructure beyond the two application services.
Rationale: Ease of local development and simple deployment is a stated
project goal, not an afterthought.

### XIII. Readable Code Over Abstraction
Python code MUST favor clarity and directness over speculative abstraction,
inheritance hierarchies, or design patterns not justified by current
requirements. Helper functions and classes MUST only be introduced when they
remove real duplication or materially improve readability.
Rationale: A small, well-scoped application benefits more from readability
than from extensibility no one has asked for.

### XIV. Scope Discipline
Features, endpoints, or UI elements not required by the current
specification MUST NOT be added speculatively. Any new capability (e.g. new
file formats, new tokenizer models, batch processing) requires an explicit
specification update before implementation.
Rationale: Scope creep is the most common way small tools become
unmaintainable; this project stays deliberately narrow.

## Technology Stack

The following stack is fixed for this project and MUST NOT be substituted
without a constitution amendment:
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Tokenization**: tiktoken
- **PDF extraction**: PyMuPDF
- **Language**: Python
- **API communication**: REST/HTTP (JSON payloads, Pydantic-defined schemas)
- **Testing**: pytest (unit tests and API tests)

Introducing an additional library MUST be justified against an existing
principle (e.g. a new library that reduces duplication under Principle XIII)
rather than added for convenience alone.

## Quality & Security Gates

- **Test gate**: A change to tokenization or PDF-extraction logic MUST ship
  with passing pytest unit tests (Principle VIII); a change to any endpoint
  MUST ship with passing pytest API tests (Principle IX). Neither MUST be
  merged with failing or skipped tests.
- **Validation gate**: Any code path that accepts a file or text input MUST
  pass through backend validation (Principle VI) before reaching tokenization
  or extraction logic.
- **Error-handling gate**: Any new input path MUST be reviewed against
  Principle X's failure modes (malformed PDF, unsupported file, empty input,
  invalid encoding) before being considered complete.
- **Security baseline**: The backend MUST enforce file-size and file-type
  limits server-side, MUST NOT execute or evaluate uploaded content, and MUST
  treat all extracted text as untrusted data (no dynamic execution, no
  unsanitized logging of full document contents at info level in production).
- **Dependency discipline**: Only the libraries listed under Technology Stack
  (plus their direct, minimal supporting dependencies such as `uvicorn` or
  `python-multipart`) MUST be added without an amendment.

## Governance

This constitution supersedes ad-hoc practice for the Tokenizer Application.
All plans, specs, and code reviews MUST verify compliance with these
principles before work is considered complete.

**Amendment procedure**: Amendments are proposed by editing this document,
recording the change in a Sync Impact Report comment at the top of the file,
and updating the version per the policy below. Amendments that remove or
redefine a principle MUST call out affected templates/specs for follow-up.

**Versioning policy** (semantic versioning applied to this document):
- **MAJOR**: Backward-incompatible governance changes, or removal/redefinition
  of an existing principle.
- **MINOR**: A new principle or section is added, or existing guidance is
  materially expanded.
- **PATCH**: Wording clarifications, typo fixes, or non-semantic refinements.

**Compliance review**: Every feature plan (`/speckit-plan`) MUST include a
Constitution Check against these principles before implementation tasks are
generated. Any deviation MUST be explicitly justified in the plan's
Complexity Tracking section or the deviation MUST be removed.

**Version**: 1.0.0 | **Ratified**: 2026-09-16 | **Last Amended**: 2026-09-16
