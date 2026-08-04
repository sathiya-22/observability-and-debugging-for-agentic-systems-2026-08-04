import json
import time
import os
from datetime import datetime

class AgentLogger:
    """
    A structured logger for agentic systems.
    Logs events to a specified file in JSON format, facilitating easy parsing
    and analysis for debugging and observability.
    """
    def __init__(self, log_file="agent_events.log"):
        self.log_file = log_file
        # Ensure the log file is cleared on initialization for a clean run
        if os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("") # Clear file

    def _log_event(self, event_type: str, agent_id: str, step: str, payload: dict = None):
        """
        Internal method to write a structured event to the log file.
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "step": step,
            "event_type": event_type,
            "payload": payload if payload is not None else {}
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + "\n")
        print(f"Logged: {event_type} for Agent {agent_id} at Step {step}")

    def agent_initialized(self, agent_id: str, config: dict):
        """Logs when an agent is initialized."""
        self._log_event("AGENT_INITIALIZED", agent_id, "init", {"config": config})

    def step_started(self, agent_id: str, step_name: str, inputs: dict):
        """Logs when a specific step in the agent's process starts."""
        self._log_event("STEP_STARTED", agent_id, step_name, {"inputs": inputs})

    def step_completed(self, agent_id: str, step_name: str, outputs: dict):
        """Logs when a specific step in the agent's process completes successfully."""
        self._log_event("STEP_COMPLETED", agent_id, step_name, {"outputs": outputs})

    def step_failed(self, agent_id: str, step_name: str, error: str, traceback: str = None):
        """Logs when a specific step in the agent's process fails."""
        self._log_event("STEP_FAILED", agent_id, step_name, {"error": error, "traceback": traceback})

    def state_updated(self, agent_id: str, step_name: str, new_state: dict):
        """Logs a significant update to the agent's internal state."""
        self._log_event("STATE_UPDATED", agent_id, step_name, {"new_state": new_state})

    def tool_called(self, agent_id: str, step_name: str, tool_name: str, tool_args: dict):
        """Logs when an agent calls an external tool."""
        self._log_event("TOOL_CALLED", agent_id, step_name, {"tool_name": tool_name, "tool_args": tool_args})

    def tool_response(self, agent_id: str, step_name: str, tool_name: str, response: any):
        """Logs the response received from an external tool."""
        self._log_event("TOOL_RESPONSE", agent_id, step_name, {"tool_name": tool_name, "response": response})

    def agent_exited(self, agent_id: str, reason: str = "completed"):
        """Logs when an agent process exits, either successfully or due to an error."""
        self._log_event("AGENT_EXITED", agent_id, "exit", {"reason": reason})
