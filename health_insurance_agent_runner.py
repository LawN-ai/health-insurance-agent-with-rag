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
        # Uncomment to debug all event types:
        # print(f"[DEBUG Event] Author: {getattr(event, 'author', 'N/A')}, Type: {type(event).__name__}, Content: {getattr(event, 'content', 'N/A')}")

        if hasattr(event, 'is_final_response') and event.is_final_response():
            if event.content and event.content.parts and hasattr(event.content.parts[0], 'text'):
                final_response_text = event.content.parts[0].text
                print(f"Agent Response: {final_response_text}")
            else:
                print("Agent Response: (No text part in final response or unexpected structure)")
        # It's possible intermediate text parts come in other event types or FinalResponseEvents without is_final_response() being true yet
        # For now, we are primarily focused on distinct tool calls/responses and the ultimate final text response.
        # If accumulating intermediate text is needed, the logic from the GitHub issue (concatenating text from non-final events) would be added here.
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