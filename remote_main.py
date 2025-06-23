from vertexai import agent_engines

user_id = "0"
agent_engine = agent_engines.get('projects/749505306239/locations/us-central1/reasoningEngines/2855115037985472512')
sessions = agent_engine.list_sessions(user_id=user_id).get('sessions', [])
session = next(iter(sessions), None)

if not session:
  session = agent_engine.create_session(user_id=user_id)

for event in agent_engine.stream_query(
    user_id=user_id,
    session_id=session["id"],
    message="Can you remind me about my last learning session?",
):
  print(event)