[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#quacktrack-agent)

# ➤ QuackTrack Agent A.K.A Ducrates

![ducrates](ducrates.png?raw=true)

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#description)

## ➤ Description

QuackTrack is a Python-based,, multi-agent system designed to help users reflect on their learning experiences. It guides users through structured conversations, using a series of specialized agents to encourage deeper thinking, constructive dialogue, and personal growth. The system leverages Google ADK, Gemini 2.5 Flash, and RAG memory for advanced conversational and memory capabilities.

![agent flow](flow.png?raw=true)

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#table-of-contents)

## ➤ Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [License](#license)


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#installation)

## ➤ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/quacktrack.git
   cd quacktrack
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in required values (e.g., `DATABASE_URL`).


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#usage)

## ➤ Usage

Run the main application:

```bash
python main.py
```

- Enter your student ID when prompted.
- Interact with the system by typing your reflections or questions.
- Type `exit`, `quit`, or `bye` to end the session.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#features)

## ➤ Features

- **Multi-agent architecture:** Modular agents for greeting, compliance, requirements checking, argument building, and Socratic questioning.
- **Session management:** Persistent sessions using a database backend.
- **RAG memory integration:** Stores and retrieves relevant learning content.
- **Ethical and safety compliance:** Built-in checks for privacy, bias, and responsible communication.
- **Conversational guidance:** Encourages users to reflect, elaborate, and deepen their understanding.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#configuration)

## ➤ Configuration

- **Environment Variables:**
  Set in the `.env` file.
  - `DATABASE_URL`: Database connection string (default: `sqlite:///./learning_sessions.db`).
  - Other Google ADK or API credentials as required.

- **RAG Memory Service:**
  Configured in `main.py` with resource name, similarity, and distance threshold.

- **Agent Customization:**
  Agents and their logic are defined in the `step_runner_agent/sub_agents/` directory.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#license)

## ➤ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
