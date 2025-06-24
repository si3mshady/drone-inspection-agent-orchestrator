from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.agents import Agent
from agent_tools import launch_gazebo, start_qgc, start_mission
from mission_code_agent import mission_code_agent
#test11

class Prompt(BaseModel):
    user_input: str
    waypoints: list[dict] = []  # optional list of waypoints for mission generation

app = FastAPI()

roof_agent = Agent(
    name="roof_inspection_agent",
    model="gemini-2.0-pro",
    description="Orchestrates drone inspection simulations.",
    instruction="You are the overseer of a drone mission. You handle launching tools and request mission code from another agent.",
    tools=[launch_gazebo, start_qgc],
)

@app.post("/inspect")
async def handle_inspection(prompt: Prompt):
    # Handle Gazebo/QGC steps
    roof_agent(prompt.user_input)

    # Generate mission code using separate code agent
    mission_code = mission_code_agent.tools[0](prompt.waypoints)

    # Run mission
    mission_result = start_mission(mission_code)

    return {"status": "completed", "mission_result": mission_result}
