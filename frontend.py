import streamlit as st
import requests
import time
import json

#test2

st.set_page_config(page_title="Roof Inspection Dashboard", layout="wide")

# Sidebar - User Input
st.sidebar.title("📝 Mission Input")
st.sidebar.markdown("Enter your inspection mission parameters below.")
waypoints_input = st.sidebar.text_area("Waypoints JSON", '[{"lat": 37.7749, "lon": -122.4194, "alt": 15}]')
start_button = st.sidebar.button("🛰️ Start Mission")

# Main Dashboard
st.title("🏠 Autonomous Roof Inspection Dashboard")

# --- Workflow Status Table --- #
st.subheader("📋 Workflow Status")
workflow_steps = [
    ("Customer Request", "CRM, email, phone", "Inspection scheduled"),
    ("Pre-Flight Planning", "QGroundControl", "Automated mission ready"),
    ("On-Site Setup", "PX4 drone, QGC", "Safe launch area, system check"),
    ("Automated Flight", "PX4, QGroundControl", "Geo-tagged roof images"),
    ("Data Processing", "WebODM", "2D map, 3D model"),
    ("Analysis", "QGIS (+ plugins)", "Measurements, annotations, defect find"),
    ("Report Generation", "QGIS, PDF tool", "Professional inspection report"),
    ("Delivery", "Email/cloud", "Results to customer")
]

st.table({
    "Step": [s[0] for s in workflow_steps],
    "Tool/Software": [s[1] for s in workflow_steps],
    "Output/Goal": [s[2] for s in workflow_steps]
})

# --- System Status Panel --- #
st.subheader("📡 System Status")
cols = st.columns(4)
system_status = {
    "Gazebo": "🟢 Online",
    "QGroundControl": "🟢 Connected",
    "MAVLink": "🟡 Awaiting Mission",
    "ROS2": "🟢 Active"
}

for i, (component, status) in enumerate(system_status.items()):
    with cols[i]:
        st.metric(label=component, value=status)

# --- Mission Control --- #
st.subheader("🚀 Mission Execution")
if start_button:
    try:
        waypoints = json.loads(waypoints_input)
        with st.spinner("Sending mission to backend agent..."):
            res = requests.post("http://localhost:8000/inspect", json={
                "user_input": "run roof inspection",
                "waypoints": waypoints
            })
        if res.status_code == 200:
            st.success("✅ Mission Started")
            st.json(res.json())
        else:
            st.error("❌ Failed to start mission")
    except Exception as e:
        st.error(f"Invalid JSON input or request failed: {e}")

# --- Agent Console Logs --- #
st.subheader("🧠 Agent Logs")
log_placeholder = st.empty()

# Optional: You can update this to poll from a /logs endpoint if available
example_logs = """
>> Agent initialized: roof_inspection_agent
>> Request received: run roof inspection
>> Invoking mission_code_agent...
>> Waypoints parsed: 3
>> start_mission.py written
>> Executing mission...
>> RTL command issued
"""
log_placeholder.code(example_logs, language="bash")
