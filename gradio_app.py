import gradio as gr
import uuid
import os
from dotenv import load_dotenv



# --- Environment Setup ---
# Evidence-based fix: Load the .env file to get the GOOGLE_API_KEY.
project_root = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root, 'health_insurance_agent', '.env')
load_dotenv(dotenv_path=dotenv_path)
# -------------------------

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from health_insurance_agent import agent

# --- ADK Setup ---
# Create a single, shared session service and runner instance for the Gradio app.
APP_NAME = "Health Insurance Agent"
session_service = InMemorySessionService()
health_insurance_runner = Runner(
    agent=agent.root_agent, 
    app_name=APP_NAME, 
    session_service=session_service
)
# -----------------

# Keep track of created sessions to avoid creating them more than once.
created_sessions = set()

async def process_message(message: str, history: list, session_id: str):
    """Processes a user's message using the shared ADK runner."""
    user_id = "gradio_user"  # Static user ID for all Gradio sessions for simplicity

    try:
        # Evidence-based fix: Create the session if it's the first time we've seen this ID.
        if session_id not in created_sessions:
            await session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id
            )
            created_sessions.add(session_id)

        # Now, process the user's message.
        full_response = ""
        content = types.Content(role="user", parts=[types.Part(text=message)])
        async for event in health_insurance_runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.is_final_response() and event.content and event.content.parts:
                full_response += event.content.parts[0].text
        return full_response
    except Exception as e:
        return f"An error occurred: {e}"

async def chat_interface_fn(message, history, session_id_state):
    """Wrapper function for Gradio's ChatInterface."""
    session_id = session_id_state if session_id_state else str(uuid.uuid4())
    response = await process_message(message, history, session_id)
    return response

with gr.Blocks() as demo:
    gr.Markdown("# Health Insurance Agent")
    session_id_state = gr.State(str(uuid.uuid4()))

    gr.ChatInterface(
        fn=chat_interface_fn,
        additional_inputs=[session_id_state],
        title="Health Insurance Chatbot",
        description="Ask me about health insurance products!",
        examples=[
            ["I need hospital cover for my family"],
            ["What extras products do you have?"],
            ["I want to know about hospital and extras cover."]
        ]
    )

demo.launch(share=True)
