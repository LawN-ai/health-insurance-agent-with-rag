# Health Insurance Product Agent

This project is a conversational AI agent designed to assist users in finding suitable health insurance products. It is built using the [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/).

Currently, the agent is in its first stage of development, focusing on establishing a friendly and engaging conversation with the user.

## Project Structure

**Important:** The Google Agent Development Kit (ADK) relies on a specific project structure to discover and load your agent. Please adhere to the following structure:

```
health-insurance-chat-agent-3/  <- Project Root
├── .gitignore
├── README.md
├── requirements.txt
├── health_insurance_agent/     <- Agent Module Directory
│   ├── __init__.py           <- Makes this a Python package
│   ├── agent.py              <- Defines your `root_agent`
│   └── .env                  <- API keys and environment variables (create this from .env.example if provided, or manually)
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
cd health-insurance-chat-agent-3
```

If you are working with a local copy, navigate to the project directory:

```bash
cd path/to/health-insurance-chat-agent-3
```

### 2. Create and Activate Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

**On Windows:**

*   **Using Command Prompt (cmd.exe):**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate.bat 
    ```

*   **Using PowerShell:**
    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
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

1.  Navigate to the `health_insurance_agent` directory:
    ```bash
    cd health_insurance_agent
    ```
2.  Create a new file named `.env` in this directory (`health_insurance_agent/.env`).
3.  Add your Google API key to the `.env` file as follows:
    ```env
    GOOGLE_API_KEY=your_actual_google_api_key_here
    ```
    Replace `your_actual_google_api_key_here` with your valid API key.
4.  Navigate back to the project root directory:
    ```bash
    cd ..
    ```

**Important:** The `.env` file is included in `.gitignore` to prevent accidental commitment of your API key.

## Core Components

### 1. Agent Definition (`health_insurance_agent/agent.py`)

This file is the heart of the conversational AI. It defines the `root_agent` using Google ADK's `Agent` class. Key aspects include:

*   **System Prompt**: A detailed set of instructions (`system_prompt` variable) guiding the agent's personality, goals, conversation style, tool usage, and how to format information.
*   **Tool Integration**: Defines and integrates custom tools, such as `get_health_insurance_products`, which the agent can use to fetch information or perform actions.
*   **Model Configuration**: Specifies the underlying language model (e.g., "gemini-2.0-flash") and other agent parameters.
*   **ADK Compatibility**: Adheres to ADK's structure by naming the main agent instance `root_agent`, allowing ADK to discover and run it.

### 2. Agent Runner Script (`health_insurance_agent_runner.py`)

This script (located in the project root) provides a standalone way to interact with and test the `health_insurance_agent` directly from the command line, without needing the full `adk web` or `adk run` interfaces. Its main functions are:

*   **Environment Setup**: Loads environment variables (like `GOOGLE_API_KEY`) from the `.env` file located within the `health_insurance_agent` sub-directory.
*   **Session Management**: Initializes an `InMemorySessionService` to manage conversational state. It creates a new session for each run.
*   **Runner Initialization**: Sets up an ADK `Runner` instance, linking it to the `root_agent` defined in `agent.py` and the session service.
*   **Asynchronous Interaction**: Uses `asyncio` to handle the asynchronous nature of agent communication. It includes an `async def call_agent_async` function to send user messages to the agent and process the stream of events (including final responses and tool calls/responses).
*   **Conversation Simulation**: The `async def main()` function orchestrates session creation and makes one or more calls to `call_agent_async` to simulate a conversation.

This script is particularly useful for quick tests, debugging specific interaction flows, or when a full web UI is not required.

## Running the Agent

Ensure your virtual environment is activated and you are in the project root directory (`health-insurance-chat-agent-3`).

There are two primary ways to run the agent:

### 1. Using the ADK Web UI (Recommended for Interactive Development)

This launches a web interface where you can chat with the agent and inspect events.

```bash
adk web
```

**Note for Windows users:** If you encounter a `_make_subprocess_transport NotImplementedError`, try:

```bash
adk web --no-reload
```

After running the command, open the URL provided (usually `http://localhost:8000` or `http://127.0.0.1:8000`) in your browser. Select `health_insurance_agent` from the agent dropdown menu in the UI.

### 2. Running Directly in the Command Line

This allows for direct terminal-based interaction with the agent.

```bash
adk run health_insurance_agent
```

To stop the agent, press `Ctrl+C`.

### 3. Using the Standalone Runner Script

For more direct script-based interaction and testing, you can use the `health_insurance_agent_runner.py` script located in the project root. This script handles session setup and allows you to send messages to the agent programmatically.

1.  Ensure your virtual environment is activated and you are in the project root directory.
2.  Run the script:
    ```bash
    python health_insurance_agent_runner.py
    ```
    The script will typically send an initial message (e.g., "I am looking for health insurance") and print the agent's response, including any tool activity. You can modify the `main()` function in `health_insurance_agent_runner.py` to simulate different conversational turns.
