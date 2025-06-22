# Health Insurance Product Agent with RAG

This project is a conversational AI agent designed to assist users in finding suitable health insurance products. It is built using the [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/).

## Project Structure

**Important:** The Google Agent Development Kit (ADK) relies on a specific project structure to discover and load your agent. Please adhere to the following structure:

```
health-insurance-agent-with-rag/  <- Project Root
├── .gitignore
├── README.md
├── requirements.txt
├── health_insurance_agent_runner.py <- Standalone runner script
├── health_insurance_agent/     <- Agent Module Directory
│   ├── __init__.py           <- Makes this a Python package
│   ├── agent.py              <- Defines your `root_agent`
│   └── .env                  <- API keys and environment variables (create this manually)
└── .venv/                    <- Python virtual environment (will be created by you)
```

Key points for ADK compatibility:
*   The `adk web` and `adk run` commands are typically executed from the **Project Root**.
*   ADK looks for an agent module directory (e.g., `health_insurance_agent`).
*   Inside the agent module directory, `__init__.py` is necessary to treat it as a package.
*   The `agent.py` file must define a variable named `root_agent` which holds your main `Agent` instance.

## Setup and Installation

### Prerequisites

*   Python 3.8 or newer
*   Git

### 1. Clone the Repository (if applicable)

If you have this project on a remote Git repository (e.g., GitHub), clone it:

```bash
git clone <repository_url>
cd health-insurance-agent-with-rag
```

If you are working with a local copy, navigate to the project directory.

### 2. Create and Activate Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

**On Windows:**

```bash
# Using Command Prompt (cmd.exe)
python -m venv .venv
.venv\Scripts\activate.bat
```

**On macOS and Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

The agent requires a Google API key for the Gemini model.

1.  Navigate to the `health_insurance_agent` directory.
2.  Create a new file named `.env` in this directory (`health_insurance_agent/.env`).
3.  Add your Google API key to the `.env` file as follows:
    ```env
    GOOGLE_API_KEY=your_actual_google_api_key_here
    ```
4.  Navigate back to the project root directory (`cd ..`).

**Important:** The `.env` file is included in `.gitignore` to prevent accidental commitment of your API key.

## Core Components

### 1. Agent Definition (`health_insurance_agent/agent.py`)

This file defines the `root_agent` using Google ADK's `Agent` class. Key aspects include:

*   **System Prompt**: A detailed set of instructions guiding the agent's personality, goals, and a multi-step tool workflow.
*   **Tool Integration & RAG**: Defines and integrates custom tools that enable a RAG (Retrieval-Augmented Generation) workflow:
    *   `get_health_insurance_products`: A placeholder tool that simulates fetching a product and its corresponding PDF document URL.
    *   `process_product_document`: Downloads the product PDF, extracts the text, and builds an in-memory vector store (using FAISS) for efficient searching.
    *   `answer_from_product_document`: Takes a user's question, searches the vector store for relevant text chunks from the PDF, and returns them as context for the agent to formulate an answer.

### 2. Key Dependencies (`requirements.txt`)

The project relies on several key libraries to enable the RAG functionality:

*   **`google-adk`**: The core framework for building the agent.
*   **`pdfplumber`**: Used to extract text content from PDF documents robustly.
*   **`sentence-transformers`**: Provides the embedding model to convert text into numerical vectors.
*   **`faiss-cpu`**: A library for efficient similarity search, used to create and query the vector index.

### 3. Agent Runner Script (`health_insurance_agent_runner.py`)

This script provides a standalone way to interact with the agent directly from the command line. It's set up for a fully interactive chat session and will print tool call activity for debugging purposes.

## Running the Agent

Ensure your virtual environment is activated and you are in the project root directory (`health-insurance-agent-with-rag`).

There are three primary ways to run the agent:

### 1. Interactive Web UI (Recommended)

This method launches a local web server with a chat interface.

```bash
adk web
```

### 2. Interactive Terminal Runner (for Debugging)

This script provides a fully interactive chat session in your terminal and prints detailed tool activity, which is useful for debugging.

```bash
python health_insurance_agent_runner.py
```

### 3. Single Response from CLI

You can get a single response from the agent for a given query directly from the command line.

```bash
adk run "your query here"
```

