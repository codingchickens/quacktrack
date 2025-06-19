# QuackTrack - Multi-Agent Educational System

QuackTrack is an intelligent educational system that uses multiple specialized AI agents to provide personalized learning experiences. Built for the Google Cloud ADK Hackathon, it leverages Vertex AI for natural language understanding and learning assistance.

## Features

- **Multi-Agent Architecture**
  - Orchestrator Agent: Central coordinator with language detection
  - Socrates Agent: Socratic method questioning
  - Feedback Agent: Constructive feedback
  - RAG Agent: Information retrieval and context
  - Security Agent: Content moderation and safety

- **Smart Capabilities**
  - Language detection and multilingual support
  - Ethical content filtering
  - Personalized learning paths
  - Session persistence
  - Security auditing

## Technical Stack

- Python 3.12+
- Google ADK
- Vertex AI
- SQLAlchemy
- SQLite

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

1. Start the system:
```bash
python main.py
```

2. Interact with the system through the command line interface.

## Architecture

### Agent Structure
```
orchestrator_agent/
├── agent.py (Root orchestrator)
└── sub_agents/
    ├── socrates_agent/
    ├── feedback_agent/
    ├── rag_agent/
    └── security_agent/
```

### Database Schema
- students: User profiles and preferences
- sessions: Learning sessions
- interactions: Message history
- security_logs: Security audit trail

## Development

### Adding New Agents

1. Create a new directory under `sub_agents/`
2. Implement the agent with required tools
3. Register the agent in the orchestrator

### Security Considerations

- Content validation through Security Agent
- Ethical AI guidelines enforcement
- Personal data protection
- Safe learning environment maintenance

## Known Issues

- **Model Availability**: Ensure that the models used are available in your region. Use `chat-bison` or `text-bison` as alternatives if other models are unavailable.
- **Service Account Permissions**: Verify that the service account has the necessary permissions for Vertex AI and Google Drive.

## License

[Add your license here]

## Contributors

[Add contributors here]
