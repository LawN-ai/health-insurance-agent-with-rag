import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from health_insurance_agent import agent
import uuid
import asyncio

# Construct the path to the .env file
project_root = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root, 'health_insurance_agent', '.env')

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)

APP_NAME = "Health Insurance Agent"
USER_ID = "user_1"
SESSION_ID = str(uuid.uuid4())

async def call_agent_async(query, runner_instance, user_id_val, session_id_val):
    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = ""
    async for event in runner_instance.run_async(user_id=user_id_val, session_id=session_id_val, new_message=content):
        # Safely check for tool-related events
        if hasattr(event, 'content') and event.content and event.content.parts:
            part = event.content.parts[0]
            if hasattr(part, 'tool_code'):
                print(f"\n[TOOL CALL] Agent is calling tool: {part.tool_code.name}")
                continue  # A tool call is not the final response
            elif hasattr(part, 'tool_output'):
                print(f"[TOOL OUTPUT] Tool {part.tool_output.name} returned: {part.tool_output.result}")
                continue  # A tool output is not the final response

        # Check for final response event
        if hasattr(event, 'is_final_response') and event.is_final_response():
            if event.content and event.content.parts and hasattr(event.content.parts[0], 'text'):
                final_response_text = event.content.parts[0].text
                print(f"\nAgent Response: {final_response_text}")
            else:
                print("\nAgent Response: (No text part in final response or unexpected structure)")
    return final_response_text

async def main():
    session_service = InMemorySessionService()

    # Create session asynchronously
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # Instantiate Runner
    runner_instance = Runner(agent=agent.root_agent, app_name=APP_NAME, session_service=session_service)

    # Interact with the agent in a loop
    print("Starting chat with Health Insurance Agent. Type 'exit' to end.")
    while True:
        user_query = input("You: ")
        if user_query.lower() == 'exit':
            print("Exiting chat.")
            break
        if not user_query.strip(): # Skip empty input
            continue
        await call_agent_async(user_query, runner_instance, USER_ID, SESSION_ID)

if __name__ == "__main__":
    asyncio.run(main())