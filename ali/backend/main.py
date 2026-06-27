from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simulator import DataSimulator
from agents import DataAgent, ModelAgent, APIAgent, AlertAgent
from risk_engine import PropagationRiskAgent
from engine.phase6_engine import Phase6Engine
from state_manager import SystemStateManager

app = FastAPI()

# ===============================
# Initialize Core Components
# ===============================

engine = Phase6Engine()
state_manager = SystemStateManager()
simulator = DataSimulator(state_manager)

data_agent = DataAgent()
model_agent = ModelAgent()
api_agent = APIAgent()
cascade_agent = PropagationRiskAgent()
alert_agent = AlertAgent()

logs = []

# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# MAIN METRICS ENDPOINT
# ===============================

@app.get("/metrics")
def get_metrics():

    # --- Phase 6 Synthetic Drift Engine ---
    current_data = engine.generate_data()
    risk_math = engine.compute_risk(current_data)

    # --- Keep simulator for phase tracking ---
    df = simulator.get_data()

    # --- Use Phase 6 risk outputs ---
    data_risk = risk_math["data_risk"]
    model_risk = risk_math["model_risk"]
    api_risk = risk_math["api_risk"]
    cascade_risk = risk_math["cascade_risk"]

    # --- Reasons (Explainability) ---
    data_reason = f"Z-score={risk_math['z_score']:.2f}, KL={risk_math['kl_divergence']:.4f}"
    model_reason = "Amplified from Data Risk (×1.2)"
    api_reason = "Amplified from Model Risk (×1.15)"
    cascade_reason = "Weighted multi-agent cascade aggregation"

    # --- Dynamic Threshold ---
    threshold = risk_math["threshold"]
    safety_margin = risk_math["safety_margin"]

    # --- Adaptive Alert Logic ---
    if safety_margin < 0:
        alert = "CASCADE FAILURE"
    elif safety_margin < 5:
        alert = "CRITICAL"
    elif safety_margin < 20:
        alert = "WARNING"
    else:
        alert = "SAFE"

    # --- Logging ---
    log_entry = {
        "data": data_reason,
        "model": model_reason,
        "api": api_reason,
        "cascade": cascade_reason,
        "phase": state_manager.phase,
        "alert": alert
    }

    logs.append(log_entry)

    # --- Full Response for Frontend Math Panel ---
    return {
        "phase": state_manager.phase,

        "data_risk": data_risk,
        "model_risk": model_risk,
        "api_risk": api_risk,
        "cascade_risk": cascade_risk,

        "baseline_mean": risk_math["baseline_mean"],
        "baseline_std": risk_math["baseline_std"],
        "current_mean": risk_math["current_mean"],
        "current_std": risk_math["current_std"],

        "z_score": risk_math["z_score"],
        "kl_divergence": risk_math["kl_divergence"],

        "threshold": threshold,
        "safety_margin": safety_margin,

        "alert": alert
    }

# ===============================
# Drift Injection Endpoint
# ===============================

@app.post("/inject_drift/{drift_type}")
def inject_drift(drift_type: str):
    engine.inject_drift(drift_type)
    return {"status": f"{drift_type} injected"}

# ===============================
# Logs
# ===============================

@app.get("/logs")
def get_logs():
    return logs[-20:]

# ===============================
# System State
# ===============================

@app.get("/system_state")
def get_state():
    return {
        "phase": state_manager.phase
    }