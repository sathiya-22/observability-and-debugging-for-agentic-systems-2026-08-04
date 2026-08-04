import time
import random
from agent_logger import AgentLogger

# Initialize the logger
logger = AgentLogger()

def run_example_agent(agent_id: str):
    """
    Simulates an agent's lifecycle, generating various log events.
    """
    print(f"\n--- Starting Agent: {agent_id} ---")

    # 1. Agent Initialization
    config = {"model": "gemini-pro", "temperature": 0.7, "max_tokens": 500}
    logger.agent_initialized(agent_id, config)
    time.sleep(0.5)

    # 2. Planning Step
    step_name = "planning_phase"
    logger.step_started(agent_id, step_name, {"goal": "research_topic", "topic": "AI Observability"})
    time.sleep(random.uniform(0.5, 1.5))
    logger.state_updated(agent_id, step_name, {"current_plan": ["search_web", "summarize_results", "generate_report"]})
    time.sleep(0.5)
    logger.step_completed(agent_id, step_name, {"plan_generated": True, "num_steps": 3})

    # Introduce a potential failure point
    if random.random() < 0.2: # 20% chance of planning failure
        error_msg = "Failed to generate a coherent plan due to ambiguous query."
        logger.step_failed(agent_id, step_name, error_msg, "Traceback: ... (simulated)")
        logger.agent_exited(agent_id, reason="planning_failure")
        print(f"--- Agent {agent_id} exited due to planning failure ---")
        return

    # 3. Execution Step: Tool Calling
    step_name = "execution_phase_search"
    logger.step_started(agent_id, step_name, {"query": "best practices for agentic AI observability"})
    time.sleep(random.uniform(0.5, 1.0))

    # Simulate tool call
    tool_name = "web_search_tool"
    tool_args = {"query": "agentic AI observability best practices"}
    logger.tool_called(agent_id, step_name, tool_name, tool_args)
    time.sleep(random.uniform(1.0, 2.0))

    if random.random() < 0.15: # 15% chance of tool failure
        error_msg = "Web search tool timed out."
        logger.tool_response(agent_id, step_name, tool_name, {"status": "error", "message": error_msg})
        logger.step_failed(agent_id, step_name, error_msg)
        logger.agent_exited(agent_id, reason="tool_failure")
        print(f"--- Agent {agent_id} exited due to tool failure ---")
        return

    tool_response_data = {"results": [{"title": "Doc1", "url": "url1"}, {"title": "Doc2", "url": "url2"}], "count": 2}
    logger.tool_response(agent_id, step_name, tool_name, tool_response_data)
    logger.state_updated(agent_id, step_name, {"search_results": tool_response_data})
    logger.step_completed(agent_id, step_name, {"search_success": True, "num_results": 2})

    # 4. Analysis Step
    step_name = "analysis_phase"
    logger.step_started(agent_id, step_name, {"data_to_analyze": tool_response_data})
    time.sleep(random.uniform(0.5, 1.0))
    analysis_result = {"summary": "Key insights from search results...", "sentiment": "positive"}
    logger.state_updated(agent_id, step_name, {"analysis_output": analysis_result})
    logger.step_completed(agent_id, step_name, {"analysis_success": True, "report_snippet": analysis_result["summary"][:20]})

    # 5. Final Report Generation
    step_name = "report_generation_phase"
    logger.step_started(agent_id, step_name, {"final_data": analysis_result})
    time.sleep(random.uniform(0.5, 1.0))
    final_report = {"title": "Observability Report", "content": "Full report content..."}
    logger.step_completed(agent_id, step_name, {"report_path": "/tmp/report.pdf", "report_size_kb": 120})

    # 6. Agent Exit
    logger.agent_exited(agent_id, reason="success")
    print(f"--- Agent {agent_id} completed successfully ---")


if __name__ == "__main__":
    # Run multiple agents concurrently or sequentially to demonstrate distinct logs
    print("Generating agent logs...")
    for i in range(3):
        agent_id = f"Agent-{i+1}"
        run_example_agent(agent_id)
        time.sleep(random.uniform(1, 3)) # Simulate time between agent runs

    print("\nFinished generating example agent logs.")
    print("View logs at http://127.0.0.1:5000 (if the Flask app is running)")
