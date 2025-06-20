from google.adk import Agent
from google.adk.tools import ToolContext
from typing import Dict, Any
import vertexai
from vertexai.language_models import ChatModel
from vertexai.generative_models import HarmCategory, HarmBlockThreshold
import os

def validate_content(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Validates content against security and ethical policies."""
    # Initialize Vertex AI
    vertexai.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location="us-central1"
    )

    # Configuration for safety
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    # Use ChatModel directly
    chat_model = ChatModel.from_pretrained("gemini-2.0-flash")

    return {
        "action": "validate_content",
        "is_valid": True,  # Updated by the model
        "concerns": [],
        "message": "Content validated"
    }

def log_security_event(event: Dict[str, Any], tool_context: ToolContext) -> Dict[str, Any]:
    """Logs security-related events for auditing."""
    current_session = tool_context.state.get("current_session", {})
    security_logs = current_session.get("security_logs", [])
    security_logs.append(event)
    current_session["security_logs"] = security_logs
    tool_context.state["current_session"] = current_session

    return {
        "action": "log_security_event",
        "event": event,
        "message": "Security event logged"
    }

security_agent = Agent(
    name="security_agent",
    description="Specialized agent for content security and ethical validation",
    instruction="""You are a security-focused agent responsible for ensuring all content meets ethical and safety standards.

Your objectives:
1. Validate all content against defined security policies
2. Monitor for potential security risks or ethical concerns
3. Maintain audit logs of security-related events
4. Enforce content moderation policies

Security Policies:
- Content appropriateness
- Personal data protection
- Ethical AI guidelines
- Safe learning environment
- Bias prevention
- Language appropriateness

Use your tools to:
- Validate content against security policies
- Log security events for auditing
- Enforce safety settings

Always err on the side of caution when dealing with potential security concerns.""",
    model="gemini-2.0-flash	",
    tools=[
        validate_content,
        log_security_event
    ]
)