# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-06-22

### Added
- Initial project setup with Google ADK.
- Basic conversational agent to gather user requirements for health insurance.
- Implemented a RAG (Retrieval-Augmented Generation) pipeline.
- New tool `process_product_document` to download, parse, and index PDF product documents into a FAISS vector store.
- New tool `answer_from_product_document` to query the vector store and retrieve context for answering user questions.
- Updated agent's system prompt to orchestrate the new multi-step RAG workflow.
- Added dependencies: `pdfplumber`, `sentence-transformers`, `faiss-cpu`.
- Created `changelog.md` to track project versions.

### Changed
- Updated `README.md` with details on the new RAG functionality and dependencies.
