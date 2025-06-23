import time
import os
import asyncio
import logging
from google.adk import Runner
from google.adk.memory import VertexAiRagMemoryService
from google.adk.sessions import VertexAiSessionService
from dotenv import load_dotenv
from models import init_db
from utils import call_agent_async
from step_runner_agent.agent import root_agent

logger = logging.getLogger(__name__)
load_dotenv()

PROJECT_ID = "quacktrack-ia"
LOCATION = "us-central1"
REASONING_ENGINE_APP_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/7082510575590178816"
RAG_CORPUS_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/3458764513820540928"
SIMILARITY_TOP_K = 5
VECTOR_DISTANCE_THRESHOLD = 0.7

session_service = VertexAiSessionService(project=PROJECT_ID, location=LOCATION)
memory_service = VertexAiRagMemoryService(
    rag_corpus=RAG_CORPUS_RESOURCE_NAME,
    similarity_top_k=SIMILARITY_TOP_K,
    vector_distance_threshold=VECTOR_DISTANCE_THRESHOLD
)

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
            session_service=session_service,
            memory_service=memory_service
        )

        user_id = input("Please enter your student ID: ")
        session_id = await get_or_create_session(user_id)

        print("Quack to start 🦆")

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
