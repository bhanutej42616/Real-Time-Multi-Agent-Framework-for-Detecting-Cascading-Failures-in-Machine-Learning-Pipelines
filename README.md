# ML Cascade Monitoring System

**Real-Time Multi-Agent Cascade Monitoring for Machine Learning Pipelines**

The ML Cascade Monitoring System is a full-stack application designed to simulate, detect, and visualize systemic failures across different layers of a machine learning pipeline. By utilizing a multi-agent architecture, the system monitors the Data, Model, and API layers in real-time, identifying how minor data drifts can amplify into critical cascading failures downstream.

## 🚀 Features

- **Real-Time Risk Propagation:** Visualizes how statistical anomalies in the data layer (e.g., mean shift, variance explosion) propagate and amplify through the model and API layers.
- **Multi-Agent Architecture:** Specialized agents (DataAgent, ModelAgent, APIAgent, AlertAgent) independently monitor and evaluate risk at their respective pipeline stages.
- **Phase 6 Synthetic Drift Engine:** The mathematical core that generates synthetic data and computes statistical drift using Z-scores and KL Divergence.
- **Adaptive Thresholding:** Employs a dynamic threshold based on the 85th percentile of historical risk to trigger alerts, ensuring resilience against normal system fluctuations.
- **Interactive Scenarios:** Users can manually inject various drift types (Sudden Shock, Gradual Drift, etc.) via the dashboard to observe system responses.
- **AI Presentation Mode:** A built-in frontend feature that utilizes browser speech synthesis to explain the current system state and risk metrics.

## 🏗️ Architecture

The system is divided into a robust Python backend and an interactive web frontend.

### Backend (FastAPI)
- **`main.py`**: The API entry point that orchestrates the risk engines, simulators, and agents.
- **`engine/phase6_engine.py`**: The core mathematical engine responsible for synthetic data generation and statistical drift computation.
- **`agents.py`**: Defines the logic for the individual monitoring agents.
- **`simulator.py` & `state_manager.py`**: Manages the background simulation, cycling through different system states (normal, drift, recovery).

### Frontend (HTML/JS/CSS)
- **`index.html`**: The primary dashboard featuring live charts, pipeline visualizations, and scenario controls.
- **`script.js`**: Handles the client-side logic, including the Chart.js integration, polling the backend metrics, and the AI presentation mode.
- **`style.css`**: Provides the dark-themed, responsive styling for the dashboard.

## 🛠️ Tech Stack

- **Backend:** Python 3.12, FastAPI, Uvicorn, NumPy, SciPy, Pandas
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Chart.js

## 🚦 Getting Started

### Prerequisites
- Python 3.12+
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ml-cascade-monitoring.git
   cd ml-cascade-monitoring/ali
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the FastAPI Backend:**
   ```bash
   # From the backend directory
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

2. **Launch the Frontend:**
   Simply open `frontend/index.html` in your preferred web browser. No build step is required for the frontend.

## 📊 How It Works

1. The **DataSimulator** continuously generates synthetic data, advancing through predefined system phases.
2. The **Phase 6 Engine** calculates the statistical drift (Z-score, KL Divergence) of the current data against a baseline.
3. The **Agents** evaluate the risk at each layer, applying amplification factors as the risk propagates from Data -> Model -> API.
4. The **Frontend** polls the `/metrics` endpoint every 2 seconds, updating the live charts, pipeline visualizations, and alert panels based on the aggregated cascade risk.

## 📄 License

This project is licensed under the MIT License.
