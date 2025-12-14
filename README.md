# 🚗 AutoPilot - Autonomous Predictive Maintenance System

An agentic AI solution for automotive predictive maintenance using Google ADK (Agent Development Kit). A Master Agent orchestrates 13 specialized worker agents to handle end-to-end vehicle maintenance prediction, customer engagement, service scheduling, and manufacturing quality feedback.

## 🎯 Features

- **Predictive Maintenance**: Analyze real-time vehicle telemetry to predict failures before they occur
- **Autonomous Scheduling**: Proactively schedule service appointments with customer consent
- **Voice-First Interface**: In-car voice assistant for driver communication
- **RCA/CAPA Analysis**: Manufacturing feedback loop for quality improvement
- **UEBA Security**: Behavior analytics monitoring all agent interactions

## 📁 Project Structure

```
predictive_maintenance/
├── __init__.py
├── agent.py                      # Master Agent (Orchestrator)
├── agents/                       # 13 Worker Agents
│   ├── data_analysis.py          # Telemetry analysis
│   ├── diagnosis.py              # Failure prediction
│   ├── customer_outreach.py      # Voice contact initiation
│   ├── customer_engagement.py    # Issue explanation & consent
│   ├── scheduling.py             # Appointment booking
│   ├── logistics.py              # Parts management
│   ├── technician_matcher.py     # Skill-based assignment
│   ├── emergency_response.py     # Critical failure handling
│   ├── feedback.py               # Post-service collection
│   ├── forecasting.py            # Demand prediction
│   ├── manufacturing_insights.py # RCA/CAPA analysis
│   ├── model_retraining.py       # Continuous learning
│   └── ueba_security.py          # Security monitoring
├── tools/                        # Agent Tools
│   ├── telemetry_tools.py
│   ├── database_tools.py
│   ├── scheduling_tools.py
│   └── notification_tools.py
data/                             # Mock Data
├── vehicles.json                 # 10 vehicles
├── maintenance_history.json
├── telemetry_stream.json
├── service_centers.json
└── capa_records.json
dashboard/                        # Web Dashboard
├── index.html
├── styles.css
└── app.js
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Install packages
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your Google API key
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the Agent

```bash
# Run with ADK CLI
adk run predictive_maintenance

# Or use the web interface
adk web predictive_maintenance
```

### 4. View the Dashboard

```bash
cd dashboard
python -m http.server 8080
# Open http://localhost:8080
```

## 🤖 Agent Architecture

```
                    ┌─────────────────────────┐
                    │     Master Agent        │
                    │    (Orchestrator)       │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────▼───────┐       ┌───────▼───────┐       ┌───────▼───────┐
│  Detection &  │       │   Customer    │       │    Service    │
│  Diagnosis    │       │  Interaction  │       │  Preparation  │
├───────────────┤       ├───────────────┤       ├───────────────┤
│ Data Analysis │       │   Outreach    │       │   Logistics   │
│   Diagnosis   │       │  Engagement   │       │   Technician  │
└───────────────┘       │  Scheduling   │       │   Matcher     │
                        └───────────────┘       └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Background Agents   │
                    ├───────────────────────┤
                    │ Emergency Response    │
                    │ Feedback Collection   │
                    │ Forecasting           │
                    │ Manufacturing Insights│
                    │ Model Retraining      │
                    │ UEBA Security         │
                    └───────────────────────┘
```

## 💬 Example Interactions

### Analyze a Vehicle

```
User: Analyze vehicle VH002

Master Agent: I'll analyze the telemetry for VH002...
[Delegates to data_analysis_agent]

Result: Vehicle VH002 (Mahindra XUV700) shows WARNING status:
- Engine temperature: 105°C (HIGH)
- Coolant level: 60% (LOW)
- Brake pad wear: 85% (HIGH)

Recommendation: Schedule service within 1-3 days.
```

### Emergency Scenario

```
User: Vehicle VH006 has critical engine overheating

Master Agent: This is a critical safety issue. Activating Emergency Response...
[Delegates to emergency_response_agent]

🚨 EMERGENCY ALERT sent to owner:
"Your vehicle has detected engine overheating at 118°C. 
Please pull over safely. Finding nearest service center..."

[Coordinates immediate service booking]
```

### Manufacturing Report

```
User: Generate quality insights report

Master Agent: Generating RCA/CAPA analysis...
[Delegates to manufacturing_insights_agent]

## Quality Insight Report

### Top Issues:
1. Brake pad wear (XUV700, Scorpio-N) - 287 affected vehicles
2. Battery degradation (Creta, Venue) - 423 affected vehicles
3. Coolant leaks (XUV700, Thar) - 156 affected vehicles

### Recommendations:
- Update brake pad compound formula
- Enhance battery thermal management
- Revise coolant hose clamp specifications
```

## 🔒 UEBA Security

The UEBA agent monitors all agent activities:

- **Baseline Behavior**: Each agent has defined normal operations
- **Anomaly Detection**: Flags unusual tool access or data queries
- **Risk Scoring**: 0-10 scale for activity risk assessment
- **Policy Enforcement**: Blocks unauthorized actions

Example Alert:
```
⚠️ ANOMALY DETECTED
Agent: scheduling_agent
Action: Attempted to access telemetry data
Risk Score: 7/10
Status: FLAGGED for review
```

## 📊 Dashboard Views

1. **Owner View**: Vehicle health, alerts, telemetry, service history
2. **Service Center View**: Bookings, technician assignments, inventory
3. **Manufacturer View**: RCA/CAPA insights, defect trends, quality metrics
4. **Fleet View**: All vehicles status at a glance
5. **Agent Logs**: UEBA-monitored agent activity

## 🛠️ Tech Stack

- **Agent Framework**: Google ADK
- **LLM**: Gemini 2.5 Flash
- **Backend**: Python 3.10+
- **Dashboard**: HTML/CSS/JavaScript
- **Data**: JSON (mock)

## 📝 License

MIT License - See LICENSE file for details.

---

Built for EY Hackathon - Autonomous Predictive Maintenance Challenge
