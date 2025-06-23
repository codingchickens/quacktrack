import vertexai
from vertexai import agent_engines
from step_runner_agent.agent import root_agent

PROJECT_ID = "quacktrack-ia"
staging_bucket = "gs://quacktrack-bucket"

vertexai.init(
    project=PROJECT_ID, location="us-central1", staging_bucket=staging_bucket
)

remote_app = agent_engines.create(
    agent_engine=root_agent,
    requirements="requirements.txt",
    extra_packages = ["step_runner_agent"],
    env_vars = {
        "GOOGLE_GENAI_USE_VERTEXAI": "True"
    }
)

