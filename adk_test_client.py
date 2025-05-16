import requests

# Step 1: Get all sessions
sessions = requests.get("http://localhost:9000/adk/sessions").json()
session_id = sessions[0]["id"]  # Or select based on your needs

# Step 2: Send a message
data = {
    "app_name": "manager_agent",
    "user_id": "user",
    "session_id": session_id,
    "new_message": {
        "role": "user",
        "parts": [{"text": "What are the available claims?"}]
    },
    "streaming": True
}

response = requests.post("http://localhost:9000/adk/run_sse", json=data)
print(response.text)