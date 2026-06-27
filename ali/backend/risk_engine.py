class PropagationRiskAgent:
    def __init__(self):
        self.memory = 0

    def compute(self, data_risk, model_risk, api_risk):
        # Time-weighted propagation memory
        self.memory = 0.7 * self.memory + 0.3 * (
            0.4 * data_risk +
            0.35 * model_risk +
            0.25 * api_risk
        )

        cascade = self.memory

        # Amplification logic
        if data_risk > 60:
            cascade *= 1.15

        if model_risk > 70:
            cascade *= 1.25

        cascade = min(100, cascade)

        reason = {
            "memory": round(self.memory, 2),
            "final_cascade": round(cascade, 2)
        }

        return cascade, reason