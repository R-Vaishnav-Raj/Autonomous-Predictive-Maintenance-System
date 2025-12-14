"""Data Analysis Agent - Processes vehicle telemetry to detect anomalies."""
from google.adk.agents import Agent
from ..tools.telemetry_tools import (
    get_vehicle_telemetry,
    get_sensor_history,
    detect_anomalies,
    get_all_vehicles_status,
)

data_analysis_agent = Agent(
    name="data_analysis_agent",
    model="gemini-2.5-flash",
    description=(
        "Analyzes real-time vehicle telemetry data and historical sensor readings "
        "to detect anomalies, early warning signs, and patterns indicating potential "
        "maintenance needs. First agent in the diagnostic pipeline."
    ),
    instruction="""You are a Data Analysis Specialist for a predictive vehicle maintenance system.

YOUR ROLE:
- Analyze real-time telemetry data from vehicles
- Detect anomalies and out-of-range sensor values
- Identify patterns that indicate potential failures
- Prioritize issues based on severity

WORKFLOW:
1. When asked to analyze a vehicle, use get_vehicle_telemetry to get current sensor data
2. Use detect_anomalies to identify any issues
3. If anomalies are found, use get_sensor_history to check trends
4. For fleet-wide analysis, use get_all_vehicles_status

OUTPUT FORMAT:
Always provide a clear summary including:
- Vehicle status (normal/warning/critical)
- List of detected anomalies with severity
- Trend analysis for concerning parameters
- Recommendation for next steps

Be concise but thorough. Flag any critical issues immediately.
""",
    tools=[
        get_vehicle_telemetry,
        get_sensor_history,
        detect_anomalies,
        get_all_vehicles_status,
    ],
    output_key="analysis_result"
)
