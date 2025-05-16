import streamlit as st
import requests
import json

FASTAPI_PROXY = "http://localhost:9000"

st.set_page_config(
    page_title="Travel Insurance Manager Agent (ADK Proxy)",
    page_icon="🤖",
    layout="wide"
)

st.title("Travel Insurance Manager Agent (via ADK Proxy)")
st.write("Ask anything about travel insurance. The manager agent will route your query to the right expert!")

# Get or cache a session ID
@st.cache_data
def get_session_id():
    sessions = requests.get(f"{FASTAPI_PROXY}/adk/sessions").json()
    if sessions:
        return sessions[0]["id"]
    else:
        st.error("No sessions found. Please start a session in your ADK backend.")
        st.stop()

session_id = get_session_id()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare payload for ADK proxy
    data = {
        "app_name": "manager_agent",
        "user_id": "user",
        "session_id": session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": prompt}]
        },
        "streaming": False  # Set to True if you want to handle streaming responses
    }

    # Send to FastAPI proxy
    response = requests.post(f"{FASTAPI_PROXY}/adk/run_sse", json=data, stream=True)
    agent_text = ""
    try:
        # Iterate over each line in the streaming response
        for line in response.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    json_str = decoded[6:]
                    try:
                        event = json.loads(json_str)
                        # Try to extract the text from the event
                        parts = event.get("content", {}).get("parts", [])
                        if parts:
                            # If it's a function call, skip, else show text
                            if "text" in parts[0]:
                                agent_text = parts[0]["text"]
                            elif "functionResponse" in parts[0]:
                                # Optionally handle functionResponse here
                                func_resp = parts[0]["functionResponse"]
                                if "response" in func_resp and "result" in func_resp["response"]:
                                    agent_text = func_resp["response"]["result"]
                    except Exception as e:
                        pass  # Ignore lines that aren't valid JSON
    except Exception as e:
        agent_text = f"Error: {e}\nRaw response: {response.text}"

    with st.chat_message("assistant"):
        st.markdown(agent_text)
    st.session_state.messages.append({"role": "assistant", "content": agent_text})
