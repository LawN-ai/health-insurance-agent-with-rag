# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-06-22

### Changed
- Improved the `health_insurance_agent_runner.py` script to be fully interactive and to print tool calls and tool outputs for better debugging visibility.

### Fixed
- Corrected an `AttributeError` in `health_insurance_agent_runner.py` by implementing a more robust method for checking event types (`hasattr` instead of checking `event.type`).

## [1.1.0] - 2025-06-22

### Added
- Implemented a RAG (Retrieval-Augmented Generation) pipeline.
- New tool `process_product_document` to download, parse, and index PDF product documents into a FAISS vector store.
- New tool `answer_from_product_document` to query the vector store and retrieve context for answering user questions.
- New dependencies: `pdfplumber`, `sentence-transformers`, `faiss-cpu`.

### Changed
- Updated agent's system prompt to orchestrate the new multi-step RAG workflow.
- Updated `README.md` with details on the new RAG functionality and dependencies.
- Updated project title and paths in `README.md`.

## [1.0.0] - 2025-06-22

### Added
- Initial project setup with Google ADK.
- A friendly and engaging conversational agent.
- Placeholder `get_health_insurance_products` tool to simulate product retrieval.
- `health_insurance_agent_runner.py` for basic script-based interaction.
- `README.md` and `changelog.md` for documentation.
- `.gitignore` to exclude virtual environment and `.env` files.
