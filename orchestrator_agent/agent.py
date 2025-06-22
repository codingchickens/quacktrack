from google.adk import Agent
from google.adk.tools import ToolContext
from typing import Dict, Any
import json
from google.genai import types
from google import genai
from google.genai.types import HttpOptions

def call_orchestrator_gemini(student_text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Analizes student text and decide routing."""

    tool_context.state["student_text"] = student_text

    safety_settings = [
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold= types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold = types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE),
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold = types.HarmBlockThreshold.BLOCK_ONLY_HIGH),
        types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold = types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE)
    ]

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            temperature = 0.2, top_p = 0.8, max_output_tokens = 512, safety_settings=safety_settings
        ),
    )
    response = chat_session.send_message(student_text)

    student_info = tool_context.state.get("student_info", {})
    learning_history = tool_context.state.get("learning_history", {})

    prompt = f"""
    Analyze the following student message and determine:
    1. The most appropriate agent to handle it (socrates, feedback, or rag)
    2. The language being used
    3. Any potential safety concerns

    Student Info: {json.dumps(student_info)}
    Learning History: {json.dumps(learning_history)}
    Current Message: {student_text}

    Respond in JSON format with:
    {
        "selected_agent": "agent_name",
        "language": "detected_language",
        "routing_reason": "explanation"
        "safety_check": {
            "is_safe": boolean,
            "concerns": []
        },
    }
    """

    try:
        response = chat_session.send_message(prompt)
        return { "response": response.text }

    except json.JSONDecodeError:
        return {
            "selected_agent": "none",
            "language": "unknown",
            "safety_check": {
                "is_safe": False,
                "concerns": ["Failed to process response"]
            },
            "routing_reason": "Error processing response"
        }

root_agent = Agent(
    name="orchestrator_agent",
    description="Central agent that coordinates the learning system, ensuring ethics and intelligent routing",
    instruction="""Role and Purpose:
        You are the `orchestrator_agent`, a central coordination component within a multi-agent educational system. Your function is twofold: (1) ensure that all interactions comply with strict ethical and safety standards, and (2) route each valid student message to the appropriate internal agent based on predefined logic.

        Modular Architecture:
        Your operation includes collaboration with the Gemini model to analyze incoming messages using natural language processing (NLP). Use this analysis to apply ethical screening and routing rules. You interact with two internal agents:
        - `socrates_agent`: for Socratic, question-based engagement.
        - `feedback_agent`: for reflective, feedback-based responses.

        Routing Logic (Apply After Ethics Validation):
        Once the message is deemed ethical, route based on the following conditions:

        - If the message is short (~under 30 words) or vague → `socrates_agent`
        - If it contains closure cues (e.g., "I'm done", "I already answered") → `feedback_agent`
        - If the student has already responded to metacognitive prompts with elaboration → `feedback_agent`
        - If there is clear expression of insight/reflection (e.g., "I learned", "I didn’t expect", "this helped me see…") → `feedback_agent` with `trigger_integration = true`

        Output:
        ### If rejected for ethics:
        Answer the student politely that he/she should be more serious about this process and that they must reformulate their answer

        ### If approved and routed:
        Delegate to the proper agent
        """,
    model="gemini-2.0-flash"
)
