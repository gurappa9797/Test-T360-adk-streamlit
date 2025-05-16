from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents import (
    refund_agent, payment_agent, vetting_agent, coverage_agent, flight_agent,
    explore_plans_agent, purchase_plan_agent, claim_agent, cancel_agent
)
import requests

# Define the root agent that routes to specialized sub-agents
root_agent = Agent(
    name="manager_agent",
    model="gemini-2.5-pro-preview-03-25",
    description="Manager agent for travel insurance system",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.
    Always delegate the task to the appropriate agent. Use your best judgement to determine which agent to delegate to.
    You are responsible for delegating tasks to the following agents:
    - vetting_agent: For checking eligibility and user verification
    - coverage_agent: For insurance plan and coverage details
    - payment_agent: For payment processing
    - refund_agent: For refund processing
    - flight_agent: For flight search and booking
    - explore_plans_agent: For plan exploration and comparison
    - purchase_plan_agent: For plan purchase facilitation
    - claim_agent: For insurance claim management
    - cancel_agent: For plan cancellation and refund guidance

    When a user asks a question:
    1. Analyze the intent of the question
    2. Determine which agent is best suited to handle it
    3. Delegate the task to that agent
    4. Return the response to the user

    Always maintain a professional and helpful tone.
    """,
    tools=[
        AgentTool(vetting_agent),
        AgentTool(coverage_agent),
        AgentTool(payment_agent),
        AgentTool(refund_agent),
        AgentTool(flight_agent),
        AgentTool(explore_plans_agent),
        AgentTool(purchase_plan_agent),
        AgentTool(claim_agent),
        AgentTool(cancel_agent)
    ]
)

# Expose root_agent as agent attribute for ADK framework
agent = root_agent

# Expose sub-agents for direct use
__all__ = [
    "root_agent", "vetting_agent", "coverage_agent", "payment_agent", "refund_agent", "flight_agent",
    "explore_plans_agent", "purchase_plan_agent", "claim_agent", "cancel_agent"
]

# Get all sessions
sessions = requests.get("http://localhost:9000/adk/sessions").json()
# Use the first session's ID (or pick based on your logic)
session_id = sessions[0]["id"]
print("Session ID:", session_id)

# Use the session_id from the previous step
session_id = "your-session-id-here"  # Replace with the one you got

data = {
    "app_name": "manager_agent",
    "user_id": "user",
    "session_id": session_id,
    "new_message": {
        "role": "user",
        "parts": [{"text": "YOUR CUSTOM MESSAGE HERE"}]
    },
    "streaming": True
}

response = requests.post("http://localhost:9000/adk/run_sse", json=data)
print(response.text)