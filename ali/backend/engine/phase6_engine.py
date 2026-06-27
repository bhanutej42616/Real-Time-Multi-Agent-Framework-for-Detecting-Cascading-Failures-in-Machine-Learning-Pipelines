import numpy as np
from scipy.stats import entropy

class Phase6Engine:
    def __init__(self):
        # =========================
        # Baseline Distribution
        # =========================
        self.baseline_data = np.random.normal(50, 5, 500)
        self.baseline_mean = np.mean(self.baseline_data)
        self.baseline_std = np.std(self.baseline_data)

        self.current_mean = self.baseline_mean
        self.current_std = self.baseline_std

        self.drift_mode = None
        self.drift_timer = 0

        # Store previous risks for adaptive threshold
        self.risk_history = []

    # =========================
    # KL Divergence
    # =========================
    def compute_kl_divergence(self, current_data):
        hist_base, bins = np.histogram(self.baseline_data, bins=30, density=True)
        hist_curr, _ = np.histogram(current_data, bins=bins, density=True)

        hist_base += 1e-8
        hist_curr += 1e-8

        return entropy(hist_base, hist_curr)

    # =========================
    # Drift Injection
    # =========================
    def inject_drift(self, drift_type):
        self.drift_mode = drift_type
        self.drift_timer = 50

    # =========================
    # Data Generation
    # =========================
    def generate_data(self):
        if self.drift_mode == "mean_shift":
            self.current_mean += 0.5

        elif self.drift_mode == "variance_explosion":
            self.current_std *= 1.05

        elif self.drift_mode == "sudden_shock":
            shock = np.random.normal(100, 20, 100)
            return shock

        elif self.drift_mode == "gradual_drift":
            self.current_mean += 0.1

        # Auto recovery
        if self.drift_timer > 0:
            self.drift_timer -= 1
        else:
            self.current_mean += (self.baseline_mean - self.current_mean) * 0.05
            self.current_std += (self.baseline_std - self.current_std) * 0.05

        return np.random.normal(self.current_mean, self.current_std, 100)

    # =========================
    # Risk Calculation
    # =========================
    def compute_risk(self, current_data):

        mean = np.mean(current_data)
        std = np.std(current_data)

        # -------------------------
        # Statistical Drift Measures
        # -------------------------
        z_score = abs((mean - self.baseline_mean) / self.baseline_std)
        kl = self.compute_kl_divergence(current_data)

        # -------------------------
        # Normalized Data Risk (Sigmoid Scaling)
        # -------------------------
        raw_risk = (z_score * 2) + (kl * 5)

        data_risk = 100 * (1 / (1 + np.exp(-raw_risk)))

        # -------------------------
        # Propagation Logic
        # -------------------------
        model_risk = min(data_risk * 1.1, 100)
        api_risk = min(model_risk * 1.05, 100)

        cascade_risk = (
            data_risk * 0.4 +
            model_risk * 0.3 +
            api_risk * 0.3
        )

        # -------------------------
        # Adaptive Threshold
        # -------------------------
        self.risk_history.append(cascade_risk)

        if len(self.risk_history) > 100:
            self.risk_history.pop(0)

        if len(self.risk_history) > 10:
            dynamic_threshold = np.percentile(self.risk_history, 85)
        else:
            dynamic_threshold = 75  # Default threshold

        safety_margin = dynamic_threshold - cascade_risk

        return {
            "baseline_mean": self.baseline_mean,
            "baseline_std": self.baseline_std,
            "current_mean": mean,
            "current_std": std,
            "z_score": z_score,
            "kl_divergence": kl,
            "data_risk": round(data_risk, 2),
            "model_risk": round(model_risk, 2),
            "api_risk": round(api_risk, 2),
            "cascade_risk": round(cascade_risk, 2),
            "threshold": round(dynamic_threshold, 2),
            "safety_margin": round(safety_margin, 2)
        }