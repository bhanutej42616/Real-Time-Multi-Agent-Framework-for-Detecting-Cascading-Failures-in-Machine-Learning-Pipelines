function updatePipeline(dataRisk, modelRisk, apiRisk) {

    const dataNode = document.getElementById("dataNode");
    const modelNode = document.getElementById("modelNode");
    const apiNode = document.getElementById("apiNode");

    dataNode.style.boxShadow = `0 0 ${dataRisk}px red`;
    modelNode.style.boxShadow = `0 0 ${modelRisk}px orange`;
    apiNode.style.boxShadow = `0 0 ${apiRisk}px purple`;

    document.getElementById("arrow1").style.background =
        dataRisk > 50 ? "red" : "#475569";

    document.getElementById("arrow2").style.background =
        modelRisk > 50 ? "red" : "#475569";
}