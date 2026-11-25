# EngineeringTeam Crew

Welcome to the EngineeringTeam Crew project. This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to the project directory and install the project dependencies:

```bash
uv sync
```

Alternatively, install the project into an existing Python environment:

```bash
python -m pip install -e .
```

CrewAI's CLI can also manage installation if it is already available:

```bash
crewai install
```
### Customizing

**Configure a Gemini API key before running the crew.** The agents in `src/engineering_team/config/agents.yaml` currently use `gemini/gemini-1.5-flash`, so set `GEMINI_API_KEY` in your environment or `.env` file (and ensure your installed CrewAI/LiteLLM configuration loads it). An `OPENAI_API_KEY` alone does not authenticate the configured Gemini models. Never commit your `.env` file or API keys.

- Modify `src/engineering_team/config/agents.yaml` to define your agents
- Modify `src/engineering_team/config/tasks.yaml` to define your tasks
- Modify `src/engineering_team/crew.py` to add your own logic, tools and specific args
- Modify `src/engineering_team/main.py` to add custom inputs for your agents and tasks

## Safe code execution prerequisite

The backend and test agents in `src/engineering_team/crew.py` use CrewAI's `allow_code_execution=True` with `code_execution_mode="safe"`. **Install and start Docker before running the crew**, and confirm the Docker daemon is available with `docker info`. These agents execute generated Python code in a Docker-backed environment; without a working Docker daemon, code-execution steps can fail even when the Gemini API key is configured. Review generated code before running it outside the sandbox.

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the engineering_team Crew, assembling the agents and assigning them tasks as defined in your configuration.

The current configuration runs an engineering workflow for a trading-simulation account module. It writes the design to `output/accounts.py_design.md`, the backend implementation to `output/accounts.py`, the Gradio prototype to `output/app.py`, and the generated tests to `output/test_accounts.py`. Generated code and tests should be reviewed and executed before use.

## Running tests

Run the repository's entry-point tests from the project root:

```bash
python -m pip install pytest
python -m pytest tests/test_main.py
```

These tests mock the AI crew and do not require Gemini credentials or Docker. To test the generated account implementation separately, review the generated files first, then run:

```bash
cd output
python -m pytest test_accounts.py
```

## Understanding Your Crew

The engineering_team Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the EngineeringTeam Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
