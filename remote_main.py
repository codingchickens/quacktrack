import vertexai

agent_engine = vertexai.agent_engines.get('projects/quacktrack-ia/locations/us-central1/reasoningEngines/1697689933751255040')
session = agent_engine.create_session(user_id="0")

for event in agent_engine.stream_query(
    user_id="u_456",
    session_id=session["id"],
    message="Can you remind me about my last learning session?",
):
  print(event)