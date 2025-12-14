"""Telemetry tools for accessing vehicle sensor data."""
import json
from pathlib import Path
from typing import Optional

# Path to data directory
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def get_vehicle_telemetry(vehicle_id: str) -> dict:
    """
    Retrieves the current real-time telemetry data for a specific vehicle.
    
    Args:
        vehicle_id: The unique identifier of the vehicle (e.g., 'VH001')
        
    Returns:
        dict: Current telemetry data including engine, battery, brakes, tyres, 
              and transmission status. Returns error if vehicle not found.
    """
    try:
        with open(DATA_DIR / "telemetry_stream.json", "r") as f:
            telemetry_data = json.load(f)
        
        if vehicle_id in telemetry_data:
            return {
                "status": "success",
                "data": telemetry_data[vehicle_id]
            }
        else:
            return {
                "status": "error",
                "error_message": f"No telemetry data found for vehicle {vehicle_id}"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve telemetry: {str(e)}"
        }


def get_sensor_history(vehicle_id: str, sensor_type: str, days: int = 7) -> dict:
    """
    Retrieves historical sensor readings for a specific sensor over a time period.
    
    Args:
        vehicle_id: The unique identifier of the vehicle
        sensor_type: Type of sensor (e.g., 'engine_temperature', 'battery_voltage', 
                     'brake_pad_wear', 'oil_pressure')
        days: Number of days of history to retrieve (default: 7)
        
    Returns:
        dict: Historical readings with timestamps and trend analysis
    """
    # Simulated historical data based on sensor type
    sensor_histories = {
        "engine_temperature": {
            "VH001": [88, 90, 91, 92, 91, 90, 92],
            "VH002": [95, 98, 100, 102, 103, 104, 105],
            "VH006": [100, 105, 108, 112, 115, 117, 118]
        },
        "battery_voltage": {
            "VH001": [12.6, 12.6, 12.5, 12.6, 12.6, 12.5, 12.6],
            "VH004": [12.2, 12.1, 12.0, 11.9, 11.9, 11.8, 11.8],
            "VH007": [12.9, 12.9, 12.8, 12.9, 12.9, 12.8, 12.9]
        },
        "brake_pad_wear": {
            "VH001": [65, 66, 67, 68, 69, 69, 70],
            "VH002": [78, 80, 81, 82, 83, 84, 85],
            "VH003": [12, 13, 13, 14, 14, 15, 15]
        },
        "oil_pressure": {
            "VH001": [36, 35, 35, 36, 35, 35, 35],
            "VH006": [28, 27, 26, 25, 24, 23, 22]
        }
    }
    
    try:
        if sensor_type in sensor_histories:
            history = sensor_histories[sensor_type].get(
                vehicle_id, 
                [50] * days  # Default values
            )
            
            # Calculate trend
            if len(history) >= 2:
                trend = "increasing" if history[-1] > history[0] else \
                        "decreasing" if history[-1] < history[0] else "stable"
                change_percent = ((history[-1] - history[0]) / history[0]) * 100 if history[0] != 0 else 0
            else:
                trend = "stable"
                change_percent = 0
            
            return {
                "status": "success",
                "vehicle_id": vehicle_id,
                "sensor_type": sensor_type,
                "readings": history[-days:],
                "trend": trend,
                "change_percent": round(change_percent, 2),
                "period_days": days
            }
        else:
            return {
                "status": "error",
                "error_message": f"Unknown sensor type: {sensor_type}"
            }
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Failed to retrieve sensor history: {str(e)}"
        }


def detect_anomalies(vehicle_id: str) -> dict:
    """
    Runs anomaly detection algorithms on all telemetry data for a vehicle.
    Identifies values outside normal operating ranges and patterns indicating
    potential failures.
    
    Args:
        vehicle_id: The unique identifier of the vehicle
        
    Returns:
        dict: List of detected anomalies with severity levels and recommendations
    """
    # Normal operating ranges for various sensors
    THRESHOLDS = {
        "engine_temperature": {"low": 70, "high": 100, "critical": 110},
        "oil_pressure": {"low": 25, "high": 65, "critical_low": 20},
        "oil_level": {"low": 50, "critical_low": 30},
        "coolant_temp": {"high": 100, "critical": 110},
        "coolant_level": {"low": 50, "critical_low": 30},
        "battery_voltage": {"low": 12.0, "critical_low": 11.5},
        "battery_health": {"low": 60, "critical_low": 40},
        "brake_pad_wear": {"high": 75, "critical": 85},
        "tyre_pressure": {"low": 28, "high": 36},
        "tread_depth": {"low": 3.0, "critical_low": 1.6}
    }
    
    try:
        with open(DATA_DIR / "telemetry_stream.json", "r") as f:
            telemetry_data = json.load(f)
        
        if vehicle_id not in telemetry_data:
            return {
                "status": "error",
                "error_message": f"No telemetry data found for vehicle {vehicle_id}"
            }
        
        vehicle_data = telemetry_data[vehicle_id]
        anomalies = []
        
        # Check engine parameters
        engine = vehicle_data.get("engine", {})
        if engine.get("temperature_celsius", 0) > THRESHOLDS["engine_temperature"]["critical"]:
            anomalies.append({
                "component": "engine",
                "issue": "engine_overheating",
                "severity": "critical",
                "current_value": engine["temperature_celsius"],
                "threshold": THRESHOLDS["engine_temperature"]["critical"],
                "recommendation": "Immediate inspection required. Do not drive vehicle."
            })
        elif engine.get("temperature_celsius", 0) > THRESHOLDS["engine_temperature"]["high"]:
            anomalies.append({
                "component": "engine",
                "issue": "engine_temperature_high",
                "severity": "warning",
                "current_value": engine["temperature_celsius"],
                "threshold": THRESHOLDS["engine_temperature"]["high"],
                "recommendation": "Schedule service within 1 week. Monitor coolant levels."
            })
        
        if engine.get("oil_pressure_psi", 50) < THRESHOLDS["oil_pressure"]["critical_low"]:
            anomalies.append({
                "component": "engine",
                "issue": "oil_pressure_critical",
                "severity": "critical",
                "current_value": engine["oil_pressure_psi"],
                "threshold": THRESHOLDS["oil_pressure"]["critical_low"],
                "recommendation": "Stop driving immediately. Engine damage risk."
            })
        
        if engine.get("coolant_level_percent", 100) < THRESHOLDS["coolant_level"]["critical_low"]:
            anomalies.append({
                "component": "cooling_system",
                "issue": "coolant_critical_low",
                "severity": "critical",
                "current_value": engine["coolant_level_percent"],
                "threshold": THRESHOLDS["coolant_level"]["critical_low"],
                "recommendation": "Top up coolant immediately. Check for leaks."
            })
        elif engine.get("coolant_level_percent", 100) < THRESHOLDS["coolant_level"]["low"]:
            anomalies.append({
                "component": "cooling_system",
                "issue": "coolant_low",
                "severity": "warning",
                "current_value": engine["coolant_level_percent"],
                "threshold": THRESHOLDS["coolant_level"]["low"],
                "recommendation": "Schedule coolant top-up within 1-2 days."
            })
        
        # Check battery
        battery = vehicle_data.get("battery", {})
        if battery.get("health_percent", 100) < THRESHOLDS["battery_health"]["critical_low"]:
            anomalies.append({
                "component": "battery",
                "issue": "battery_failure_imminent",
                "severity": "critical",
                "current_value": battery["health_percent"],
                "threshold": THRESHOLDS["battery_health"]["critical_low"],
                "recommendation": "Replace battery immediately. Risk of stranding."
            })
        elif battery.get("health_percent", 100) < THRESHOLDS["battery_health"]["low"]:
            anomalies.append({
                "component": "battery",
                "issue": "battery_degraded",
                "severity": "warning",
                "current_value": battery["health_percent"],
                "threshold": THRESHOLDS["battery_health"]["low"],
                "recommendation": "Plan battery replacement within 1 month."
            })
        
        # Check brakes
        brakes = vehicle_data.get("brakes", {})
        if brakes.get("front_pad_wear_percent", 0) > THRESHOLDS["brake_pad_wear"]["critical"]:
            anomalies.append({
                "component": "brakes",
                "issue": "brake_pad_worn_critical",
                "severity": "critical",
                "current_value": brakes["front_pad_wear_percent"],
                "threshold": THRESHOLDS["brake_pad_wear"]["critical"],
                "recommendation": "Replace brake pads immediately. Safety risk."
            })
        elif brakes.get("front_pad_wear_percent", 0) > THRESHOLDS["brake_pad_wear"]["high"]:
            anomalies.append({
                "component": "brakes",
                "issue": "brake_pad_wear_high",
                "severity": "warning",
                "current_value": brakes["front_pad_wear_percent"],
                "threshold": THRESHOLDS["brake_pad_wear"]["high"],
                "recommendation": "Schedule brake pad replacement within 2 weeks."
            })
        
        # Check tyres
        tyres = vehicle_data.get("tyres", {})
        if tyres.get("tread_depth_mm", 8) < THRESHOLDS["tread_depth"]["critical_low"]:
            anomalies.append({
                "component": "tyres",
                "issue": "tyre_tread_critical",
                "severity": "critical",
                "current_value": tyres["tread_depth_mm"],
                "threshold": THRESHOLDS["tread_depth"]["critical_low"],
                "recommendation": "Replace tyres immediately. Illegal and unsafe."
            })
        elif tyres.get("tread_depth_mm", 8) < THRESHOLDS["tread_depth"]["low"]:
            anomalies.append({
                "component": "tyres",
                "issue": "tyre_tread_low",
                "severity": "warning",
                "current_value": tyres["tread_depth_mm"],
                "threshold": THRESHOLDS["tread_depth"]["low"],
                "recommendation": "Plan tyre replacement within 1-2 months."
            })
        
        # Determine overall status
        if any(a["severity"] == "critical" for a in anomalies):
            overall_status = "critical"
        elif any(a["severity"] == "warning" for a in anomalies):
            overall_status = "warning"
        else:
            overall_status = "normal"
        
        return {
            "status": "success",
            "vehicle_id": vehicle_id,
            "overall_status": overall_status,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "last_checked": vehicle_data.get("timestamp", "Unknown")
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to run anomaly detection: {str(e)}"
        }


def get_all_vehicles_status() -> dict:
    """
    Retrieves a summary status of all vehicles in the fleet.
    Useful for dashboard overview and prioritizing which vehicles need attention.
    
    Returns:
        dict: List of all vehicles with their current health status
    """
    try:
        with open(DATA_DIR / "telemetry_stream.json", "r") as f:
            telemetry_data = json.load(f)
        
        with open(DATA_DIR / "vehicles.json", "r") as f:
            vehicles = json.load(f)
        
        vehicle_statuses = []
        for vehicle in vehicles:
            vehicle_id = vehicle["vehicle_id"]
            telemetry = telemetry_data.get(vehicle_id, {})
            
            vehicle_statuses.append({
                "vehicle_id": vehicle_id,
                "make": vehicle["make"],
                "model": vehicle["model"],
                "owner_name": vehicle["owner"]["name"],
                "city": vehicle["owner"]["city"],
                "status": telemetry.get("status", "unknown"),
                "alerts": telemetry.get("alerts", [])
            })
        
        # Sort by severity (critical first, then warning, then normal)
        severity_order = {"critical": 0, "warning": 1, "normal": 2, "excellent": 3, "unknown": 4}
        vehicle_statuses.sort(key=lambda x: severity_order.get(x["status"], 4))
        
        return {
            "status": "success",
            "total_vehicles": len(vehicle_statuses),
            "critical_count": sum(1 for v in vehicle_statuses if v["status"] == "critical"),
            "warning_count": sum(1 for v in vehicle_statuses if v["status"] == "warning"),
            "normal_count": sum(1 for v in vehicle_statuses if v["status"] in ["normal", "excellent"]),
            "vehicles": vehicle_statuses
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve fleet status: {str(e)}"
        }
