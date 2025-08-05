import asyncio
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()


async def main():
    # Create a new session service to store state
    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Maurizio Ipsale",
        "user_preferences": """
            I like to play piano, watching tv shows (especially sci-fi), reading books (sci-fi, thriller, popular books), staying with my family and travelling.
            My favorite food is everything coming from Sicily. I come from Sicily as well, even though I live in Modena.
            My favorite TV show is Black Mirror.
            My favorite movie is Back to the Future.
        """,
    }

    # Create a NEW session
    APP_NAME = "Mauri Bot"
    USER_ID = "maurizio_ipsale"
    SESSION_ID = str(uuid.uuid4())
    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")

    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    print("\nStarting interactive session with Mauri Bot...")
    print("Type 'exit' or 'quit' to end the session.")
    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        new_message = types.Content(role="user", parts=[types.Part(text=user_input)])

        response_text = ""
        for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text

        if response_text:
            print(f"Agent: {response_text}")

    print("==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Log final Session state
    print("=== Final Session State ===")
    for key, value in session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
