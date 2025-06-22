import asyncio
import os
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.memory import VertexAiRagMemoryService
from google.adk.runners import Runner
from google.adk.tools import load_memory # Tool to query memory
from google.genai.types import Content, Part

# --- Constants ---
APP_NAME = "memory_example_app"
USER_ID = "mem_user"
MODEL = "gemini-2.0-flash" # Use a valid model
os.environ["GOOGLE_CLOUD_PROJECT"]="quacktrack-ia"
os.environ["GOOGLE_CLOUD_LOCATION"]="us-central1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"]="True"
RAG_CORPUS_RESOURCE_NAME = "projects/quacktrack-ia/locations/us-central1/ragCorpora/6917529027641081856"
SIMILARITY_TOP_K = 5
VECTOR_DISTANCE_THRESHOLD = 0.7


# --- Agent Definitions ---
# Agent 1: Simple agent to capture information
info_capture_agent = LlmAgent(
    model=MODEL,
    name="InfoCaptureAgent",
    instruction="Acknowledge the user's statement.",
    # output_key="captured_info" # Could optionally save to state too
)

# Agent 2: Agent that can use memory
memory_recall_agent = LlmAgent(
    model=MODEL,
    name="MemoryRecallAgent",
    instruction="Answer the user's question. Use the 'load_memory' tool "
                "if the answer might be in past conversations.",
    tools=[load_memory] # Give the agent the tool
)

# --- Services and Runner ---
session_service = InMemorySessionService()
memory_service = VertexAiRagMemoryService(
    rag_corpus=RAG_CORPUS_RESOURCE_NAME,
    similarity_top_k=SIMILARITY_TOP_K,
    vector_distance_threshold=VECTOR_DISTANCE_THRESHOLD
)

runner = Runner(
    # Start with the info capture agent
    agent=info_capture_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service # Provide the memory service to the Runner
)

# --- Scenario ---

# Turn 1: Capture some information in a session
print("--- Turn 1: Capturing Information ---")
session1_id = "session_info"
session1 = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session1_id)
user_input1 = Content(parts=[Part(text="My favorite project is Project Alpha.")], role="user")

# Run the agent
final_response_text = "(No final response)"
async for event in runner.run_async(user_id=USER_ID, session_id=session1_id, new_message=user_input1):
    if event.is_final_response() and event.content and event.content.parts:
        final_response_text = event.content.parts[0].text
print(f"Agent 1 Response: {final_response_text}")

# Get the completed session
completed_session1 = await runner.session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session1_id)

# Add this session's content to the Memory Service
print("\n--- Adding Session 1 to Memory ---")
memory_service = await memory_service.add_session_to_memory(completed_session1)
print("Session added to memory.")

# Turn 2: In a *new* (or same) session, ask a question requiring memory
print("\n--- Turn 2: Recalling Information ---")
session2_id = "session_recall" # Can be same or different session ID
session2 = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session2_id)

# Switch runner to the recall agent
runner.agent = memory_recall_agent
user_input2 = Content(parts=[Part(text="What is my favorite project?")], role="user")

# Run the recall agent
print("Running MemoryRecallAgent...")
final_response_text_2 = "(No final response)"
async for event in runner.run_async(user_id=USER_ID, session_id=session2_id, new_message=user_input2):
    print(f"  Event: {event.author} - Type: {'Text' if event.content and event.content.parts and event.content.parts[0].text else ''}"
        f"{'FuncCall' if event.get_function_calls() else ''}"
        f"{'FuncResp' if event.get_function_responses() else ''}")
    if event.is_final_response() and event.content and event.content.parts:
        final_response_text_2 = event.content.parts[0].text
        print(f"Agent 2 Final Response: {final_response_text_2}")
        break # Stop after final response

# Expected Event Sequence for Turn 2:
# 1. User sends "What is my favorite project?"
# 2. Agent (LLM) decides to call `load_memory` tool with a query like "favorite project".
# 3. Runner executes the `load_memory` tool, which calls `memory_service.search_memory`.
# 4. `InMemoryMemoryService` finds the relevant text ("My favorite project is Project Alpha.") from session1.
# 5. Tool returns this text in a FunctionResponse event.
# 6. Agent (LLM) receives the function response, processes the retrieved text.
# 7. Agent generates the final answer (e.g., "Your favorite project is Project Alpha.").
