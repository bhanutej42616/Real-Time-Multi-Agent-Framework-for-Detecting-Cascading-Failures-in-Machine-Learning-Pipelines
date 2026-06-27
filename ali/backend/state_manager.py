import time

class SystemStateManager:
    def __init__(self):
        self.start_time = time.time()
        self.phase = "normal"

    def update_phase(self):
        elapsed = int(time.time() - self.start_time)

        # Controlled lifecycle (loops every 120 sec)
        cycle = elapsed % 120

        if cycle < 20:
            self.phase = "normal"
        elif cycle < 40:
            self.phase = "drift"
        elif cycle < 60:
            self.phase = "model_degradation"
        elif cycle < 80:
            self.phase = "api_instability"
        elif cycle < 100:
            self.phase = "cascade"
        else:
            self.phase = "recovery"

        return self.phase