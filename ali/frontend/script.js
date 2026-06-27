const ctx = document.getElementById('riskChart').getContext('2d');

let presentationActive = false;
let narrationStep = 0;
let scenario = null;
let cascadeHistory = [];
let lastSpokenAlert = null;
let autoRecoverTimer = null;
let updateInterval = null;

let chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Data Risk', data: [], borderColor: '#3b82f6' },
            { label: 'Model Risk', data: [], borderColor: '#f59e0b' },
            { label: 'API Risk', data: [], borderColor: '#a855f7' },
            { label: 'Cascade Risk', data: [], borderColor: '#ef4444' },
            { 
              label: 'Predicted Cascade',
              data: [],
              borderColor: '#22c55e',
              borderDash: [5,5]
            }
        ]
    },
    options: {
        responsive: true,
        animation: { duration: 400 },
        scales: { y: { min: 0, max: 100 } }
    }
});

/* ---------------- VOICE ENGINE ---------------- */

function smoothFemaleVoice(text) {
    if (!window.speechSynthesis) return;

    const msg = new SpeechSynthesisUtterance(text);
    msg.rate = 0.9;
    msg.pitch = 1.05;
    msg.volume = 1;

    speechSynthesis.speak(msg);
}

/* ---------------- PRESENTATION MODE ---------------- */

function startPresentation() {

    presentationActive = true;
    narrationStep = 0;

    const steps = [
        { section: "hero", text: "This system introduces a real-time multi-agent cascade monitoring framework." },
        { section: "architecture", text: "Three agents monitor data validation, model inference, and API reliability." },
        { section: "architecture", text: "Instead of isolated detection, propagation risk is modeled across stages." },
        { section: "dashboard", text: "The red curve represents systemic cascade intensity." },
        { section: "dashboard", text: "The dashed green curve forecasts near-future escalation." },
        { section: "unique-section", text: "This enables proactive mitigation instead of reactive debugging." }
    ];

    function nextStep() {
        if (!presentationActive) return;
        if (narrationStep >= steps.length) {
            smoothFemaleVoice("Presentation complete. Autonomous monitoring continues.");
            return;
        }

        const step = steps[narrationStep];

        document.getElementById(step.section)
            .scrollIntoView({ behavior: "smooth" });

        smoothFemaleVoice(step.text);

        narrationStep++;
        setTimeout(nextStep, 7000);
    }

    nextStep();
}

document.getElementById("presentationToggle")
    .addEventListener("click", startPresentation);

/* ---------------- SCENARIO ENGINE ---------------- */

function injectScenario(type) {
    scenario = type;

    if (autoRecoverTimer) clearTimeout(autoRecoverTimer);

    autoRecoverTimer = setTimeout(() => {
        scenario = null;
        smoothFemaleVoice("Scenario automatically cleared. System returning to baseline equilibrium.");
    }, 20000);

    if (type === 'data_drift')
        smoothFemaleVoice("Data drift scenario injected. Upstream instability may propagate forward.");

    else if (type === 'model_collapse')
        smoothFemaleVoice("Model collapse scenario injected. Downstream prediction reliability degrading.");

    else if (type === 'api_latency')
        smoothFemaleVoice("API latency spike simulated. External response instability detected.");
}

function clearScenario() {
    scenario = null;
    smoothFemaleVoice("System manually restored to stable baseline.");
}

/* ---------------- STATISTICAL CORE ---------------- */

function calculateMean(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function calculateStd(arr, mean) {
    return Math.sqrt(
        arr.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / arr.length
    );
}

function forecastCascade(currentRisk) {

    cascadeHistory.push(currentRisk);
    if (cascadeHistory.length > 30) cascadeHistory.shift();

    if (cascadeHistory.length < 5)
        return currentRisk;

    const mean = calculateMean(cascadeHistory);
    const std = calculateStd(cascadeHistory, mean);

    let slope =
        (cascadeHistory[cascadeHistory.length - 1] -
         cascadeHistory[0]) / cascadeHistory.length;

    let prediction = currentRisk + slope * 5;

    const zScore = (currentRisk - mean) / (std || 1);

    if (Math.abs(zScore) > 2) {
        prediction += 10;
    }

    return Math.max(0, Math.min(100, prediction));
}

/* ---------------- RESEARCH LOG ENGINE ---------------- */

function generateResearchLog(data) {

    let log = "";

    if (cascadeHistory.length >= 5) {

        const mean = calculateMean(cascadeHistory);
        const std = calculateStd(cascadeHistory, mean);
        const zScore = (data.cascade_risk - mean) / (std || 1);

        if (Math.abs(zScore) > 2)
            log += "Statistical anomaly detected using Z-score analysis. ";

        if (data.cascade_risk > mean)
            log += "Cascade intensity above historical baseline. ";

        if (data.cascade_risk < mean)
            log += "Cascade stabilizing toward equilibrium. ";
    }

    if (scenario)
        log += "Active scenario influence detected: " + scenario + ". ";

    document.getElementById("logs").innerHTML =
        "<p>" + log + "</p>";
}

/* ---------------- REPORT EXPORT ---------------- */

function exportReport() {

    const content = `
ML Cascade Monitoring Research Report

Current Cascade Risk: ${document.getElementById("cascadeValue").innerText}
Scenario Active: ${scenario ? scenario : "None"}

System models cross-stage propagation using weighted cascade memory
and statistical anomaly amplification.

Generated at: ${new Date().toLocaleString()}
`;

    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "Cascade_Report.txt";
    link.click();

    smoothFemaleVoice("Research report exported successfully.");
}

/* ---------------- MAIN UPDATE LOOP ---------------- */

function update() {
    fetch("http://127.0.0.1:8000/metrics")
        .then(res => res.json())
        .then(data => {

            if (scenario === 'data_drift') data.data_risk += 25;
            if (scenario === 'model_collapse') data.model_risk += 30;
            if (scenario === 'api_latency') data.api_risk += 35;

            data.data_risk = Math.min(data.data_risk, 100);
            data.model_risk = Math.min(data.model_risk, 100);
            data.api_risk = Math.min(data.api_risk, 100);

            const predicted = forecastCascade(data.cascade_risk);

            chart.data.labels.push('');
            chart.data.datasets[0].data.push(data.data_risk);
            chart.data.datasets[1].data.push(data.model_risk);
            chart.data.datasets[2].data.push(data.api_risk);
            chart.data.datasets[3].data.push(data.cascade_risk);
            chart.data.datasets[4].data.push(predicted);

            if (chart.data.labels.length > 60) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(ds => ds.data.shift());
            }

            chart.update();

            document.getElementById("cascadeValue").innerText =
                data.cascade_risk.toFixed(1);

            document.getElementById("gaugeFill").style.height =
                data.cascade_risk + "%";

            const alertPanel = document.getElementById("alertPanel");
            alertPanel.innerText = data.alert;

            if (data.alert === "Critical Cascade")
                alertPanel.style.background = "red";
            else if (data.alert === "High Risk")
                alertPanel.style.background = "orange";
            else if (data.alert === "Warning")
                alertPanel.style.background = "yellow";
            else
                alertPanel.style.background = "green";

            if (data.alert !== lastSpokenAlert &&
                data.alert === "Critical Cascade") {
                smoothFemaleVoice("Critical cascade detected.");
                lastSpokenAlert = data.alert;
            }

            updatePipeline(
                data.data_risk,
                data.model_risk,
                data.api_risk
            );

            generateResearchLog(data);
        })
        .catch(err => {
            console.error("Backend not reachable:", err);
        });
}

if (!updateInterval)
    updateInterval = setInterval(update, 2000);