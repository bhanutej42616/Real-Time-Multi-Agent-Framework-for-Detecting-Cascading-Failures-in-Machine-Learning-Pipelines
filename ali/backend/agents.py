import numpy as np

class DataAgent:
    def analyze(self, df):
        drift = abs(df["feature1"].mean() - 50)
        outliers = np.sum(df["feature1"] > 75)

        risk = min(100, drift * 3 + outliers / 40)

        reason = {
            "drift": round(drift, 2),
            "outliers": int(outliers),
            "risk": round(risk, 2)
        }

        return risk, reason


class ModelAgent:
    def analyze(self, data_risk, memory_factor):
        degradation = data_risk * 0.5 + memory_factor * 0.3
        confidence_drop = degradation * 0.8

        risk = min(100, degradation + confidence_drop)

        reason = {
            "degradation": round(degradation, 2),
            "confidence_drop": round(confidence_drop, 2),
            "risk": round(risk, 2)
        }

        return risk, reason


class APIAgent:
    def analyze(self, model_risk, memory_factor):
        latency_growth = model_risk * 2
        instability = latency_growth * 0.4 + memory_factor * 0.5

        risk = min(100, instability)

        reason = {
            "latency_growth": round(latency_growth, 2),
            "instability": round(instability, 2),
            "risk": round(risk, 2)
        }

        return risk, reason


class AlertAgent:
    def evaluate(self, cascade_risk):
        if cascade_risk < 25:
            return "Safe"
        elif cascade_risk < 50:
            return "Warning"
        elif cascade_risk < 75:
            return "High Risk"
        else:
            return "Critical Cascade"