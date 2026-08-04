Observability and Debugging for Agentic Systems

**The Real Problem:**
Developers building agentic AI systems face significant challenges in understanding and debugging their agents' behavior. Unlike traditional applications, agents exhibit complex, non-deterministic interactions, making it hard to trace execution paths, inspect internal state, and diagnose issues stemming from initialization failures, unexpected state transitions, or process exits. Existing logging tools often lack the context-rich, structured data needed to effectively debug multi-step, multi-component agentic workflows. This leads to extended debugging cycles and reduced confidence in agent reliability.

**Why this project shape/stack was chosen:**
This prototype provides a lightweight, structured logging utility and a simple web-based viewer.
*   **Python Package:** Python is the de-facto standard for agentic AI development, making a Python package the most accessible and natural fit for developers.
*   **Structured Logging:** Instead of plain text, we capture events as JSON objects, allowing for easy parsing, filtering, and analysis. Each event includes critical metadata like agent ID, step, event type, and timestamp.
*   **Web Viewer (Flask):** A simple Flask application provides a local, real-time viewer for these structured logs. This allows developers to quickly visualize the flow of events, filter by agent, and inspect the state at different points, offering a much-needed "glass box" view into their agents. Flask is chosen for its simplicity and minimal setup, making it easy to integrate and run locally alongside agent development.
*   **No LLM Involvement:** The problem is pure observability infrastructure. LLMs are the *target* of observation, not a component *of* the observation system itself. The system is designed to capture agent events, regardless of whether those events involve LLM calls or other tool interactions.

**Setup and Usage Instructions (Zero API Keys):**

1.  **Clone the repository:**
    `git clone <repository-url>`
    `cd <repository-directory>`

2.  **Create a virtual environment and install dependencies:**
    `python -m venv venv`
    `source venv/bin/activate` (on Linux/macOS) or `venv\Scripts\activate` (on Windows)
    `pip install -r requirements.txt`

3.  **Run the log viewer:**
    `python app.py`
    The viewer will be accessible at `http://127.0.0.1:5000` in your browser. Initially, it will show no logs.

4.  **Run the example agent (which generates logs):**
    Open a *new* terminal window (keeping the `app.py` process running in the first one).
    Activate the virtual environment:
    `source venv/bin/activate` (on Linux/macOS) or `venv\Scripts\activate` (on Windows)
    Run the example agent:
    `python example_agent.py`

    As `example_agent.py` runs, you will see its events appear in real-time in your browser at `http://127.0.0.1:5000`. You can refresh the page or watch for new events.

**Optional Real-LLM Adapter:**
No LLM adapter is provided or required, as this tool focuses solely on the infrastructure for observing agent behavior, not on interacting with LLMs directly. The events logged by the agent could *include* details of LLM interactions (e.g., prompt, response, token usage), but the logging system itself is LLM-agnostic.
