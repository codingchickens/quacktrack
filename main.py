import os
import asyncio
import logging
from dotenv import load_dotenv
from google.adk import Runner
from google.genai import types
from google.adk.sessions import DatabaseSessionService
from google.adk.tools.agent_tool import AgentTool
from orchestrator_agent.agent import root_agent
from orchestrator_agent.sub_agents.rag_agent.agent import rag_agent
from orchestrator_agent.sub_agents.socrates_agent.agent import socrates_agent
from orchestrator_agent.sub_agents.feedback_agent.agent import feedback_agent
from orchestrator_agent.sub_agents.security_agent.agent import security_agent
from models import init_db
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quacktrack.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
load_dotenv()
db_url = os.getenv("DATABASE_URL", "sqlite:///./learning_sessions.db")
session_service = DatabaseSessionService(db_url=db_url)

try:
    init_db(db_url)
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise

root_agent.tools.extend([
    AgentTool(rag_agent),
    AgentTool(socrates_agent),
    AgentTool(feedback_agent),
    AgentTool(security_agent)
])

async def process_agent_response(event):
    """Process and display agent response events."""
    # Log basic event info
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for final response after specific parts
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            # Use colors and formatting to make the final response stand out
            print(
                f"\n╔══ AGENT RESPONSE ═════════════════════════════════════════"
            )
            print(f"{final_response}")
            print(
                f"╚═════════════════════════════════════════════════════════════\n"
            )
        else:
            print(
                f"\n==> Final Agent Response: [No text content in final event]\n"
            )

    return final_response

async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n--- Running Query: {query} ---"
    )
    final_response_text = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during agent call: {e}")

    return final_response_text

async def get_or_create_session(user_id: str):
    """Gets an existing session or creates a new one."""
    try:
        existing_sessions = await session_service.list_sessions(
            app_name="quacktrack",
            user_id=user_id
        )

        if existing_sessions and len(existing_sessions.sessions) > 0:
            session_id = existing_sessions.sessions[0].id
            logger.info(f"Continuing existing session: {session_id}")
            return session_id

        # Create new session with initial state
        session_id = f"session_{int(time.time())}"
        initial_state = {
            "student_info": {
                "id": user_id,
                "name": "",
                "learning_preferences": {},
                "current_topics": []
            },
            "learning_history": {
                "sessions": [],
                "interactions": [],
                "progress_markers": []
            },
            "current_session": {
                "context": "",
                "objectives": [],
                "status": "active",
                "security_logs": []
            },
            "student_text": "",
            "memory_flags": ""
        }

        await session_service.create_session(
            app_name="quacktrack",
            user_id=user_id,
            session_id=session_id,
            state=initial_state
        )
        logger.info(f"New session created: {session_id}")
        return session_id
    except Exception as e:
        logger.error(f"Error in session management: {e}")
        raise

async def main():
    """Main application loop."""
    try:
        # Configure the runner with session service
        runner = Runner(
            agent=root_agent,
            app_name="quacktrack",
            session_service=session_service
        )

        user_id = input("Please enter your student ID: ")
        session_id = await get_or_create_session(user_id)

        # Start interaction
        print("\nWelcome to QuackTrack - Your Personalized Learning Assistant")
        print("Type 'exit' to end the session\n")

        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    break

                await call_agent_async(runner, user_id, session_id, user_input)
            except KeyboardInterrupt:
                print("\nSession interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error during interaction: {e}")
                print("\nAn error occurred. Please try again.")

        print("\nThank you for using QuackTrack! Goodbye!")

    except Exception as e:
        logger.error(f"Critical error in main loop: {e}")
        print("\nA critical error occurred. Please check the logs and try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print("\nApplication error. Please check the logs.")
