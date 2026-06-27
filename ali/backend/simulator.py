import numpy as np
import pandas as pd
import threading
import time
from datetime import datetime

class DataSimulator:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.data = pd.DataFrame()
        self.lock = threading.Lock()
        self.running = True
        self._generate_initial_data()
        threading.Thread(target=self._stream, daemon=True).start()

    def _generate_initial_data(self):
        timestamps = pd.date_range(
            end=datetime.now(),
            periods=50000,
            freq='s'
        )

        self.data = pd.DataFrame({
            "timestamp": timestamps,
            "feature1": np.random.normal(50, 5, 50000),
            "feature2": np.random.normal(30, 3, 50000)
        })

    def _stream(self):
        drift_shift = 0

        while self.running:
            time.sleep(2)
            phase = self.state_manager.update_phase()

            if phase == "drift":
                drift_shift += 0.5
            elif phase == "recovery":
                drift_shift *= 0.8
            elif phase == "cascade":
                drift_shift += 1.2

            new_row = {
                "timestamp": datetime.now(),
                "feature1": np.random.normal(50 + drift_shift, 5),
                "feature2": np.random.normal(30, 3)
            }

            with self.lock:
                self.data = pd.concat([self.data, pd.DataFrame([new_row])])
                self.data = self.data.tail(50000)

    def get_data(self):
        with self.lock:
            return self.data.copy()